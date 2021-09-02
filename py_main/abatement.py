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
			self.add_sets(tech,kwargs_ns)
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

	def add_aliases(self,list_of_tuples,ns={}):
		self.model.database.update_alias(pd.MultiIndex.from_tuples(list_of_tuples))
		self.ns.update({k[1]:df(k[1],ns) for k in list_of_tuples}) # add to namespace

	def namespace_local_sets(self,nt):
		"""create namespace for each tree by copying attributes."""
		return {tree: {attr: nt.trees[tree].__dict__[attr] for attr in nt.trees[tree].__dict__ if attr not in set(['tree','database']).union(nt.prune_trees)} for tree in nt.trees}

	def namespace_global_variables(self,kwargs):
		"""create global namespace for variables used in partial equilibrium model. kwargs modify the names."""
		return {varname: df(varname,kwargs) for varname in self.default_variables}

	@property
	def default_variables(self):
		return ('PbT','PwT','PwThat','pM','pMhat','qD','qS','qsumU','qsumX','M0','M','phi','os','mu','sigma','eta','gamma_tau','currapp_ID')

	def add_sets(self,tech,kwargs):
		""" Define global 'levels' mappings and subsets, e.g. all technology goods across nesting trees. """
		self.ns.update({s: df(s,kwargs) for s in ['ID_'+ss for ss in ['t_all','ai']]})
		self.ns.update({s: df(s,kwargs) for s in ['ID_'+ss for ss in ['i2t','u2t','e2u','e2t','e2ai2i','e2ai','mu_endoincalib','mu_exo']]})
		# level sets:
		self.model.database[self.n('ID_t_all')] = self.get('kno_ID_TX').union(self.get('kno_ID_BX'))
		self.model.database[self.n('ID_i2ai')] = tech['ID']['Q2P']
		self.model.database[self.n('ai')] = tech['ID']['Q2P'].levels[1].rename(self.n('n'))
		# Mappings:
		self.model.database[self.n('ID_i2t')] = self.get('ID_map_all')[(self.get('ID_map_all').get_level_values(self.n('n')).isin(self.get('ID_inp'))) & (self.get('ID_map_all').get_level_values(self.n('nn')).isin(self.get('ID_t_all')))]
		self.model.database[self.n('ID_u2t')] = self.get('ID_map_all')[(self.get('ID_map_all').get_level_values(self.n('n')).isin(self.get('bra_ID_CU'))) & (self.get('ID_map_all').get_level_values(self.n('nn')).isin(self.get('ID_t_all')))]
		self.model.database[self.n('ID_e2u')] = DataBase_wheels.appmap(self.get('map_ID_CU'),DataBase_wheels.map_from_mi(self.get('map_ID_EC'),self.n('n'),self.n('nn')),self.n('nn')).swaplevel(0,1).set_names([self.n('n'),self.n('nn')])
		self.model.database[self.n('ID_e2t')] = DataBase_wheels.appmap(self.get('ID_e2u'),DataBase_wheels.map_from_mi(self.get('ID_u2t'),self.n('n'),self.n('nn')),self.n('nn')).unique()
		t2i2ai = DataBase_wheels.mi.add_ndmi(self.get('ID_i2t').swaplevel(0,1).set_names([self.n('n'),self.n('nn')]),tech['ID']['Q2P'].set_names([self.n('nn'),self.n('nnn')]))
		self.model.database[self.n('ID_e2ai2i')] = DataBase_wheels.appmap(t2i2ai,DataBase_wheels.map_from_mi(self.get('ID_e2t'),self.n('nn'),self.n('n')),self.n('n')).swaplevel(1,2).set_names([self.n('n'),self.n('nn'),self.n('nnn')])
		self.model.database[self.n('ID_e2ai')] = self.get('ID_e2ai2i').droplevel(self.n('nnn')).unique()
		self.model.database[self.n('ID_mu_endoincalib')] = pd.MultiIndex.from_tuples(OS.union(*[s.tolist() for s in (self.get('map_ID_EC'), self.g('map_ID_CU').rctree_pd(self.g('bra_no_ID_BU')), self.get('map_ID_BX'), self.get('map_ID_Y'), self.get('map_ID_BU'))]), names = [self.n('n'),self.n('nn')])
		self.model.database[self.n('ID_mu_exo')] = pd.MultiIndex.from_tuples(OS.union(*[s.tolist() for s in (self.get('map_ID_TX'), self.get('map_ID_TU'), self.g('map_ID_CU').rctree_pd(self.g('bra_ID_BU')))]), names = [self.n('n'),self.n('nn')])

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
		elif var == 'os':
			return pd.Series(0.5, index = self.get('ID_e2t'), name = self.n(var))
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

	# ------------------ 2: Groups  ------------------ #
	def group_conditions(self,group):
		if group == 'g_ID_alwaysexo':
			return [{'sigma': self.g('ID_kno_inp'), 'mu': self.g('ID_mu_exo'), 'eta': self.g('ID_kno_out'), 'phi': self.g('ai'),
			  		 'pM': None, 'PwT': self.g('ID_inp'), 'qS': self.g('ID_out')}]
		elif group == 'g_ID_alwaysendo':
			return [{'PwThat': {'or': [self.g('ID_int'), self.g('ID_inp')]}, 'PbT': self.g('ID_out'), 'pMhat': None,
					'qD': {'and': [{'or': [self.g('ID_int'), self.g('ID_inp')]}, {'not': [{'or': [self.g('kno_ID_EC'), self.g('kno_ID_CU')]}]}]}, 'qsumU': self.g('ID_e2t'), 'os': self.g('ID_e2t'),
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

	# ------------------ 3: Special solve statements  ------------------ #
	@property
	def add_solve(self):
		if self.state == 'EOPcalibrate':
			return f"""solve {self.model.settings.get_conf('name')} using NLP min {self.g('minobj').write()};"""
		else:
			return None

	# ------------------------ 4: Blocks  ----------------------- #
	@property
	def blocktext(self):
		blocks = {**{f"M_{tree}": self.eqtext(tree) for tree in self.ns_local},
				  **{f"M_{self.model.settings.name}_ID_sum": self.init_ID_sum(),
				     f"M_{self.model.settings.name}_ID_Em": self.init_ID_emissions(),
				     f"M_{self.model.settings.name}_ID_agg": self.init_agg()}}
		return blocks

	@property
	def mblocks(self):
		return set([f"M_{tree}" for tree in self.ns_local]+
				   [f"M_{self.model.settings.name}_"+m for m in ('ID_sum','ID_Em','ID_agg')])

	def init_ID_sum(self):
		s = getattr(gams_abatement,'ID_sum')()
		s.add_symbols(self.model.database,self.ns)
		s.add_conditions()
		return s.run(self.model.settings.name)
	def init_ID_emissions(self):
		s = getattr(gams_abatement,'ID_emissions')()
		s.add_symbols(self.model.database,self.ns)
		s.add_conditions()
		return s.run(self.model.settings.name)
	def init_agg(self):
		s = getattr(gams_abatement,'aggregates')(state=self.state)
		s.add_symbols(self.model.database,self.ns)
		s.add_conditions()
		return s.run(self.model.settings.name)
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
