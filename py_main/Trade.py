from gmspython import *
from Production import pr_static
import gams_trade

class trade_dynamic(gmspython):
	def __init__(self,db=None,version='Armington_v1',pickle_path=None,work_folder=None,gs_v='gs_v1',gs_vals = {},kwargs_ns={},kwargs_st = {},**kwargs_gs):
		databases = [DataBase.GPM_database()] if db is None else [db]
		super().__init__(module='trade_dynamic',pickle_path=pickle_path,work_folder=work_folder,databases=databases,**kwargs_gs)
		if pickle_path is None:
			self.version = version
			self.ns = {**self.ns, **self.namespace_global_sets(kwargs_ns), **self.namespace_global_variables(kwargs_ns)}
			self.ns_local = {**self.ns_local, **self.namespace_local_sets(kwargs_ns)} # per default only one tree.
			self.update_alias()
			self.sector = dfelse('sector',False,kwargs_st)
			self.add_global_settings(gs_v,kwargs_ns=kwargs_ns,kwargs_vals=gs_vals)
			if 'ss' in kwargs_st:
				self.sector = True

	def namespace_global_sets(self,kwargs):
		""" retrieve attributes from global tree"""
		return {setname: df(setname,kwargs) for setname in ('n','nn','nnn','n_for','s','s_for','n_prod','sfor_ndom','sfor_nfor','dom2for')}

	def namespace_global_variables(self,kwargs):
		"""create global namespace for variables used in partial equilibrium model. kwargs modify the names."""
		return {varname: df(varname,kwargs) for varname in self.default_variables}

	def namespace_local_sets(self,kwargs,tree_name='trade'):
		""" Create 'local' namespace """
		return {tree_name: {setname: df(setname,kwargs) for setname in ['dom2for','sfor_ndom']}}

	@property
	def default_variables(self):
		return ('PwT','Peq','qD','phi','sigma')

	# --- 			Initialize from GE data and simple data --- #
	def add_sets_from_GE(self,GE):
		for sym in ('n','n_for','s','s_for','n_prod','sfor_ndom','sfor_nfor'):
			self.model.database[self.n(sym)] = GE[self.n(sym)]

	def update_alias(self):
		self.model.database.update_alias(pd.MultiIndex.from_tuples([(self.n('n'),self.n('nn')),(self.n('n'),self.n('nnn'))]))

	# ---			2: Initialize variables			--- #
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

	def default_var_series(self,var):
		if var=='PwT':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('sfor_ndom'),self.get('txE')), name = self.n(var))
		elif var == 'Peq':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('n_for'),self.get('txE')), name = self.n(var))
		elif var == 'qD':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('sfor_ndom'),self.get('txE')), name = self.n(var))
		elif var == 'phi':
			return pd.Series(1, index = self.get('sfor_ndom'), name=self.n(var))
		elif var == 'sigma':
			return pd.Series(5, index = self.get('sfor_ndom'), name = self.n(var))

	def ivfs(self,static,variables=['qD','PwT','Peq'],merge=True):
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
			return {'sigma': self.g('sfor_ndom')}
		elif group == 'g_tech_endo':
			return {'phi': self.g('sfor_ndom')}
		elif group == 'g_exovars':
			return {'PwT': self.g('sfor_ndom'), 'Peq': self.g('n_for')}
		elif group == 'g_calib_exo':
			return {'qD': {'and': [self.g('sfor_ndom'), self.g('t0')]}}
		elif group == 'g_endovars':
			return {'qD': {'and': [self.g('sfor_ndom'), self.g('tx0E')]}}
		elif group in self.gog:
			return self.gog_conditions(group)

	@property
	def gog(self):
		return ['g_tech','g_endo_vars','g_exo_vars']

	def group_of_groups(self,group,n=''):
		if group == 'g_tech':
			return {'g_tech_exo': n+'g_tech_exo', 'g_tech_endo': n+'g_tech_endo'}
		elif group == 'g_exo_vars':
			return {'g_exovars': n+'g_exovars'}
		elif group == 'g_endo_vars':
			return {'g_endovars': n+'g_endovars','g_calib_exo': n+'g_calib_exo'}

	@property
	def exo_groups(self):
		""" Collect exogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ('g_tech','g_exo_vars')}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_tech_exo','g_exovars','g_calib_exo')}

	@property
	def endo_groups(self):
		""" Collect endogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ['g_endo_vars']}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_endovars','g_tech_endo')}

	@property 
	def sub_groups(self):
		""" Collect groups that are subgroups of other groups; these are not written to list of exogenous/endogenous groups. """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {**{n+g: self.add_group(g,n=n) for g in ('g_tech_endo','g_tech_exo','g_exovars','g_calib_exo','g_endovars')}}
		elif self.state in ('SC','DC'):
			return {}

	# --- 		4: Define blocks 		--- #
	@property
	def blocktext(self):
		return {f"M_{tree}": self.eqtext(tree) for tree in self.ns_local}

	@property
	def mblocks(self):
		return set([f"M_{tree}" for tree in self.ns_local])

	def eqtext(self,tree_name):
		tree = self.ns_local[tree_name]
		gams_class = getattr(gams_trade,self.version)(version=self.version)
		gams_class.add_symbols(self.model.database,tree,ns_global=self.ns,dynamic=True)
		gams_class.add_conditions(self.model.database,tree,dynamic=True)
		return gams_class.run(tree_name)
