from gmspython import *
import gams_hh,global_settings

class hh_static(gmspython):
	""" nested ces-type nesting trees. This version builds a relatively simple structure."""
	def __init__(self,nt=None,pickle_path=None,work_folder=None,kwargs_ns={},gs_v='gs_v1',**kwargs_gs):
		databases = None if nt is None else [nt.database.copy()]
		super().__init__(module='hh_static',pickle_path=pickle_path,work_folder=work_folder,databases=databases,**kwargs_gs)
		if pickle_path is None:
			self.version = nt.version
			self.ns = {**self.ns, **self.namespace_global_sets(nt,kwargs_ns), **self.namespace_global_variables(kwargs_ns)}
			self.ns_local = {**self.ns_local, **self.namespace_local_sets(nt)}
			self.sector = False
			self.add_global_settings(gs_v,kwargs_ns=kwargs_ns,dynamic=False)
			self.add_default_subsets()

	# ---			1: Retrieve namespace from nesting trees, set up default objects		--- #
	def namespace_global_sets(self,nt,kwargs):
		""" retrieve attributes from global tree"""
		std_sets = {setname: getattr(nt,setname) for setname in ('n','nn','nnn','inp','out','int','int_temp','exo','kno','top','map_all','s') if setname in nt.__dict__}
		[std_sets.__setitem__(k,df(k,kwargs)) for k in ('endo_mu','s_HH','fg_HH')];
		return std_sets

	@property
	def hh_sectors(self):
		""" read the household sectors from the nesting tree.""" 
		return None if not isinstance(self.get('inp'),pd.MultiIndex) else self.get('inp').union(self.get('int')).union(self.get('out')).levels[0]

	def add_default_subsets(self):
		self.model.database[self.n('endo_mu')] = self.get('map_all').droplevel(self.n('nn'))[self.get('map_all').droplevel(self.n('nn')).isin(self.get('inp').union(self.get('out')))]		
		self.model.database[self.n('s_HH')] = self.hh_sectors
		self.model.database[self.n('fg_HH')] = self.get('out').levels[-1]

	def namespace_global_variables(self,kwargs):
		"""create global namespace for variables used in partial equilibrium model. kwargs modify the names."""
		return {varname: df(varname,kwargs) for varname in self.default_variables}

	@property
	def default_variables(self):
		""" sp is an auxliary variable used to compute the household budget.""" 
		return ('PbT','PwT','qS','qD','mu','sigma','Peq','tauS','tauLump','sp')

	def namespace_local_sets(self,nt):
		"""create namespace for each tree, by copying attributes."""
		return {tree: {attr: nt.trees[tree].__dict__[attr] for attr in nt.trees[tree].__dict__ if attr not in ['tree','database']} for tree in nt.trees}

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

	def compute_sp(self,db=None,names={}):
		""" compute the savings variable from state of other variables. """
		ss_o, ss_i = self.g('out'), self.g('inp')
		if db is None:
			var = {v: self.g(v) for v in ('qS','qD','PbT','PwT','tauLump')}
		else:
			var = {v: db[df(self.n(v), names)] for v in ('qS','qD','PbT','PwT','tauLump')}
		return pd.Series((var['qS'].rctree_pd(ss_o)*var['PbT'].rctree_pd(ss_o)).groupby([d for d in var['qS'].index.names if d != self.n('n')]).sum()
						-(var['qD'].rctree_pd(ss_i)*var['PwT'].rctree_pd(ss_i)).groupby([d for d in var['qD'].index.names if d != self.n('n')]).sum()
						-var['tauLump'].rctree_pd(self.hh_sectors))

	def default_var_series(self,var):
		if var=='PbT':
			return pd.Series(1, index = self.get('out'), name = self.n(var))
		elif var=='PwT':
			return pd.Series(1, index = self.get('inp').union(self.get('int')), name = self.n(var))
		elif var == 'qS':
			return pd.Series(1, index = self.get('out'), name = self.n(var))
		elif var == 'qD':
			return pd.Series(1, index = self.get('inp').union(self.get('int')), name = self.n(var))
		elif var == 'Peq':
			return pd.Series(1, index = self.get('fg_HH'), name = self.n(var))
		elif var == 'mu':
			return pd.Series(1, index = self.get('map_all'), name=self.n(var))
		elif var == 'sigma':
			return pd.Series(0.5, index = self.get('kno'), name = self.n(var))
		elif var == 'tauS':
			return pd.Series(0, index = self.get('out'), name = self.n(var))
		elif var == 'tauLump':
			return 0 if self.hh_sectors is None else pd.Series(0, index = self.hh_sectors, name = self.n(var))
		elif var == 'sp':
			if self.hh_sectors is not None:
				return self.compute_sp()
			else:
				return 0

	# ---			3: Define groups	 		--- #
	def add_group(self,group,n=None):
		if group in self.gog:
			return self.group_of_groups(group,n=n)
		else:
			return self.define_group(self.group_conditions(group))

	def define_group(self,group):
		return {self.n(var): {'conditions': self.g(var).rctree_gams(group[var]), 'text': self.g(var).write()} for var in group}	

	@property
	def gog(self):
		return ['g_tech']

	def group_of_groups(self,group,n=''):
		if group == 'g_tech':
			return {'g_tech_exo': n+'g_tech_exo', 'g_tech_endo': n+'g_tech_endo'}

	def group_conditions(self,group):
		if group == 'g_tech_exo':
			return {'sigma': self.g('kno'), 'mu': {'and': [self.g('map_all'), {'not': self.g('endo_mu')}]}}
		elif group == 'g_tech_endo':
			return {'mu': self.g('endo_mu')}
		elif group == 'g_endovars':
			return {'PwT': {'and': [self.g('int'), {'not':self.g('top')}]},'PbT': self.g('out'),'qD': self.g('int')}
		elif group == 'g_exovars':
			return {'PwT': self.g('inp'), 'Peq': self.g('fg_HH'), 'qD': {'and': [self.g('inp'),self.g('exo')]}, 'qS': {'and': [self.g('out'), self.g('exo')]},'tauS': self.g('out'),
					'tauLump': None if self.hh_sectors is None else self.g('s_HH')}
		elif group == 'g_calib_exo':
			return {'qD': {'and': [self.g('inp'), {'not': self.g('exo')}]}, 'qS': {'and': [self.g('out'),{'not': self.g('exo')}]}, 'PwT': self.g('top')} 
		elif group is 'g_savings':
			return {'sp': self.g('s_HH')}
		elif group in self.gog:
			return self.gog_conditions(group)

	@property
	def exo_groups(self):
		""" Collect exogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ('g_tech','g_exovars','g_savings')}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_tech_exo','g_exovars','g_calib_exo')}

	@property
	def endo_groups(self):
		""" Collect endogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ('g_endovars','g_calib_exo')}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_endovars','g_tech_endo','g_savings')}

	@property 
	def sub_groups(self):
		""" Collect groups that are subgroups of other groups; these are not written to list of exogenous/endogenous groups. """
		n = self.model.settings.name+'_'
		return {n+g: self.add_group(g,n=n) for g in ('g_tech_endo','g_tech_exo')}

	# --- 		4: Define blocks 		--- #
	@property
	def blocktext(self):
		return {**{f"M_{tree}": self.eqtext(tree) for tree in self.ns_local},**{f"M_bdgt_{self.model.settings.name}":self.eqtext_budget()}}

	@property
	def mblocks(self):
		return set([f"M_{tree}" for tree in self.ns_local]+[f"M_bdgt_{self.model.settings.name}"])

	def eqtext(self,tree_name):
		tree = self.ns_local[tree_name]
		gams_class = getattr(gams_hh,tree['type_f'])(version=tree['version'])
		gams_class.add_symbols(self.model.database,tree,ns_global=self.ns)
		gams_class.add_conditions(self.model.database,tree)
		return gams_class.run(tree_name)

	def eqtext_budget(self):
		gams_class = getattr(gams_hh,'budget')()
		gams_class.add_symbols(self.model.database,self.ns,sector=self.hh_sectors)
		gams_class.add_conditions(sector=self.hh_sectors)
		return gams_class.run(self.model.settings.name)

	@staticmethod
	def add_t_to_variable(var,tindex):
		if tindex.name not in var.index.names:
			return pd.concat({i: var for i in tindex},names=tindex.names)
		else:
			return var

class hh_dynamic(gmspython):
	def __init__(self,nt=None,dyn='ramsey',pickle_path=None,work_folder=None,gs_v='gs_v1',gs_vals = {},kwargs_ns={},kwargs_st = {},**kwargs_gs):
		databases = None if nt is None else [nt.database.copy()]
		super().__init__(module='hh_dynamic',pickle_path=pickle_path,work_folder=work_folder,databases=databases,**kwargs_gs)
		if pickle_path is None:
			self.version = nt.version
			self.ns = {**self.ns, **self.namespace_global_sets(nt,kwargs_ns), **self.namespace_global_variables(kwargs_ns)}
			self.ns_local = {**self.ns_local, **self.namespace_local_sets(nt)}
			self.sector = dfelse('sector',False,kwargs_st)
			self.add_global_settings(gs_v,kwargs_ns=kwargs_ns,kwargs_vals=gs_vals,dynamic=True)
			self.dyn = getattr(gams_hh,dyn)(**kwargs_ns)
			self.add_default_subsets()

	# ---			1: Retrieve namespace from nesting trees, set up default objects		--- #
	def namespace_global_sets(self,nt,kwargs):
		""" retrieve attributes from global tree"""
		std_sets = {setname: getattr(nt,setname) for setname in ('n','nn','nnn','inp','out','int','int_temp','exo','kno','top','map_all','s') if setname in nt.__dict__}
		[std_sets.__setitem__(k,df(k,kwargs)) for k in ('endo_mu','s_HH','fg_HH')];
		return std_sets

	@property
	def hh_sectors(self):
		""" read the household sectors from the nesting tree.""" 
		return None if not isinstance(self.get('inp'),pd.MultiIndex) else self.get('inp').union(self.get('int')).union(self.get('out')).levels[0]

	@property 
	def savings_domain(self):
		static = self.get('svngs') if self.hh_sectors is None else DataBase_wheels.prepend_index_with_1dindex(self.get('svngs'),self.hh_sectors)
		return DataBase_wheels.prepend_index_with_1dindex(static,self.get('t'))

	def add_default_subsets(self):
		self.model.database[self.n('endo_mu')] = self.get('map_all').droplevel(self.n('nn'))[self.get('map_all').droplevel(self.n('nn')).isin(self.get('inp').union(self.get('out')))]		
		self.model.database[self.n('s_HH')] = self.hh_sectors
		self.model.database[self.n('fg_HH')] = self.get('out').levels[-1]
		self.adjust_endo_mu()
		self.dyn.sector = self.ns['s_HH']

	def adjust_endo_mu(self):
		if self.hh_sectors is None:
			self.model.database[self.n('endo_mu')] = self.get('endo_mu').drop(self.get('endo_mu')[0])
		else:
			self.model.database[self.n('endo_mu')] = self.get('endo_mu').drop([self.get('endo_mu')[self.get('endo_mu').get_level_values(self.n('s'))==s][0] for s in self.get('s_HH')])

	def namespace_global_variables(self,kwargs):
		"""create global namespace for variables used in partial equilibrium model. kwargs modify the names."""
		return {varname: df(varname,kwargs) for varname in self.default_variables}

	@property
	def default_variables(self):
		return ('PbT','PwT','Peq','qS','qD','vD','mu','sigma','irate','crra','disc','hh_tvc','tauS','tauLump','sp')

	def namespace_local_sets(self,nt):
		"""create namespace for each tree, by copying attributes."""
		return {tree: {attr: nt.trees[tree].__dict__[attr] for attr in nt.trees[tree].__dict__ if attr not in ['tree','database']} for tree in nt.trees}

	# ---			2: Add time 			--- #
	def add_svngs(self,kwargs_ns={},**kwargs):
		""" Add the time index and durables to model. """ 
		self.add_svngs_to_namespace(**kwargs_ns)
		self.add_savings_to_database(**kwargs)

	def add_svngs_to_namespace(self,**kwargs):
		"""" add to namespace """
		self.ns.update({set_: df(set_,kwargs) for set_ in self.svngs_ns})

	@property
	def svngs_ns(self):
		return ['svngs']

	def add_savings_to_database(self,dur=['svngs'],**kwargs):
		self.add_savings_sets_to_database(dur)
		for var in self.default_variables:
			if self.ns[var] not in self.model.database.symbols:
				self.model.database[self.ns[var]] = self.default_var_series(var)

	def add_savings_sets_to_database(self,dur):
		""" Add sets/subsets to database."""
		self.model.database[self.ns['svngs']] = pd.Index(dur,name=self.ns['n'])
		self.model.database[self.ns['n']] = self.get('n').union(self.get('svngs')).unique()

	def ivfs(self,static,variables=['qS','qD','PbT','PwT','Peq','sp','tauS','tauLump'],merge=True):
		""" initialize variables from database w. static version """ 
		for var in variables:
			add_var = hh_static.add_t_to_variable(static.get(self.ns[var]),self.get('txE'))
			if merge is True and self.ns[var] in self.model.database.symbols:
				self.model.database[self.ns[var]] = add_var.combine_first(self.get(var))
			else:
				self.model.database[self.ns[var]] = add_var

	# ---			3: Initialize variables			--- #
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
		self.initialize_dyn()

	def compute_sp(self,db=None,names={}):
		""" compute the savings variable from state of other variables. """
		ss_o, ss_i = self.g('out'), self.g('inp')
		if db is None:
			var = {v: self.g(v) for v in ('qS','qD','PbT','PwT','tauLump')}
		else:
			var = {v: db[df(self.n(v), names)] for v in ('qS','qD','PbT','PwT','tauLump')}
		return pd.Series((var['qS'].rctree_pd(ss_o)*var['PbT'].rctree_pd(ss_o)).groupby([d for d in var['qS'].index.names if d != self.n('n')]).sum()
						-(var['qD'].rctree_pd(ss_i)*var['PwT'].rctree_pd(ss_i)).groupby([d for d in var['qD'].index.names if d != self.n('n')]).sum()
						-var['tauLump'].rctree_pd(self.hh_sectors))

	def initialize_dyn(self):
		self.dyn.add_symbols(self.model.database,self.ns)
		self.dyn.add_conditions(self.model.database,self.ns)

	def default_var_series(self,var):
		if var=='PbT':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('out'),self.get('txE')),name =self.n(var))
		elif var=='PwT':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('inp').union(self.get('int')),self.get('txE')), name = self.n(var))
		elif var == 'Peq':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('fg_HH'),self.get('txE')), name = self.n(var))
		elif var == 'qS':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('out'),self.get('txE')), name = self.n(var))
		elif var == 'qD':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('inp').union(self.get('int')),self.get('txE')), name = self.n(var))
		elif var == 'vD':
			return pd.Series(1, index = self.savings_domain, name=self.n(var))
		elif var == 'tauS':
			return pd.Series(0, index = DataBase_wheels.prepend_index_with_1dindex(self.get('out'),self.get('txE')), name = self.n(var))
		elif var == 'tauLump':
			return pd.Series(0, index = DataBase_wheels.prepend_index_with_1dindex(self.get('s_HH'),self.get('txE')), name = self.n(var))
		elif var == 'mu':
			return pd.Series(0.5, index = self.get('map_all'), name=self.n(var))
		elif var == 'sigma':
			return pd.Series(0.5, index = self.get('kno'), name = self.n(var))
		elif var=='irate':
			return pd.Series(self.get('R_LR')*(1+self.get('infl_LR')), index = self.get('txE'), name = self.ns['irate'])
		elif var =='crra':
			return pd.Series(0.5, index = self.get('int_temp'),name = self.ns[var])
		elif var == 'disc':
			return pd.Series(self.compute_ss_disc, index = self.hh_sectors, name = self.n(var))
		elif var=='hh_tvc':
			return pd.Series(0, index = self.savings_domain.droplevel(self.n('t')).unique(),name=self.ns[var])
		elif var == 'sp':
			return self.compute_sp()

	@property
	def compute_ss_disc(self):
		return (1+self.get('g_LR'))**(self.get('crra').droplevel('n'))/self.get('R_LR')

	# ---			4: Define groups	 		--- #
	def add_group(self,group,n=None):
		if group in self.gog:
			return self.group_of_groups(group,n=n)
		else:
			return self.define_group(self.group_conditions(group))

	def define_group(self,group):
		return {self.n(var): {'conditions': self.g(var).rctree_gams(group[var]), 'text': self.g(var).write()} for var in group}

	@property
	def gog(self):
		return ['g_tech']

	def group_of_groups(self,group,n=''):
		if group == 'g_tech':
			return {'g_tech_exo': n+'g_tech_exo', 'g_tech_endo': n+'g_tech_endo'}

	def group_conditions(self,group):
		if group == 'g_tech_exo':
			return {'sigma': self.g('kno'), 'mu': {'and': [self.g('map_all'), {'not': self.g('endo_mu')}]},
					'irate': None,'disc': self.g('s_HH'),'crra':self.g('int_temp'), 'hh_tvc':{'and': [self.g('svngs'), self.g('s_HH')]}}
		elif group == 'g_tech_endo':
			return {'mu': self.g('endo_mu')}
		elif group =='g_endo_static':
			return {'PwT': self.g('int'), 'PbT': self.g('out'), 'qD': {'or': [self.g('int'), {'and': [self.g('inp'),{'not': self.g('exo')},self.g('tx0E')]}]},
					 'qS': {'and': [self.g('out'),{'not':self.g('exo')},self.g('tx0E')]}}
		elif group =='g_endo_dyn':
			return {'PwT': {'and': [self.g('top'),self.g('tx0E')]}, 'vD': {'and': [self.g('svngs'),self.g('s_HH'),self.g('tx0')]},'sp': self.g('s_HH')}
		elif group =='g_exo_static':
			return {'PwT': self.g('inp'), 'Peq': self.g('fg_HH'), 'qD': {'and': [self.g('inp'),self.g('exo')]}, 'qS': {'and': [self.g('out'), self.g('exo')]}, 
					'tauLump': self.g('s_HH'), 'tauS': self.g('out')}
		elif group =='g_calib_endo':
			return {'vD': {'and': [self.g('svngs'), self.g('s_HH'), self.g('t0')]}}
		elif group == 'g_calib_exo':
			return {'qD': {'and': [self.g('inp'),self.g('t0'),{'not': self.g('exo')}]},
					'qS': {'and': [self.g('out'),self.g('t0'),{'not': self.g('exo')}]}}
		elif group in self.gog:
			return self.gog_conditions(group)

	@property
	def exo_groups(self):
		""" Collect exogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ('g_tech','g_exo_static','g_calib_endo')}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_tech_exo','g_exo_static','g_calib_exo')}

	@property
	def endo_groups(self):
		""" Collect endogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ('g_endo_static','g_endo_dyn','g_calib_exo')}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_endo_static','g_endo_dyn','g_tech_endo','g_calib_endo')}

	@property 
	def sub_groups(self):
		""" Collect groups that are subgroups of other groups; these are not written to list of exogenous/endogenous groups. """
		n = self.model.settings.name+'_'
		if self.state == 'B':
			return {n+g: self.add_group(g,n=n) for g in ('g_tech_endo','g_tech_exo')}
		elif self.state in ('SC','DC'):
			return {}

	# --- 		4: Define blocks 		--- #
	@property
	def blocktext(self):
		return {**{f"M_{tree}": self.eqtext(tree) for tree in self.ns_local},
				**{f"M_bdgt_{self.model.settings.name}":self.eqtext_budget(), 
				   f"M_{self.model.settings.name}_dyn": self.dyn.run(self.model.settings.name)}}

	@property
	def mblocks(self):
		return set([f"M_{tree}" for tree in self.ns_local]+[f"M_bdgt_{self.model.settings.name}", f"M_{self.model.settings.name}_dyn"])

	def eqtext(self,tree_name):
		tree = self.ns_local[tree_name]
		gams_class = getattr(gams_hh,tree['type_f'])(version=tree['version'])
		gams_class.add_symbols(self.model.database,tree,ns_global=self.ns,dynamic=True)
		gams_class.add_conditions(self.model.database,tree,dynamic=True)
		return gams_class.run(tree_name)

	def eqtext_budget(self):
		gams_class = getattr(gams_hh,'budget')()
		gams_class.add_symbols(self.model.database,self.ns,sector=self.hh_sectors,dynamic=True)
		gams_class.add_conditions(sector=self.hh_sectors,dynamic=True)
		return gams_class.run(self.model.settings.name)
