from gmspython import *
import gams_abatement,global_settings

class abate(gmspython):
	def __init__(self,tech_db=None,nt=None,pickle_path=None,work_folder=None,kwargs_ns={},**kwargs_gs):
		databases = None if nt is None else [nt.database.copy()]
		super().__init__(module='pr_static',pickle_path=pickle_path,work_folder=work_folder,databases=databases,**kwargs_gs)
		if pickle_path is None:
			self.version = nt.version
			self.ns = {**self.ns, **self.namespace_global_sets(nt,tech_db.symbols,kwargs_ns), **self.namespace_global_variables(kwargs_ns)}
			self.ns_local = {**self.ns_local, **self.namespace_local_sets(nt)}
			for c in ["simplesum", "minimize_object", "EOP"]:
				setattr(self, c, getattr(gams_abatement, c)())
			for tree in nt.trees.values():
				DataBase.GPM_database.merge_dbs(self.model.database,tree.database,'first')
			DataBase.GPM_database.merge_dbs(self.model.database, tech_db, 'first')
			self.add_default_subsets()

	def use_EOP():
		pass

	# ---			1: Retrieve namespace from nesting trees		--- #
	def namespace_global_sets(self,nt,tech_db_syms,kwargs):
		""" retrieve attributes from global tree"""
		#NOGET HER SKAL LAVE DE KORREKTE NAVNE OM TIL "ID_"
		std_sets = {setname: getattr(nt,setname) for setname in ('n','nn','nnn','inp','out','int','wT','map_all','kno_out','kno_inp','s') if setname in nt.__dict__}
		self.sector = True if hasattr(nt,'s') else False
		std_sets['PwT_dom'] = nt.PwT_dom if self.version=='Q2P' else nt.wT
		std_sets['exo_mu'] = df('exo_mu',kwargs)
		std_sets['endo_PbT'] = df('endo_PbT',kwargs)
		std_sets['n_out'] = df('n_out',kwargs)
		for sym in tech_db_syms:
			std_sets[sym] = "ID_" + sym
		if self.sector is not False:
			std_sets['s_prod'] = df('s_prod',kwargs)
		return std_sets

	def add_default_subsets(self):
		self.model.database[self.n('n_out')] = self.get('out').levels[-1] if isinstance(self.get('out'),pd.MultiIndex) else self.get('out')
		if self.sector is not False:
			self.model.database[self.n('s_prod')] = self.get('out').levels[0]

	def namespace_global_variables(self,kwargs):
		"""create global namespace for variables used in partial equilibrium model. kwargs modify the names."""
		return {varname: df(varname,kwargs) for varname in self.default_variables}

	@property
	def default_variables(self):
		return ('PwThat','PbT','qS','qD','mu','sigma','eta','Peq','markup','qsumU','qsumX') #'tauS','tauLump'

	def namespace_local_sets(self,nt):
		"""create namespace for each tree, by copying attributes."""
		return {tree: {attr: nt.trees[tree].__dict__[attr] for attr in nt.trees[tree].__dict__ if attr not in set(['tree','database']).union(nt.prune_trees)} for tree in nt.trees}

	# ---			2: Initialize variables			--- #
	# Note: The method 'initialize_variables' should be provided; however, how this works is optional.
	def initialize_variables(self,**kwargs):
		try:
			if kwargs['check_variables'] is True:
				for var in self.default_variables:
					if self.ns[var] not in self.model.database.symbols:
						self.model.database[self.ns[var]] = self.default_var_series(var)
					else:
						self.model.database[self.ns[var]].vals = DataBase.merge_symbols(self.get(var),self.default_var_series(var))
		except KeyError:
			for var in self.default_variables:
				if self.ns[var] not in self.model.database.symbols:
					self.model.database[self.ns[var]] = self.default_var_series(var)
		if self.ns['exo_mu'] not in self.model.database.symbols:
			self.add_calibration_subsets()
		if self.state == 'calibrate':
			self.model.settings.set_conf('solve',self.add_solve + "\n")

	def default_var_series(self,var):
		if var=='PbT':
			return pd.Series(1, index = self.get('out'), name = self.n(var))
		elif var == 'PwThat':
			return pd.Series(1, index = self.get('PwT_dom'), name = self.n(var))
		elif var == 'qS':
			return pd.Series(1, index = self.get('out'), name = self.n(var))
		elif var == 'qD':
			return pd.Series(1, index = self.get('wT'), name = self.n(var))
		elif var == 'mu':
			return pd.Series(1, index = self.get('map_all'), name=self.n(var))
		elif var == 'sigma':
			return pd.Series(1, index = self.get('kno_inp'), name = self.n(var))
		elif var == 'eta':
			return pd.Series(-1, index = self.get('kno_out'), name = self.n(var))
		elif var == 'Peq':
			return pd.Series(1, index = self.get('n_out'), name = self.n(var))
		elif var == 'markup':
			return pd.Series(0, index = self.get('out'), name = self.n(var))
		# elif var == 'tauS':
		# 	return pd.Series(0, index = self.get('out'), name = self.n(var))
		# elif var == 'tauLump':
		# 	return 0 if self.sector is False else pd.Series(0, index = self.get('s_prod'), name = self.n(var))
		elif var == 'qsumU':
			return pd.Series(10, index = self.get('sumUaggs'), name = self.n(var))
		elif var == 'qsumX':
			return pd.Series(10, index = self.get('sumXaggs'), name = self.n(var))
		elif var == "M0":
			return pd.Series(5, index = self.get("M_subset"), name = self.n(var))
		elif var == "phi":
			return pd.Series(0.1, index = self.get("map_M2X"), name = self.n(var))
		elif var == "PwT":
			return pd.Series(1, index = self.get("inp"), name = self.n(var))
		

	def add_calibration_subsets(self):
		(self.model.database[self.ns['endo_PbT']],self.model.database[self.ns['exo_mu']]) = self.calib_subsets

	@property
	def calib_subsets(self):
		endo_pbt, exo_mu = empty_index(self.get('out')),empty_index(self.get('map_all'))
		for tree in self.ns_local:
			if self.n('type_io',tree=tree)=='input':
				endo_pbt = endo_pbt.union(self.get('tree_out',tree=tree))
				map_ = self.get('map_',tree=tree)
				exo_mu = exo_mu.union(map_[(map_.droplevel(self.n('nn')).isin(self.get('int')))])
			elif self.n('type_io',tree=tree)=='output':
				map_ = self.get('map_',tree=tree)
				tree_out = self.get('tree_out',tree=tree)
				for x in self.get('knots',tree=tree):
					z = map_[(map_.droplevel(self.n('n')).isin([x])) & (map_.droplevel(self.n('nn')).isin(tree_out))]
					if not z.empty:
						endo_pbt = endo_pbt.insert(0,z.droplevel(self.n('nn'))[0])
						exo_mu = exo_mu.insert(0,z[0])
				exo_mu = exo_mu.union(map_[~(map_.droplevel(self.n('nn')).isin(tree_out))])
		return endo_pbt,exo_mu

	# ---			3: Define groups	 		--- #

	def group_conditions(self,group):
		#PARAMETERS
		if group == 'g_params_alwaysexo':
			return [{'sigma': [{"and": [self.g('kno_inp'), {"not":self.g("tech_endoincalib_sigma")}]}], 'mu':self.g("params_alwaysexo_mu"), 'eta': self.g('kno_out')}]
			# return [{'sigma': self.g('kno_inp'), 'eta': self.g('kno_out'), 'mu': self.g('exo_mu')}]
		elif group == 'g_params_endoincalib':
			return [{"sigma": self.g("tech_endoincalib_sigma"), "mu":self.g("tech_endoincalib_mu")}, {'markup': self.g('out')}]
		#PRICES
		elif group == "g_prices_alwaysendo":
			return [{'PwThat': self.g('int'), 'PbT': self.g('endo_PbT')}]
		elif group == 'g_prices_alwaysexo':
			return [{'tauS': self.g('out'), 'tauLump': None if self.sector is False else self.g('s_prod')}] #'PwThat': self.g('inp')
		elif group == 'g_prices_exoincalib':
			return [{'PbT': {'and': [self.g('out'), {'not': self.g('endo_PbT')}]}, 'Peq': self.g('n_out')}]
		#QUANTITIES
		elif group == 'g_quants_alwaysendo':
			return [{'qD': [{"and":[self.g('int'), self.g("inp"), {"not":self.g("endovars_exoincalib_C")}]}]}]
		elif group == 'g_quants_alwaysexo':
			return [{'qS': [{"and":[self.g('out'), {"not":self.g("EOP_C_subset")}]}]}]
		elif group == 'g_quants_exoincalib':
			return [{"qD":self.g("endovars_exoincalib_C"), "qsumU":self.g("sumUaggs"), "qsumX":self.g("sumXaggs")}]
		#MINIMIZATION OBJECTS
		elif group == "g_minobj_exoincalib":
			return [{"weight_mu":None, "weight_sigma":None, "minobj_sigma":self.g("minobj_sigma_subset"), "minobj_mu":self.g("minobj_mu_subset")}]
		elif group == "g_minobj_endoincalib":
			return [{"minobj":None}]
		#EMISSION ACCOUNTS
		elif group == "g_emissions_alwaysendo":
			return [{"M0":self.g("M_subset"), "M":self.g("M_subset")}]
		elif group == "g_emissions_alwaysexo":
			return [{"phi":self.g("map_M2X")}]
		#END-OF-PIPE ABATEMENT
		elif group == "g_EOP_endogenousC":
			return [{"qS":self.g("EOP_C_subset")}]
		elif group == "g_EOP_endoincalib":
			return [{"theta":self.g("EOP_C_subset"), "muG":self.g("EOP_C_subset"), "sigmaG":self.g("EOP_C_subset")}]
		#END-OF-PIPE PRICES
		elif group == "g_EOP_alwaysexo":
			return [{"pM":self.g("M_subset"), "PwT":self.g("inp")}]
		elif group == "g_EOP_alwaysendo":
			return [{"pMhat":self.g("M_subset"), "PwThat":self.g("inp")}]
		#FJERN EOP VARIABLE i ID-MODE. 


	@property
	def exo_groups(self):
		""" Collect exogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ('g_params_alwaysexo', 'g_prices_alwaysexo', 'g_quants_alwaysexo', 'g_params_endoincalib', 'g_emissions_alwaysexo', 'g_EOP_alwaysexo', 'g_EOP_endoincalib')}
		elif self.state in ('calibrate','SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_params_alwaysexo', 'g_prices_alwaysexo', 'g_quants_alwaysexo', 'g_prices_exoincalib', 'g_quants_exoincalib', 'g_minobj_exoincalib')}

	@property
	def endo_groups(self):
		""" Collect endogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ('g_prices_alwaysendo', 'g_quants_alwaysendo', 'g_prices_exoincalib', 'g_quants_exoincalib', 'g_emissions_alwaysendo', "g_EOP_endogenousC", "g_EOP_alwaysendo")}
		elif self.state in ('calibrate', 'SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_prices_alwaysendo', 'g_quants_alwaysendo', 'g_params_endoincalib', 'g_minobj_endoincalib')}

	@property
	def add_solve(self):
		if self.state == 'calibrate':
			return f"""solve {self.model.settings.get_conf('name')} using NLP min {self.g('minobj').write()};"""
		else:
			return None

	# @property 
	# def sub_groups(self):
	# 	""" Collect groups that are subgroups of other groups; these are not written to list of exogenous/endogenous groups. """
	# 	n = self.model.settings.name+'_'
	# 	return {n+g: self.add_group(g,n=n) for g in ('g_tech_endo','g_tech_exo')}

	# --- 		4: Define blocks 		--- #
	@property
	def blocktext(self):
		blocks = {**{f"M_{tree}": self.eqtext(tree) for tree in self.ns_local}, **{f"M_{self.model.settings.name}_simplesum":self.init_simplesum()}}
		blocks[f"M_{self.model.settings.name}_EOP"] = self.init_EOP()
		if self.state == "calibrate":
			blocks[f"M_{self.model.settings.name}_minobj"] = self.init_minimize_object()
		return blocks
		#FJERN BLOCKS OM EOP i ID-mode

	@property
	def mblocks(self):
		blocks = [f"M_{tree}" for tree in self.ns_local] + [f"M_{self.model.settings.name}_simplesum"]
		blocks += [f"M_{self.model.settings.name}_EOP"]
		if self.state == "calibrate":
			blocks += [f"M_{self.model.settings.name}_minobj"]
		return set(blocks)
		#FJERN BLOCKS OM EOP i ID-mode

	def init_simplesum(self):
		self.simplesum.add_symbols(self.model.database, self.ns)
		self.simplesum.add_conditions()
		return self.simplesum.run()

	def init_minimize_object(self):
		self.minimize_object.add_symbols(self.model.database, self.ns)
		return self.minimize_object.run()
	
	def init_EOP(self):
		self.EOP.add_symbols(self.model.database, self.ns)
		self.EOP.add_conditions()
		return self.EOP.run("EOP")

	def eqtext(self,tree_name):
		tree = self.ns_local[tree_name]
		gams_class = getattr(gams_abatement,tree['type_f'])(version=tree['version'])
		gams_class.add_symbols(self.model.database,tree,ns_global=self.ns)
		gams_class.add_conditions(self.model.database,tree)
		return gams_class.run(tree_name)

	# ---		5: Special run methods 		--- #

	# # ---		6: Add sector  		--- #
	# def add_sector(self,s,add_to_existing_s=False,excep_global = ['n_out'],local_exceptions = {},**kwargs):
	# 	self.add_sector_to_namespace(**kwargs)
	# 	self.s = s
	# 	self.add_sector_to_sets(add_to_existing=add_to_existing_s)
	# 	self.add_sector_to_subsets(exceptions=excep_global)
	# 	self.add_sector_to_variables(exceptions=excep_global)
	# 	for tree in self.ns_local:
	# 		self.add_sector_to_local(tree,exceptions=local_exceptions[tree] if tree in local_exceptions else [])

	# def add_sector_to_namespace(self,**kwargs):
	# 	self.ns.update({set_: df(set_,kwargs) for set_ in ['s','s_prod']})

	# def add_sector_to_sets(self,add_to_existing=False):
	# 	if self.ns['s'] not in self.model.database.symbols:
	# 		self.model.database[self.ns['s']] = pd.Index([self.s],name=self.ns['s'])
	# 	elif add_to_existing is True:
	# 		self.model.database[self.ns['s']].vals = self.model.database[self.ns['s']].vals.union(pd.Index([self.s],name=self.ns[s]))

	# def add_sector_to_local(self,tree,exceptions=[]):
	# 	ste = ['name','type_io','version','temp_namespace','type_f']
	# 	[self.add_sector_to_subset(ss) for ss in set(self.dvbk(self.ns_local[tree],exceptions+ste)).intersection(set(self.model.database.sets['subsets']+self.model.database.sets['mappings']))];
	# 	[self.add_sector_to_variable(var) for var in set(self.dvbk(self.ns_local[tree],exceptions+ste)).intersection(set(self.model.database.variables_flat+self.model.database.parameters_flat))];

	# def dvbk(self,obj,exceptions):
	# 	return [v for k,v in obj.items() if k not in exceptions]

	# def add_sector_to_subsets(self,exceptions=['n_out']):
	# 	[self.add_sector_to_subset(ss) for ss in set(self.dvbk(self.ns,exceptions)).intersection(set(self.model.database.sets['subsets']+self.model.database.sets['mappings']))];

	# def add_sector_to_variables(self,exceptions=[]):
	# 	[self.add_sector_to_variable(var) for var in set(self.dvbk(self.ns,exceptions)).intersection(set(self.model.database.variables_flat+self.model.database.parameters_flat))];

	# def add_sector_to_variable(self,var):
	# 	db =self.model.database
	# 	if db[var].gtype in ('scalar_variable','scalar_parameter'):
	# 		gtype = db[var].gtype
	# 		db[var] = pd.Series(db[var],index=self.get('s')[self.get('s')==self.s],name=var)
	# 		db[var].gtype = gtype.split('_')[-1]
	# 	elif self.ns['s'] not in db[var].domains:
	# 		db[var].vals.index = DataBase_wheels.prepend_index_with_1dindex(db[var].index,self.get('s')[self.get('s')==self.s])

	# def add_sector_to_subset(self,subset):
	# 	db =self.model.database
	# 	if self.ns['s'] not in db[subset].domains:
	# 		db[subset] = DataBase_wheels.prepend_index_with_1dindex(db.get(subset),self.get('s')[self.get('s')==self.s])	

# class pr_dynamic(gmspython):
# 	def __init__(self,nt=None,pickle_path=None,work_folder=None,ict='ict_v1',gs_v='gs_v1',pw='pricewedge',kwargs_ns={},kwargs_st={},gs_vals={},**kwargs_gs):
# 		databases = None if nt is None else [nt.database.copy()]
# 		super().__init__(module='pr_dynamic',pickle_path=pickle_path,work_folder=work_folder,databases=databases,**kwargs_gs)
# 		if pickle_path is None:
# 			self.version = nt.version
# 			self.ns = {**self.ns, **self.namespace_global_sets(nt,kwargs_ns), **self.namespace_global_variables(kwargs_ns)}
# 			self.ns_local = {**self.ns_local, **self.namespace_local_sets(nt)}
# 			self.add_global_settings(gs_v,kwargs_ns=kwargs_ns,kwargs_vals=gs_vals,dynamic=True)
# 			self.ict = getattr(gams_production,ict)(**kwargs_ns)
# 			self.pw = getattr(gams_production,pw)()
# 			for tree in nt.trees.values():
# 				DataBase.GPM_database.merge_dbs(self.model.database,tree.database,'first')
# 			if 'ss' in kwargs_st:
# 				self.sector = True
# 				self.add_sector_ict(kwargs_st['ss'],**kwargs_ns)
# 			self.add_default_subsets()

# 	# ---			1: Retrieve namespace from nesting trees		--- #
# 	def namespace_global_sets(self,nt,kwargs):
# 		""" retrieve attributes from global tree"""
# 		std_sets = {setname: getattr(nt,setname) for setname in ('n','nn','nnn','inp','out','int','wT','map_all','kno_out','kno_inp','s') if setname in nt.__dict__}
# 		std_sets['PwT_dom'] = nt.PwT_dom if self.version=='Q2P' else nt.wT
# 		std_sets['exo_mu'] = df('exo_mu',kwargs)
# 		std_sets['endo_PbT'] = df('endo_PbT',kwargs)
# 		std_sets['n_out'] = df('n_out',kwargs)
# 		return std_sets

# 	def add_sector_set(self,set_,index):
# 		""" Add the sector index 's_prod' to an multiindex 'set_' at the index'th place. """
# 		return set_ if self.sector is False else DataBase_wheels.prepend_index_with_1dindex(set_,self.get('ss')).reorder_levels(set_.names[0:index]+self.g('ss').domains+set_.names[index:])

# 	def add_sector_set_from_product(self,list_of_sets,index):
# 		return pd.MultiIndex.from_product(list_of_sets) if self.sector is False else pd.MultiIndex.from_product(list_of_sets[0:index]+[self.get('ss')]+list_of_sets[index:])

# 	def add_default_subsets(self):
# 		self.model.database[self.n('n_out')] = self.get('out').levels[-1] if isinstance(self.get('out'),pd.MultiIndex) else self.get('out')

# 	def namespace_global_variables(self,kwargs):
# 		"""create global namespace for variables used in partial equilibrium model. kwargs modify the names."""
# 		return {varname: df(varname,kwargs) for varname in self.default_variables}

# 	@property
# 	def default_variables(self):
# 		return ('PwT','PbT','qS','qD','mu','sigma','eta','Peq','markup','tauS','tauLump','Rrate','rDepr')

# 	def namespace_local_sets(self,nt):
# 		"""create namespace for each tree, by copying attributes."""
# 		return {tree: {attr: nt.trees[tree].__dict__[attr] for attr in nt.trees[tree].__dict__ if attr not in set(['tree','database']).union(nt.prune_trees)} for tree in nt.trees}

# 	def add_sector_ict(self,sector,**kwargs):
# 		""" add the subset of sectors for which we apply the installation cost module. The sectoral set 's' must be included."""
# 		self.ns['ss'] = 's_prod' if 'ss' not in kwargs else kwargs['ss']
# 		self.model.database[self.ns['ss']] = self.get('s')[self.get('s').isin(sector)];
# 		self.ict.sector = self.ns['ss']

# 	# ---			2: Initialize methods			--- #
# 	def initialize_variables(self,**kwargs):
# 		try:
# 			if kwargs['check_variables'] is True:
# 				for var in self.default_variables:
# 					if self.ns[var] not in self.model.database.symbols:
# 						self.model.database[self.ns[var]] = self.default_var_series(var)
# 					else:
# 						self.model.database[self.ns[var]].vals = DataBase.merge_symbols(self.get(var),self.default_var_series(var))
# 		except KeyError:
# 			for var in self.default_variables:
# 				if self.ns[var] not in self.model.database.symbols:
# 					self.model.database[self.ns[var]] = self.default_var_series(var)
# 		if self.ns['exo_mu'] not in self.model.database.symbols:
# 			self.add_calibration_subsets()
# 		self.initialize_ict()

# 	# ---			2.1: Add time to the model durables			--- #
# 	def add_dur(self,dur,dur2inv=None,kwargs_ns={},**kwargs):
# 		""" Add the time index and durables to model. """ 
# 		self.add_dur_to_namespace(**kwargs_ns)
# 		self.add_durables_to_database(dur,dur2inv=dur2inv)

# 	def ivfs(self,static,variables=['qS','qD','PwT','PbT','Peq','tauS','tauLump'],merge=True):
# 		""" initialize variables from database w. static version """
# 		for var in variables:
# 			if var not in ('qD','PwT'):
# 				add_var = DataBase_wheels.repeat_variable_windex(static.get(self.ns[var]),self.get('txE'))
# 			else:
# 				ndurs = DataBase_wheels.repeat_variable_windex(static.get(self.ns[var]),self.get('txE'))
# 				durs  = DataBase_wheels.repeat_variable_windex(static.get(self.ns[var])[static.get(self.ns[var]).index.get_level_values(self.ns['n']).isin(self.get('dur'))],self.get('t'))
# 				add_var = ndurs.combine_first(durs)
# 			if merge is True and self.ns[var] in self.model.database.symbols:
# 				self.model.database[self.ns[var]] = add_var.combine_first(self.get(var))
# 			else:
# 				self.model.database[self.ns[var]] = add_var

# 	def add_dur_to_namespace(self,**kwargs):
# 		"""" add to namespace """
# 		self.ns.update({set_: df(set_,kwargs) for set_ in self.time_ns})

# 	@property
# 	def time_ns(self):
# 		return ('dur','ndur','inv','dur2inv')

# 	def add_durables_to_database(self,dur,dur2inv=None):
# 		self.add_durable_sets_to_database(dur,dur2inv=dur2inv)
# 		self.adjust_subsets_to_durables()
# 		for var in self.default_variables:
# 			if self.ns[var] not in self.model.database.symbols:
# 				self.model.database[self.ns[var]] = self.default_var_series(var)

# 	def adjust_subsets_to_durables(self):
# 		""" add investment goods to inputs, move durables to intermediate goods."""
# 		dur = self.get('inp')[self.get('inp').get_level_values(self.ns['n']).isin(self.get('dur'))] if self.sector is True else self.get('dur')
# 		inv = DataBase_wheels.mi.map_v1(dur,self.get('dur2inv')) if self.sector is True else self.get('inv')
# 		self.model.database[self.ns['inp']] = self.get('inp').drop(dur).union(inv)
# 		self.model.database[self.ns['wT']] = self.get('wT').union(inv)
# 		self.model.database[self.ns['PwT_dom']] = self.get('PwT_dom').union(inv)
# 		self.model.database[self.ns['int']] = self.get('int').union(dur)

# 	def add_durable_sets_to_database(self,dur,dur2inv=None):
# 		""" Add sets/subsets to database."""
# 		self.model.database[self.ns['dur']] = pd.Index(dur,name=self.ns['n'])
# 		if dur2inv is None:
# 			self.model.database[self.ns['dur2inv']] = pd.MultiIndex.from_tuples(list(zip(*[self.get('dur'),'I_'+self.get('dur')])), names = [self.ns['n'],self.model.database.alias_dict[self.ns['n']][0]])
# 		else:
# 			self.model.database[self.ns['dur2inv']] = dur2inv
# 		self.model.database[self.ns['inv']] = pd.Index(self.get('dur2inv').get_level_values(1).unique(),name=self.ns['n'])
# 		self.model.database[self.ns['ndur']]= pd.Index(set(self.get('n'))-set(self.get('dur'))-set(self.get('inv')),name=self.ns['n'])
# 		self.model.database[self.ns['n']] = self.get('n').union(self.get('inv'))

# 	# ---			2.2: Define default initial values for variables			--- #
# 	def initialize_ict(self):
# 		self.ict.add_symbols(self.model.database,self.ns)
# 		self.ict.add_conditions(self.model.database,self.ns)
# 		self.ns = {**self.ns,**self.ict.ns}

# 	def default_var_series(self,var):
# 		if var=='PbT':
# 			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('out'),self.get('txE')), name = self.n(var))
# 		elif var == 'PwT':
# 			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('PwT_dom'),self.get('txE')), name = self.n(var))
# 		elif var == 'qS':
# 			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('out'),self.get('txE')), name = self.n(var))
# 		elif var == 'qD':
# 			durables_tE = DataBase_wheels.prepend_index_with_1dindex(self.get('wT')[self.get('wT').get_level_values(self.ns['n']).isin(self.get('dur'))],self.get('tE'))
# 			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('wT'),self.get('txE')).union(durables_tE), name = self.n(var))
# 		elif var == 'mu':
# 			return pd.Series(1, index = self.get('map_all'), name=self.n(var))
# 		elif var == 'sigma':
# 			return pd.Series(0.5, index = self.get('kno_inp'), name = self.n(var))
# 		elif var == 'eta':
# 			return pd.Series(1, index = self.get('kno_out'), name = self.n(var))
# 		elif var == 'Peq':
# 			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('n_out'),self.get('txE')), name = self.n(var))
# 		elif var == 'markup':
# 			return pd.Series(0, index = self.get('out'), name = self.n(var))
# 		elif var == 'tauS':
# 			return pd.Series(0, index = DataBase_wheels.prepend_index_with_1dindex(self.get('out'),self.get('txE')), name = self.n(var))
# 		elif var == 'tauLump':
# 			index = self.get('txE') if self.sector is False else DataBase_wheels.prepend_index_with_1dindex(self.get('s_prod'),self.get('txE'))
# 			return pd.Series(0, index = index, name=self.n(var))
# 		elif var=='Rrate':
# 			return pd.Series(self.get('R_LR'), index = self.get('txE'), name = self.ns['Rrate'])
# 		elif var=='rDepr':
# 			return pd.Series(0.05, index = self.add_sector_set_from_product([self.get('t'),self.get('dur')],1),name=self.ns['rDepr'])
# 		elif var in self.ict.ns:
# 			return self.ict.default_var_series(var)

# 	def ss_rDepr(self,GE_data,inplace=True):
# 		inv = DataBase_wheels.mi.v1_series(GE_data[self.n('qD')].rctree_pd(self.g('inv')), pd.MultiIndex.from_tuples(self.get('dur2inv').swaplevel(0,1).values,names=[self.n('n'),self.n('nn')]))
# 		rDepr = pd.Series(DataBase_wheels.repeat_variable_windex(inv/GE_data[self.n('qD')].rctree_pd(self.g('dur'))-self.get('g_LR'),self.get('t')),name=self.n('rDepr'))
# 		if inplace is True:
# 			self.model.database[self.n('rDepr')] = rDepr
# 		else:
# 			return rDepr

# 	# ---			3: Define groups	 		--- #	
# 	def group_conditions(self,group):
# 		if group == 'g_tech_exo':
# 			return [{'sigma': self.g('kno_inp'), 'eta': self.g('kno_out'), 'mu': self.g('exo_mu')}]
# 		elif group == 'g_tech_exo_dyn':
# 			return [{'rDepr': self.g('dur'),'Rrate': None}]
# 		elif group == 'g_tech_endo':
# 			return [{'mu': {'and': [self.g('map_all'), {'not': self.g('exo_mu')}]},'markup': self.g('out')}]
# 		elif group == 'gvars_endo':
# 			return [{'PbT': self.g('endo_PbT'), 'PwT': self.g('int'), 'qD': {'or': [{'and': [self.g('wT'), self.g('tx0')]}, {'and': [self.g('int'), self.g('t0'), {'not': self.g('dur')}]}]},'Peq': {'and': [self.g('n_out'),self.g('tx0E')]}}]
# 		elif group == 'gvars_exo':
# 			return [{'qS': self.g('out'), 'PwT': self.g('inp'), 'qD': {'and': [self.g('dur'), self.g('t0')]}, 'tauS': self.g('out'), 'tauLump': None if self.sector is False else self.g('s_prod')}]
# 		elif group == 'g_calib_exo':
# 			return [{'qD': {'and': [self.g('inp'), self.g('t0')]}, 'PbT': {'and': [self.g('t0'),self.g('out'),{'not': self.g('endo_PbT')}]}, 'Peq': {'and': [self.g('t0'), self.g('n_out')]}}]
# 		elif group == 'g_tech':
# 			return ['g_tech_exo','g_tech_exo_dyn','g_tech_endo']
# 		elif group == 'g_vars_exo':
# 			return ['gvars_exo']
# 		elif group == 'g_vars_endo':
# 			return ['gvars_endo','g_calib_exo']
# 		else:
# 			return self.ict.group_conditions(group)

# 	@property
# 	def exo_groups(self):
# 		""" Collect exogenous groups """
# 		n = self.model.settings.name+'_'
# 		if self.state=='B':
# 			return {n+g: self.add_group(g,n=n) for g in ['g_tech','g_vars_exo']+self.ict.exo_groups()}
# 		elif self.state in ('SC','DC'):
# 			return {n+g: self.add_group(g,n=n) for g in ['g_tech_exo','g_tech_exo_dyn','gvars_exo','g_calib_exo']+self.ict.endo_groups()}

# 	@property
# 	def endo_groups(self):
# 		""" Collect endogenous groups """
# 		n = self.model.settings.name+'_'
# 		if self.state=='B':
# 			return {n+g: self.add_group(g,n=n) for g in ['g_vars_endo']+self.ict.endo_groups()}
# 		elif self.state in ('SC','DC'):
# 			return {n+g: self.add_group(g,n=n) for g in ['g_tech_endo','gvars_endo']+self.ict.endo_groups()}

# 	@property 
# 	def sub_groups(self):
# 		""" Collect groups that are subgroups of other groups; these are not written to list of exogenous/endogenous groups. """
# 		n = self.model.settings.name+'_'
# 		if self.state=='B':
# 			return {n+g: self.add_group(g,n=n) for g in ('g_tech_exo','g_tech_exo_dyn','g_tech_endo','gvars_exo','gvars_endo','g_calib_exo')}
# 		elif self.state in ('SC','DC'):
# 			return {}

# 	# --- 		4: Define blocks 		--- #
# 	@property
# 	def blocktext(self):
# 		return {**{f"M_{tree}": self.eqtext(tree) for tree in self.ns_local},
# 				**{f"M_{self.model.settings.name}_pw":self.init_pw(), f"M_{self.model.settings.name}_cf": self.ict.run(self.model.settings.name)}}
# 	@property
# 	def mblocks(self):
# 		return set([f"M_{tree}" for tree in self.ns_local]+[f"M_{self.model.settings.name}_pw",f"M_{self.model.settings.name}_cf"])

# 	def init_pw(self):
# 		self.pw.add_symbols(self.model.database,self.ns,dynamic=True)
# 		self.pw.add_conditions(self.model.database,dynamic=True)
# 		return self.pw.run(self.model.settings.name)

# 	def eqtext(self,tree_name):
# 		tree = self.ns_local[tree_name]
# 		gams_class = getattr(gams_production,tree['type_f'])(version=tree['version'])
# 		gams_class.add_symbols(self.model.database,tree,ns_global=self.ns,dynamic=True)
# 		gams_class.add_conditions(self.model.database,tree,dynamic=True)
# 		return gams_class.run(tree_name)

# 	def add_calibration_subsets(self):
# 		(self.model.database[self.ns['endo_PbT']],self.model.database[self.ns['exo_mu']]) = self.calib_subsets

# 	@property
# 	def calib_subsets(self):
# 		endo_pbt, exo_mu = empty_index(self.get('out')),empty_index(self.get('map_all'))
# 		for tree in self.ns_local:
# 			if self.n('type_io',tree=tree)=='input':
# 				endo_pbt = endo_pbt.union(self.get('tree_out',tree=tree))
# 				map_ = self.get('map_',tree=tree)
# 				exo_mu = exo_mu.union(map_[(map_.droplevel(self.n('nn')).isin(self.g('int').rctree_pd({'not': self.g('dur')})))])
# 			elif self.n('type_io',tree=tree)=='output':
# 				map_ = self.get('map_',tree=tree)
# 				tree_out = self.get('tree_out',tree=tree)
# 				for x in self.get('knots',tree=tree):
# 					z = map_[(map_.droplevel(self.n('n')).isin([x])) & (map_.droplevel(self.n('nn')).isin(tree_out))]
# 					endo_pbt = endo_pbt.insert(0,z.droplevel(self.n('nn'))[0])
# 					exo_mu = exo_mu.insert(0,z[0])
# 				exo_mu = exo_mu.union(map_[~(map_.droplevel(self.n('nn')).isin(tree_out))])
# 		return endo_pbt,exo_mu

