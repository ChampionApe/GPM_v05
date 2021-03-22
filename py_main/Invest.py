from gmspython import *
from Production import pr_static
import gams_production

class inv_dynamic(gmspython):
	def __init__(self,nt=None,pickle_path=None,work_folder=None,gs_v='gs_v1',pw='pricewedge',gs_vals={},kwargs_ns={},kwargs_st = {},**kwargs_gs):
		databases = None if nt is None else [nt.database.copy()]
		super().__init__(module='inv_dynamic',pickle_path=pickle_path,work_folder=work_folder,databases=databases,**kwargs_gs)
		if pickle_path is None:
			self.version = nt.version
			self.ns = {**self.ns, **self.namespace_global_sets(nt,kwargs_ns), **self.namespace_global_variables(kwargs_ns)}
			self.ns_local = {**self.ns_local, **self.namespace_local_sets(nt)}
			self.sector = dfelse('sector',False,kwargs_st)
			self.add_global_settings(gs_v,kwargs_ns=kwargs_ns,kwargs_vals=gs_vals,dynamic=True)
			self.pw = getattr(gams_production,pw)()
			for tree in nt.trees.values():
				DataBase.GPM_database.merge_dbs(self.model.database,tree.database,'first')
			if 'ss' in kwargs_st:
				self.sector = True
				self.ns['ss'] = 's_inv' if 'ss' not in kwargs_ns else kwargs_ns['ss']
				self.model.database[self.ns['ss']] = self.get('s')[self.get('s').isin(kwargs_st['ss'])]
			self.add_default_subsets()

	# ---			1: Retrieve namespace from nesting trees		--- #
	def namespace_global_sets(self,nt,kwargs):
		""" retrieve attributes from global tree"""
		std_sets = {setname: getattr(nt,setname) for setname in ('n','nn','nnn','inp','out','int','wT','map_all','kno_out','kno_inp','s','s_inv') if setname in nt.__dict__}
		std_sets['PwT_dom'] = nt.PwT_dom if self.version=='Q2P' else nt.wT
		std_sets['exo_mu'] = df('exo_mu',kwargs)
		std_sets['endo_PbT'] = df('endo_PbT',kwargs)
		std_sets['n_out'] = df('n_out',kwargs)
		return std_sets

	def add_default_subsets(self):
		self.model.database[self.n('n_out')] = self.get('out').levels[-1] if isinstance(self.get('out'),pd.MultiIndex) else self.get('out')

	def namespace_global_variables(self,kwargs):
		"""create global namespace for variables used in partial equilibrium model. kwargs modify the names."""
		return {varname: df(varname,kwargs) for varname in self.default_variables}

	@property
	def default_variables(self):
		return ('PwT','PbT','qS','qD','mu','sigma','eta','Peq','markup','tauS','tauLump')

	def namespace_local_sets(self,nt):
		"""create namespace for each tree, by copying attributes."""
		return {tree: {attr: nt.trees[tree].__dict__[attr] for attr in nt.trees[tree].__dict__ if attr not in set(['tree','database']).union(nt.prune_trees)} for tree in nt.trees}

	# ---			2: Initialize methods			--- #
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

	# ---			2.1: Add time to the model durables			--- #

	def default_var_series(self,var):
		if var=='PbT':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('out'),self.get('txE')), name = self.n(var))
		elif var == 'PwT':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('PwT_dom'),self.get('txE')), name = self.n(var))
		elif var == 'qS':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('out'),self.get('txE')), name = self.n(var))
		elif var == 'qD':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('wT'),self.get('txE')), name = self.n(var))
		elif var == 'Peq':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('n_out'),self.get('txE')), name = self.n(var))
		elif var == 'markup':
			return pd.Series(0, index = self.get('out'), name = self.n(var))
		elif var == 'tauS':
			return pd.Series(0, index = DataBase_wheels.prepend_index_with_1dindex(self.get('out'),self.get('txE')), name = self.n(var))
		elif var == 'tauLump':
			index = self.get('txE') if self.sector is False else DataBase_wheels.prepend_index_with_1dindex(self.get('s_inv'),self.get('txE'))
			return pd.Series(0, index = index, name=self.n(var))
		elif var == 'mu':
			return pd.Series(1, index = self.get('map_all'), name=self.n(var))
		elif var == 'sigma':
			return pd.Series(0.5, index = self.get('kno_inp'), name = self.n(var))
		elif var == 'eta':
			return pd.Series(1, index = self.get('kno_out'), name = self.n(var))

	def ivfs(self,static,variables=['qD','qS','PwT','PbT','Peq','tauS','tauLump'],merge=True):
		""" initialize variables from database w. static version """ 
		for var in variables:
			add_var = pr_static.add_t_to_variable(static.get(self.ns[var]),self.get('txE'))
			if merge is True and self.ns[var] in self.model.database.symbols:
				self.model.database[self.ns[var]] = add_var.combine_first(self.get(var))
			else:
				self.model.database[self.ns[var]] = add_var

	# ---			3: Define groups	 		--- #
	def add_group(self,group,n=None):
		if group in self.gog:
			return self.group_of_groups(group,n=n)
		else:
			return self.define_group(self.group_conditions(group))

	def define_group(self,group):
		return {self.n(var): {'conditions': self.g(var).rctree_gams(group[var]), 'text': self.g(var).write()} for var in group}	

	def group_conditions(self,group):
		if group == 'g_tech_exo':
			return {'sigma': self.g('kno_inp'), 'eta': self.g('kno_out'), 'mu': self.g('exo_mu')}
		elif group == 'g_tech_endo':
			return {'mu': {'and': [self.g('map_all'),{'not': self.g('exo_mu')}]}, 'markup': self.g('out')}
		elif group == 'gvars_endo':
			return {'PbT': self.g('endo_PbT'), 'PwT': self.g('int'), 'qD': {'and': [self.g('wT'), self.g('tx0')]},'Peq': {'and': [self.g('n_out'),self.g('tx0E')]}}
		elif group == 'gvars_exo':
			return {'qS': self.g('out'), 'PwT': self.g('inp'),'tauS': self.g('out'), 'tauLump': None if self.sector is False else self.g('s_inv')}
		elif group == 'g_calib_exo':
			return {'qD': {'and': [self.g('inp'), self.g('t0')]}, 'PbT': {'and': [self.g('t0'),self.g('out'),{'not': self.g('endo_PbT')}]},'Peq': {'and': [self.g('t0'), self.g('n_out')]}}
		elif group in self.gog:
			return self.gog_conditions(group)

	@property
	def gog(self):
		return ['g_tech','g_vars_exo','g_vars_endo']

	def group_of_groups(self,group,n=''):
		if group == 'g_tech':
			return {'g_tech_exo': n+'g_tech_exo', 'g_tech_endo': n+'g_tech_endo'}
		elif group == 'g_vars_exo':
			return {'gvars_exo': n+'gvars_exo'}
		elif group == 'g_vars_endo':
			return {'gvars_endo': n+'gvars_endo','g_calib_exo': n+'g_calib_exo'}

	@property
	def exo_groups(self):
		""" Collect exogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ('g_tech','g_vars_exo')}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_tech_exo','gvars_exo','g_calib_exo')}

	@property
	def endo_groups(self):
		""" Collect endogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ['g_vars_endo']}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_tech_endo','gvars_endo')}

	@property 
	def sub_groups(self):
		""" Collect groups that are subgroups of other groups; these are not written to list of exogenous/endogenous groups. """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ('g_tech_exo','g_tech_endo','gvars_exo','gvars_endo','g_calib_exo')}
		elif self.state in ('SC','DC'):
			return {}

	# --- 		4: Define blocks 		--- #
	@property
	def blocktext(self):
		return {**{f"M_{tree}": self.eqtext(tree) for tree in self.ns_local}, **{f"M_{self.model.settings.name}_pw":self.init_pw()}}

	@property
	def mblocks(self):
		return set([f"M_{tree}" for tree in self.ns_local]+[f"M_{self.model.settings.name}_pw"])

	def init_pw(self):
		self.pw.add_symbols(self.model.database,self.ns,dynamic=True)
		self.pw.add_conditions(self.model.database,dynamic=True)
		return self.pw.run(self.model.settings.name)

	def eqtext(self,tree_name):
		tree = self.ns_local[tree_name]
		gams_class = getattr(gams_production,tree['type_f'])(version=tree['version'])
		gams_class.add_symbols(self.model.database,tree,ns_global=self.ns,dynamic=True)
		gams_class.add_conditions(self.model.database,tree,dynamic=True)
		return gams_class.run(tree_name)

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
					endo_pbt = endo_pbt.insert(0,z.droplevel(self.n('nn'))[0])
					exo_mu = exo_mu.insert(0,z[0])
				exo_mu = exo_mu.union(map_[~(map_.droplevel(self.n('nn')).isin(tree_out))])
		return endo_pbt,exo_mu

class itoryD(gmspython):
	""" only dynamic multisector version is available. """ 
	def __init__(self,pickle_path=None,databases=None,work_folder=None,itory_type='itoryD_v1',gs_v='gs_v1',gs_vals = {},kwargs_ns={},**kwargs_gs):
		databases = [DataBase.GPM_database()] if databases is None else databases
		super().__init__(module='itoryD',pickle_path=pickle_path,work_folder=work_folder,databases=databases,**kwargs_gs)
		if pickle_path is None:
			self.ns = {**self.ns, **self.namespace_global_sets(kwargs_ns), **self.namespace_global_variables(kwargs_ns)}
			self.add_global_settings(gs_v,kwargs_ns=kwargs_ns,kwargs_vals=gs_vals)
			self.itory = getattr(gams_production,itory_type)(**kwargs_ns)

	# ---			1: Retrieve namespace from nesting trees		--- #
	def namespace_global_sets(self,kwargs):
		""" retrieve attributes from global tree"""
		return {k:df(k,kwargs) for k in ('n','s','itoryD')}

	def namespace_global_variables(self,kwargs):
		"""create global namespace for variables used in partial equilibrium model. kwargs modify the names."""
		return {varname: df(varname,kwargs) for varname in self.default_variables}

	@property
	def default_variables(self):
		return ['qD']

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
		self.initialize_itory()

	def initialize_itory(self):
		self.itory.add_symbols(self.model.database,self.ns)
		self.itory.add_conditions(self.model.database,self.ns)
		self.ns = {**self.ns,**self.itory.ns}

	def default_var_series(self,var):
		if var =='qD':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('itoryD'), self.get('txE')), name=self.n(var))
		elif var in self.itory.ns:
			return self.itory.default_var_series(var)

	# ---			3: Define groups	 		--- #
	def add_group(self,group,n=None):
		if group in self.gog:
			return self.group_of_groups(group,n=n)
		else:
			return self.define_group(self.group_conditions(group))

	def define_group(self,group):
		return {self.n(var): {'conditions': self.g(var).rctree_gams(group[var]), 'text': self.g(var).write()} for var in group}	
		
	def group_conditions(self,group):
		if group == 'g_exo':
			return {'qD': {'and': [self.g('t0'), self.g('itoryD')]}}
		elif group == 'g_endo':
			return {'qD': {'and': [self.g('tx0E'), self.g('itoryD')]}}
		elif group in self.gog:
			return self.gog_conditions(group)
		else:
			return self.itory.group_conditions(group)

	@property
	def gog(self):
		return self.itory.gog

	def group_of_groups(self,group,n=''):
		pass

	@property
	def exo_groups(self):
		""" Collect exogenous groups """
		n = self.model.settings.name+'_'
		return {**{n+g: self.add_group(g,n=n) for g in ['g_exo']},**self.itory.exo_groups(n)}

	@property
	def endo_groups(self):
		""" Collect endogenous groups """
		n = self.model.settings.name+'_'
		return {**{n+g: self.add_group(g,n=n) for g in ['g_endo']},**self.itory.endo_groups(n)}

	@property 
	def sub_groups(self):
		return {}

	# --- 		4: Define blocks 		--- #
	@property
	def blocktext(self):
		return {f"M_{self.model.settings.name}": self.itory.run(self.model.settings.name)}

	@property
	def mblocks(self):
		return set([f"M_{self.model.settings.name}"])
