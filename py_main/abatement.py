from gmspython import *
import gams_abatement,global_settings

class abate(gmspython):
	def __init__(self,nt=None,tech=None,pickle_path=None,work_folder=None,kwargs_ns={},use_EOP=False,**kwargs_gs):
		databases = None if nt is None else [nt.database.copy()]
		super().__init__(module='abate',pickle_path=pickle_path,work_folder=work_folder,databases=databases,**kwargs_gs)
		if pickle_path is None:
			self.version = nt.version
			self.ns = {**self.ns, **self.namespace_global_sets(nt,nt.name,kwargs_ns), **self.namespace_global_variables(kwargs_ns)}
			self.ns_local = {**self.ns_local, **self.namespace_local_sets(nt)}
			for tree in nt.trees.values():
				DataBase.GPM_database.merge_dbs(self.model.database,tree.database,'first')
			self.add_globals(tech,kwargs_ns,m=nt.name)
			self.setstate('ID',init=False)

	# ------------------ 1: Initialization  ------------------ #
	# ---------------- 1.1: Namespaces and sets  ------------- #
	def namespace_global_sets(self,nt,state,kwargs):
		std_sets = {s: getattr(nt,s) for s in ['n','nn','nnn','nnnn']+[state+'_'+ss for ss in ('inp','out','int','wT','map_all','kno_out','kno_inp')] if s in nt.__dict__}
		self.sector = True if hasattr(nt,'s') else False
		std_sets['z'] = df('z',kwargs) # emissions
		if self.sector:
			std_sets['s_prod'] = df('s_prod',kwargs)
		return std_sets

	def namespace_local_sets(self,nt):
		"""create namespace for each tree by copying attributes."""
		return {tree: {attr: nt.trees[tree].__dict__[attr] for attr in nt.trees[tree].__dict__ if attr not in set(['tree','database']).union(nt.prune_trees)} for tree in nt.trees}

	def namespace_global_variables(self,kwargs):
		"""create global namespace for variables used in partial equilibrium model. kwargs modify the names."""
		return {varname: df(varname,kwargs) for varname in self.default_variables}

	@property
	def default_variables(self):
		return ('PbT','PwT','PwThat','pM','pMhat','qD','qS','qsumU','qsumX','M0','M','phi','mu','sigma','eta','gamma_tau','curapp_ID','currapp_EOP')
		# return ('PwThat','PbT','qS','qD','mu','sigma','eta','qsumU','qsumX', "PwT", "M0", "M", "phi", "gamma_tau", "currapp_ID", "currapp_EOP")

	def add_globals(self,tech,kwargs,m='ID'):
		""" Define global 'levels' mappings and subsets, e.g. all technology goods across nesting trees. """
		self.ns.update({s: df(s,kwargs) for s in [m+'_'+ss for ss in ('t','t_all','c','e','u','u_all','ai')]})
		self.ns.update({s: df(s,kwargs) for s in [m+'_'+ss for ss in ('i2t','u2t','u2c','c2e','e2u','e2t','e2ai2i','e2ai')]})
		# Technology sets:
		self.model.database[self.n(m+'_t')] = pd.Index(tech[m]['techs'].keys(),name=self.n('n'))
		self.model.database[self.n(m+'_t_all')] = pd.Index(tech[m]['basetechs'].keys(),name=self.n('n'))
		self.model.database[self.n(m+'_c')] = pd.Index(tech[m]['components'].keys(),name=self.n('n'))
		self.model.database[self.n(m+'_e')] = pd.Index(tech[m]['upper_categories'].keys(),name=self.n('n'))
		self.model.database[self.n(m+'_u_all')] = pd.Index([x for y in tech[m]['components'].values() for x in y], name = self.n('n'))
		self.model.database[self.n(m+'_u')] = self.get(m+'_u_all').difference(pd.Index([x for y in tech[m]['basetechs'].values() for x in y], name = self.n('n')))
		self.model.database[self.n(m+'_ai')] = tech[m]['Q2P'].levels[1].rename(self.n('n'))
		# Mappings:
		self.model.database[self.n(m+'_i2t')] = self.get(m+'_map_all')[(self.get(m+'_map_all').get_level_values(self.n('n')).isin(self.get(m+'_inp'))) & (self.get(m+'_map_all').get_level_values(self.n('nn')).isin(self.get(m+'_t_all')))]
		self.model.database[self.n(m+'_u2t')] = self.get(m+'_map_all')[(self.get(m+'_map_all').get_level_values(self.n('n')).isin(self.get(m+'_u_all'))) & (self.get(m+'_map_all').get_level_values(self.n('nn')).isin(self.get(m+'_t_all')))]
		self.model.database[self.n(m+'_u2c')] = self.get(m+'_map_all')[(self.get(m+'_map_all').get_level_values(self.n('n')).isin(self.get(m+'_u_all'))) & (self.get(m+'_map_all').get_level_values(self.n('nn')).isin(self.get(m+'_c')))]
		self.model.database[self.n(m+'_c2e')] = self.get(m+'_map_all')[(self.get(m+'_map_all').get_level_values(self.n('n')).isin(self.get(m+'_c'))) & (self.get(m+'_map_all').get_level_values(self.n('nn')).isin(self.get(m+'_e')))]
		self.model.database[self.n(m+'_e2u')] = DataBase_wheels.appmap(self.get(m+'_u2c'),DataBase_wheels.map_from_mi(self.get(m+'_c2e'),self.n('n'),self.n('nn')),self.n('nn')).swaplevel(0,1).set_names([self.n('n'),self.n('nn')])
		self.model.database[self.n(m+'_e2t')] = DataBase_wheels.appmap(self.get(m+'_e2u'),DataBase_wheels.map_from_mi(self.get(m+'_u2t'),self.n('n'),self.n('nn')),self.n('nn')).unique()
		t2i2ai = DataBase_wheels.mi.add_ndmi(self.get(m+'_i2t').swaplevel(0,1).set_names([self.n('n'),self.n('nn')]),tech[m]['Q2P'].set_names([self.n('nn'),self.n('nnn')]))
		self.model.database[self.n(m+'_e2ai2i')] = DataBase_wheels.appmap(t2i2ai,DataBase_wheels.map_from_mi(self.get(m+'_e2t'),self.n('nn'),self.n('n')),self.n('n')).swaplevel(1,2).set_names([self.n('n'),self.n('nn'),self.n('nnn')])
		self.model.database[self.n(m+'_e2ai')] = self.get(m+'_e2ai2i').droplevel(self.n('nnn')).unique()

	# ---------------- 1.2: Variables  ------------- #
	def default_var_series(self,var):
		""" """
		if var=='PbT':
			return pd.Series(1, index = self.get('ID_out'), name = self.n(var))
		elif var == 'PwT':
			return pd.Series(1, index = self.get('ID_inp'), name = self.n(var))
		elif var == 'PwThat':
			return pd.Series(1, index = self.get('ID_wT'), name = self.n(var))
		elif var == 'pM':
			return pd.Series(1, index = self.get('z'), name = self.n(var))
		elif var == 'pMhat':
			return pd.Series(1, index = self.get('z'), name = self.n(var))
		elif var == 'qD':
			s = pd.Series(1, index = self.get('ID_wT'), name = self.n(var))
			return s.combine_first(pd.Series(1, index = self.get('ai'), name = self.n(var)))
		elif var == 'qS':
			return pd.Series(1, index = self.get('ID_out'), name = self.n(var))
		elif var == 'qsumU':
			return pd.Series(1, index = self.get('ID_e2t'), name = self.n(var))
		elif var == 'qsumX':
			return pd.Series(1, index = self.get('ID_e2ai'), name = self.n(var))
		elif var == 'M0':
			return pd.Series(1, index = self.get('z'), name = self.n(var))
		elif var == 'M':
			return pd.Series(1, index = self.get('z'), name = self.n(var))
		elif var == 'phi':
			return pd.Series(0, index = pd.MultiIndex.from_product([self.get('z'),self.get('ID_ai')]))
		elif var == 'mu':
			return pd.Series(1, index = self.get('ID_map_all'), name=self.n(var))
		elif var == 'sigma':
			return pd.Series(0.01, index = self.get('ID_kno_inp'),name = self.n(var))
		elif var == 'eta':
			return pd.Series(-0.01, index = self.get('ID_kno_out'), name = self.n(var))
		elif var == 'gamma_tau':
			return pd.Series(1, index = self.get('ID_e2t'), name = self.n(var))
		elif var == 'currapp_ID':
			return pd.Series(0.05, index = self.get('e2t'), name = self.n(var))

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
		if 'calibrate' in self.state:
			self.model.settings.set_conf('solve',self.add_solve + "\n")

	# ------------------ 2: Groups  ------------------ #
	def group_conditions(self,group):
		if group == 'g_ID_params_alwaysexo':
			return [{'sigma': self.g('ID_kno_inp'), }]

	# ---			3: Define groups	 		--- #
	def group_conditions(self,group):
		#PARAMETERS
		if group == 'g_ID_params_alwaysexo':
			return [{'sigma': self.g('ID_kno_inp'), 'mu':self.g("ID_params_alwaysexo_mu"), 'eta': self.g('ID_kno_out')}]
			# return [{'sigma': {"and": [self.g('ID_kno_inp'), {"not":self.g("ID_tech_endoincalib_sigma")}]}, 'mu':self.g("ID_params_alwaysexo_mu"), 'eta': self.g('ID_kno_out')}]
		if group == "g_EOP_params_alwaysexo":
			return [{"theta":self.g("EOP_out"), 'sigma': self.g('EOP_kno_inp'), 'mu':self.g("EOP_params_alwaysexo_mu"), 'eta': self.g('EOP_kno_out')}]
		elif group == 'g_ID_params_endoincalib':
			return [{"mu":self.g("ID_tech_endoincalib_mu")}]
		elif group == "g_EOP_params_endoincalib":
			return [{"muG":self.g("EOP_out"), "sigmaG":self.g("EOP_out")}]
		#PRICES
		elif group == "g_ID_prices_alwaysendo":
			return [{'PwThat': {"or":[self.g('ID_int'), self.g("ID_inp")]}, 'PbT': self.g('ID_out')}]
		elif group == "g_EOP_prices_alwaysendo":
			return [{'PwThat': {"or":[self.g('EOP_int'), self.g("EOP_inp")]}, 'PbT': self.g('EOP_out')}]
		elif group == 'g_ID_prices_alwaysexo':
			return [{"PwT":self.g("ID_inp")}] 
		elif group == 'g_EOP_prices_alwaysexo':
			return [{"PwT":self.g("EOP_inp")}] 
		elif group == "g_prices_alwaysexo":
			return [{"pM":self.g("M_subset")}]
		elif group == "g_prices_endogenouswithEOP":
			return [{"pMhat":self.g("M_subset")}]
		#QUANTITIES
		elif group == 'g_ID_quants_alwaysendo':
			return [{'qD': {"and":[{"or":[self.g('ID_int'), self.g("ID_inp")]}, {"not":{"or":[self.g("ID_endovars_exoincalib_C"), self.g("ID_endovars_exoincalib_E")]}}]}, "qsumU":self.g("ID_sumUaggs")}]
			# return [{'qD': {"and":[{"or":[self.g('ID_int'), self.g("ID_inp")]}, {"not":[{"or":[self.g("ID_endovars_exoincalib_C"), self.g("ID_endovars_exoincalib_E")]}]}]}}]
		elif group == 'g_EOP_quants_alwaysendo':
			return [{'qD': {"and":[{"or":[self.g('EOP_int'), self.g("EOP_inp")]}]}, "qS":self.g("EOP_out"), "qsumU":self.g("EOP_sumUaggs")}] #component outputs are endogenous in the EOP world
		elif group == 'g_ID_quants_alwaysexo':
			return [{'qS': {"and":[self.g('ID_out')]}}]
		elif group == 'g_ID_quants_exoincalib':
			#sumXaggs does not distinguish between ID and EOP, it is always the same:
			return [{"qD":{"or":[self.g("ID_endovars_exoincalib_C"), self.g("ID_endovars_exoincalib_E")]}, "currapp_ID":self.g("currapp_ID_subset"), "qsumX":{"or":[self.g('sumXinEaggs'), self.g("sumXrestaggs")]}}] 
		elif group == 'g_EOP_quants_exoincalib':
			return [{"currapp_EOP":self.g("currapp_EOP_subset")}]
		#EMISSION ACCOUNTS
		elif group == "g_emissions_alwaysendo":
			return [{"M0":self.g("M_subset")}]
		elif group == "g_emissions_alwaysexo":
			return [{"phi":self.g("map_M2X")}]
		elif group == "g_emissions_endoinEOP":
			return [{"M":self.g("M_subset")}]
		#MINIMIZATION OBJECTS
		elif group == "g_ID_minobj_exoincalib_endoinbaseline":
			return [{"currapp_ID_modified":self.g("currapp_ID_subset")}]
		elif group == "g_ID_minobj_exoincalib":
			return [{"weight_mu":None, "mubar":self.g("map_ID_nonBUC")}]
		elif group == "g_EOP_minobj_exoincalib":
			return [{"weight_muG":None, "weight_sigmaG":None, "minobj_sigmaG":self.g("EOP_out"), "minobj_muG":self.g("EOP_out")}]
		elif group == "g_minobj_endoincalib":
			return [{"minobj":None}]
		elif group == "g_minobj_endoincalib_exoinbaseline":
			return [{"gamma_tau":self.g("map_T2E")}]

	@property
	def exo_groups(self):
		""" Collect exogenous groups """
		n = self.model.settings.name+'_'
		gs = ('g_ID_params_alwaysexo', 'g_ID_prices_alwaysexo', "g_prices_alwaysexo", 'g_ID_quants_alwaysexo', 'g_emissions_alwaysexo')	
		if self.state.startswith("EOP"):
			gs += ('g_EOP_params_alwaysexo', 'g_EOP_prices_alwaysexo')
			if "EOPcalibrate" == self.state:
			#exoincalib
				gs += ('g_ID_quants_exoincalib', 'g_EOP_quants_exoincalib', "g_ID_minobj_exoincalib", "g_EOP_minobj_exoincalib", "g_ID_minobj_exoincalib_endoinbaseline")
			else:
				gs += ('g_ID_params_endoincalib', "g_EOP_params_endoincalib", "g_minobj_endoincalib_exoinbaseline")
		else:
			gs += ('g_prices_endogenouswithEOP', 'g_ID_params_endoincalib', "g_minobj_endoincalib_exoinbaseline")
		
		return {n+g: self.add_group(g,n=n) for g in gs}

	@property
	def endo_groups(self):
		""" Collect endogenous groups """
		n = self.model.settings.name+'_'
		gs = ('g_ID_prices_alwaysendo', 'g_emissions_alwaysendo', 'g_ID_quants_alwaysendo')
		if self.state.startswith("EOP"):
			gs = gs + ("g_EOP_prices_alwaysendo", 'g_prices_endogenouswithEOP', "g_EOP_quants_alwaysendo", "g_emissions_endoinEOP")
			if self.state == "EOPcalibrate":
				gs += ('g_EOP_params_endoincalib', 'g_minobj_endoincalib', "g_minobj_endoincalib_exoinbaseline")
			else:
				gs += ('g_ID_quants_exoincalib', "g_EOP_quants_exoincalib", "g_ID_minobj_exoincalib_endoinbaseline")
		else:
			gs += ('g_ID_quants_exoincalib', "g_ID_minobj_exoincalib_endoinbaseline")

		return {n+g: self.add_group(g,n=n) for g in gs}

	@property
	def add_solve(self):
		if self.state == 'EOPcalibrate':
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
		blocks = {**{f"M_{tree}": self.eqtext(tree) for tree in self.ns_local if tree.startswith("ID_")}, \
					**{f"M_{self.model.settings.name}_simplesumU_ID":self.init_simplesumU("ID"), \
						f"M_{self.model.settings.name}_simplesumX_ID":self.init_simplesumX("ID"), \
						f"M_ID_{self.model.settings.name}_emissionaccounts":self.init_emission_accounts("ID"), \
						f"M_{self.model.settings.name}_sumXinE":self.init_sumXinE(), \
						f"M_{self.model.settings.name}_currentapplications_ID":self.init_currentapplications("ID")}}
		if self.state.startswith("EOP"):
		# if self.use_EOP:
			blocks[f"M_EOP_{self.model.settings.name}_emissionaccounts"] = self.init_emission_accounts("EOP")
			blocks = {**blocks, **{f"M_{tree}": self.eqtext(tree) for tree in self.ns_local if tree.startswith("EOP_")}}
			blocks[f"M_{self.model.settings.name}_EOP"] = self.init_EOP_eqs()
			blocks[f"M_{self.model.settings.name}_simplesumU_EOP"] = self.init_simplesumU("EOP")
			blocks[f"M_{self.model.settings.name}_simplesumX_EOP"] = self.init_simplesumX("EOP")
			blocks[f"M_{self.model.settings.name}_currentapplications_EOP"] = self.init_currentapplications("EOP")
		if self.state == "EOPcalibrate":
			blocks[f"M_EOP_{self.model.settings.name}_minobj"] = self.init_minimize_object(self.state)
		return blocks

	@property
	def mblocks(self):
		blocks = [f"M_{tree}" for tree in self.ns_local if tree.startswith("ID_")] + [f"M_{self.model.settings.name}_simplesumU_ID"]
		blocks += [f"M_ID_{self.model.settings.name}_emissionaccounts"]
		blocks += [f"M_{self.model.settings.name}_sumXinE"]
		blocks += [f"M_{self.model.settings.name}_currentapplications_ID"]

		if self.state.startswith("EOP"):
		# if self.use_EOP:
			blocks += [f"M_{tree}" for tree in self.ns_local if tree.startswith("EOP_")]
			blocks += [f"M_{self.model.settings.name}_EOP"] + [f"M_{self.model.settings.name}_simplesumU_EOP"]
			blocks += [f"M_{self.model.settings.name}_simplesumX_EOP"]
			blocks += [f"M_EOP_{self.model.settings.name}_emissionaccounts"]
			blocks += [f"M_{self.model.settings.name}_currentapplications_EOP"]
		else:
			blocks += [f"M_{self.model.settings.name}_simplesumX_ID"]
		
		if self.state == "EOPcalibrate":
			blocks += [f"M_EOP_{self.model.settings.name}_minobj"]
		return set(blocks)

	def init_simplesumU(self,state):
		simplesumU = getattr(gams_abatement, "simplesumU")(state=state)
		simplesumU.add_symbols(self.model.database, self.ns)
		simplesumU.add_conditions()
		return simplesumU.run()
	
	def init_simplesumX(self, state):
		simplesumX = getattr(gams_abatement, "simplesumX")(state=state)
		simplesumX.add_symbols(self.model.database, self.ns)
		simplesumX.add_conditions()
		return simplesumX.run()

	def init_sumXinE(self):
		sumXinE = getattr(gams_abatement, "sumXinE")()
		sumXinE.add_symbols(self.model.database, self.ns)
		sumXinE.add_conditions()
		return sumXinE.run()

	def init_emission_accounts(self, state):
		emission_accounts = getattr(gams_abatement, "emission_accounts")(state=state)
		emission_accounts.add_symbols(self.model.database, self.ns)
		emission_accounts.add_conditions()
		return emission_accounts.run("emission_accounts")

	def init_currentapplications(self, state):
		currentapplications = getattr(gams_abatement, "currentapplications")(state=state)
		currentapplications.add_symbols(self.model.database, self.ns)
		currentapplications.add_conditions()
		return currentapplications.run(self.ns_local["ID_CU"]["type_f"])

	def init_minimize_object(self, state):
		minimize_object = getattr(gams_abatement, "minimize_object")(state=state)
		minimize_object.add_symbols(self.model.database, self.ns)
		minimize_object.add_conditions()
		return minimize_object.run()

	def init_EOP_eqs(self):
		EOP = getattr(gams_abatement, "EOP")()
		EOP.add_symbols(self.model.database, self.ns)
		EOP.add_conditions()
		return EOP.run("EOP")

	def eqtext(self,tree_name):
		tree = self.ns_local[tree_name]
		if "ID" in tree_name:
			treestate = "ID"
		elif "EOP" in tree_name:
			treestate = "EOP"
		gams_class = getattr(gams_abatement,tree['type_f'])(version=tree['version'], state=treestate)
		gams_class.add_symbols(self.model.database,tree,ns_global=self.ns)
		gams_class.add_conditions(self.model.database,tree)
		return gams_class.run(tree_name)
