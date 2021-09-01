from gmspython import *
import gams_abatement,global_settings
from DB2Gams import OrdSet as OS

class abate(gmspython):
	def __init__(self,nt=None,tech=None,pickle_path=None,work_folder=None,kwargs_ns={},use_EOP=False,**kwargs_gs):
		databases = None if nt is None else [nt.database.copy()]
		super().__init__(module='abate',pickle_path=pickle_path,work_folder=work_folder,databases=databases,**kwargs_gs)
		if pickle_path is None:
			self.version = nt.version
			self.ns = {**self.ns, **self.namespace_global_sets(nt,'ID',kwargs_ns), **self.namespace_global_variables(kwargs_ns)}
			self.ns_local = {**self.ns_local, **self.namespace_local_sets(nt)}
			for tree in nt.trees.values():
				DataBase.GPM_database.merge_dbs(self.model.database,tree.database,'first')
			self.add_globals(tech,kwargs_ns)
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
		return ('PbT','PwT','PwThat','pM','pMhat','qD','qS','qsumU','qsumX','M0','M','phi','mu','sigma','eta','gamma_tau','currapp_ID')

	def add_globals(self,tech,kwargs):
		""" Define global 'levels' mappings and subsets, e.g. all technology goods across nesting trees. """
		self.ns.update({s: df(s,kwargs) for s in ['ID_'+ss for ss in ['t_all','ai']]})
		self.ns.update({s: df(s,kwargs) for s in ['ID_'+ss for ss in ['i2t']]})
		# level sets:
		self.model.database[self.n('ID_t_all')] = self.get('kno_ID_TX').union(self.get('kno_ID_BX'))
		self.model.database[self.n('ai')] = tech['ID']['Q2P'].levels[1].rename(self.n('n'))
		# Mappings:
		self.model.database[self.n('ID_i2t')] = self.get('ID_map_all')[(self.get('ID_map_all').get_level_values(self.n('n')).isin(self.get('ID_inp'))) & (self.get('ID_map_all').get_level_values(self.n('nn')).isin(self.get('ID_t_all')))]
		self.model.database[self.n('ID_u2t')] = self.get('ID_map_all')[(self.get('ID_map_all').get_level_values(self.n('n')).isin(self.get('bra_ID_CU'))) & (self.get('ID_map_all').get_level_values(self.n('nn')).isin(self.get('ID_t_all')))]
		self.model.database[self.n('ID_e2u')] = DataBase_wheels.appmap(self.get('map_ID_CU'),DataBase_wheels.map_from_mi(self.get('map_ID_EC'),self.n('n'),self.n('nn')),self.n('nn')).swaplevel(0,1).set_names([self.n('n'),self.n('nn')])
		self.model.database[self.n('ID_e2t')] = DataBase_wheels.appmap(self.get('ID_e2u'),DataBase_wheels.map_from_mi(self.get('ID_u2t'),self.n('n'),self.n('nn')),self.n('nn')).unique()
		t2i2ai = DataBase_wheels.mi.add_ndmi(self.get('ID_i2t').swaplevel(0,1).set_names([self.n('n'),self.n('nn')]),tech['ID']['Q2P'].set_names([self.n('nn'),self.n('nnn')]))
		self.model.database[self.n('ID_e2ai2i')] = DataBase_wheels.appmap(t2i2ai,DataBase_wheels.map_from_mi(self.get('ID_e2t'),self.n('nn'),self.n('n')),self.n('n')).swaplevel(1,2).set_names([self.n('n'),self.n('nn'),self.n('nnn')])
		self.model.database[self.n('ID_e2ai')] = self.get('ID_e2ai2i').droplevel(self.n('nnn')).unique()

	# ---------------- 1.2: Variables  ------------- #
	def default_var_series(self,var):
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
			return pd.Series(0, index = pd.MultiIndex.from_product([self.get('z'),self.get('ai')]))
		elif var == 'mu':
			return pd.Series(1, index = self.get('ID_map_all'), name=self.n(var))
		elif var == 'sigma':
			return pd.Series(0.01, index = self.get('ID_kno_inp'),name = self.n(var))
		elif var == 'eta':
			return pd.Series(-0.01, index = self.get('ID_kno_out'), name = self.n(var))
		elif var == 'gamma_tau':
			return pd.Series(1, index = self.get('ID_e2t'), name = self.n(var))
		elif var == 'currapp_ID':
			return pd.Series(0.05, index = self.get('ID_e2t'), name = self.n(var))

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

	def initialize_variables_leontief(self):
		db = DataBase.GPM_database()
		qD = (self.get("mu")[self.g("map_ID_Y").rctree_pd(self.g("bra_o_ID_Y"))] * self.get("qS")[self.get("out_ID_Y")].values).droplevel(1) #E and Y quantity
		qD = qD.append((self.g("mu").rctree_pd(self.g("bra_no_ID_Y")) * qD[self.get("kno_no_ID_Y")].values).droplevel(1)) #X under Y quantity
		qD = qD.append((self.get("mu")[self.get("map_ID_EC")] * qD[self.get("kno_ID_EC")].rename_axis("nn")).droplevel(1)) #C quantity
		qD = qD.append((self.get("current_coverages_split") * qD[self.get("kno_ID_EC")].rename_axis("nn")).droplevel(1)) #non-baseline U quantity
		mu = DataBase_wheels.mi.add_mi_series(qD[self.get("bra_ID_TU")], self.g("map_ID_CU").rctree_pd(self.g("bra_ID_TU"))) / \
				qD[self.g("map_ID_CU").rctree_pd(self.g("bra_ID_TU")).droplevel(0).drop_duplicates()] #non baseline U share of C (mu)
		mu = mu.append(pd.Series(1, index=self.g("map_ID_CU").rctree_pd(self.g("bra_ID_BU"))).subtract(mu[self.g("map_ID_CU").rctree_pd(self.g("bra_ID_TU"))].groupby(level=1).sum(), fill_value=0)) #baseline U share of C (mu)
		assert (mu > 0).all()
		qD = qD.append((mu[self.g("map_ID_CU").rctree_pd(self.g("bra_ID_BU"))] * qD[self.get("kno_ID_CU")].rename_axis("nn")).droplevel(1)) #baseline U quantity
		qD = qD.append(DataBase_wheels.appmap_s(qD[self.get("bra_ID_CU")], DataBase_wheels.map_from_mi(self.get("ID_u2t"), "n", "nn")).groupby(by="n").sum()) #tech and baseline tech quantities
		qD = qD.append((self.get("mu")[self.get("map_ID_TX")] * qD[self.get("kno_ID_TX")].rename_axis("nn")).droplevel(1)) #X under techs
		mu = mu.append(DataBase_wheels.mi.add_mi_series(qD[self.get("bra_ID_BU")], self.g("map_ID_BU").rctree_pd(self.g("bra_ID_BU"))) / qD[self.get("kno_ID_BU")].rename_axis("nn")) #baseline tech to U shares (mu)
		#PRICES NOW

	def add_subsets(self, m="ID"):
		self.model.database[self.n("ID_mu_endoincalib")] = (
			self.get("map_ID_EC").append(self.g("map_ID_CU").rctree_pd(self.g("bra_no_ID_BU"))).append(self.get("map_ID_BX"))
			.append(self.get("map_ID_Y_in")).append(self.get("map_ID_Y_out")).append(self.get("map_ID_BU"))
		)
		self.model.database[self.n("ID_mu_exo")] = self.get("map_ID_TX").append(self.get("map_ID_TU")).append(self.g("map_ID_CU").rctree_pd(self.g("bra_ID_BU")))


	# ------------------ 2: Groups  ------------------ #
	def group_conditions(self,group):
		if group == 'g_ID_alwaysexo':
			return [{'sigma': self.g('ID_kno_inp'), 'mu': self.g('ID_mu_exo'), 'eta': self.g('ID_kno_out'), 'phi': self.g('ai'),
			  		 'pM': None, 'PwT': self.g('ID_inp'), 'qS': self.g('ID_out')}]
		elif group == 'g_ID_alwaysendo':
			return [{'PwThat': {'or': [self.g('ID_int'), self.g('ID_inp')]}, 'PbT': self.g('ID_out'), 'pMhat': None,
					'qD': {'and': [{'or': [self.g('ID_int'), self.g('ID_inp')]}, {'not': [{'or': [self.g('kno_ID_EC'), self.g('kno_ID_CU')]}]}]}, 'qsumU': self.g('ID_e2t'),
					 'M0': None}]
		elif group == 'g_ID_endoincalib':
			return [{'mu': self.g('ID_mu_endoincalib')}]
		elif group == 'g_ID_exoincalib':
			return [{'qD': {'or': [self.g('ai'), self.g('kno_ID_EC'), self.g('kno_ID_CU')]}, 'qsumX': self.g('ID_e2ai')}]
		elif group == 'g_ID_minobj_alwaysexo':
			return [{'weight_mu': None, 'mubar': {'and': [self.g('map_ID_CU'), {'not': self.g('bra_ID_BU')}]}}]
		elif group == 'g_ID_minobj_exoincalib':
			return [{'currapp_ID_mod': self.g('ID_e2t')}]
		elif group == 'g_minobj_endoincalib_exoinbaseline':
			return [{'gamma_tau': self.g('ID_e2t')}]
		elif group == 'g_minobj_endoincalib': 
			return [{'minobj': None,'currapp_ID': self.g('ID_e2t')}]

	@property
	def exo_groups(self):
		n = self.model.settings.name+'_'
		gs = OS(['g_ID_alwaysexo','g_ID_endoincalib','g_minobj_endoincalib_exoinbaseline'])
		if self.state == 'ID':
			return {n+g: self.add_group(g,n=n) for g in gs}
		elif self.state == 'ID_calibrate':
			return {n+g: self.add_group(g,n=n) for g in (gs+OS(['g_ID_exoincalib','g_ID_minobj_alwaysexo','g_ID_minobj_exoincalib'])
														   -OS(['g_ID_endoincalib','g_minobj_endoincalib_exoinbaseline']))}
	@property 
	def endo_groups(self):
		n = self.model.settings.name+'_'
		gs = OS(['g_ID_alwaysendo','g_ID_exoincalib'])
		if self.state == 'ID':
			return {n+g: self.add_group(g,n=n) for g in gs}
		elif self.state == 'ID_calibrate':
			return {n+g: self.add_group(g,n=n) for g in (gs+OS(['g_ID_endoincalib','g_minobj_endoincalib_exoinbaseline','g_minobj_endoincalib'])
														   -OS(['g_ID_exoincalib']))}

	@property
	def add_solve(self):
		if self.state == 'EOPcalibrate':
			return f"""solve {self.model.settings.get_conf('name')} using NLP min {self.g('minobj').write()};"""
		else:
			return None

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
