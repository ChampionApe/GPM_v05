from gmspython import *
from functools import reduce
import gams_government,global_settings

def taxRevenue(db):
	return reduce(lambda x,y: x.add(y,fill_value=0),[(db['qD'].rctree_pd(db['d_tauD'])*db.get('tauD')).fillna(0).groupby(db['qD'].domains[0:-1]).sum(),
													 (db['qS'].rctree_pd(db['d_tauS'])*db.get('tauS')).fillna(0).groupby(db['qS'].domains[0:-1]).sum(),
													  db.get('tauLump')])

def balanceIO_lumpsum(db):
	""" Returns the value of lump sum taxes required to target IO tax revenues."""
	return pd.Series((db['vD'].rctree_pd({'and': [db['d_tauLump'], db['n_tax']]}).droplevel(-1)-taxRevenue(db)).dropna()+db.get('tauLump'),name=db.get('tauLump').name)

def balanceIO_advalorem(db):
	advalorem_balance = (db['vD'].rctree_pd(db['n_tax']).droplevel(-1)-taxRevenue(db))/(db['qD'].rctree_pd(db['d_tauD'])*db.get('Peq')).groupby('s').sum()
	return pd.Series(advalorem2point_demand_tax(db,advalorem_balance).add(db.get('tauD'),fill_value=0), name=db.get('tauD').name)

def advalorem2point_demand_tax(db,advalorem):
	return advalorem*pd.Series(1,db.get('d_tauD')) * db.get('Peq')

class g_static(gmspython):
	""" government sector, static."""
	def __init__(self,GE_data=None,pickle_path=None,work_folder=None,kwargs_ns={},gclass='v1',gs_v='gs_v1',**kwargs_gs):
		super().__init__(module='g_static',pickle_path=pickle_path,work_folder=work_folder,databases=[GE_data],**kwargs_gs)
		if pickle_path is None:
			self.ns = {**self.ns, **self.namespace_sets(kwargs_ns), **self.namespace_variables(kwargs_ns)}
			self.add_global_settings(gs_v,kwargs_ns=kwargs_ns)
			self.add_default_subsets()
			self.gclass = getattr(gams_government,gclass)(**kwargs_ns)

	# --- 			1: Default namespaces and subsets 			--- #
	def namespace_sets(self,kwargs):
		return {k: df(k,kwargs) for k in ('n','nn','n_tax','s','s_HH','s_tax','d_tauS','d_tauD','d_tauLump','tauDendo','d_Peq')}

	def namespace_variables(self,kwargs):
		return {k: df(k,kwargs) for k in self.default_variables}

	def add_default_subsets(self):
		self.model.database[self.n('tauDendo')] = self.default_endo_tau

	@property
	def default_endo_tau(self):
		""" pick random elements in tauD to adjust."""
		endo_tau = empty_index(self.get('d_tauD'))
		for s in self.get('d_tauD').levels[0]:
			endo_tau = endo_tau.insert(0,self.get('d_tauD')[self.get('d_tauD').get_level_values(0)==s][0])
		return endo_tau

	@property
	def default_variables(self):
		return ('Peq','PwT','PbT','qD','qS','vD','tauD','tauS','tauLump','TotTaxRev')

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
		self.init_gclass()

	def default_var_series(self,var):
		if var == 'Peq':
			return pd.Series(1, index = self.get('d_Peq'),name = self.n(var))
		elif var=='PwT':
			return pd.Series(1, index = self.get('d_tauD'), name = self.n(var))
		elif var =='PbT':
			return pd.Series(1, index = self.get('d_tauS'), name = self.n(var))
		elif var == 'qD':
			return pd.Series(1, index = self.get('d_tauD'), name = self.n(var))
		elif var == 'qS':
			return pd.Series(1, index = self.get('d_tauS'), name = self.n(var))
		elif var == 'vD':
			return pd.Series(0, index = pd.MultiIndex.from_product([self.get('s_tax'),self.get('n_tax')],names=self.g('s_tax').domains+self.g('n_tax').domains), name = self.n(var))
		elif var == 'tauD':
			return pd.Series(0, index = self.get('d_tauD'), name = self.n(var))
		elif var == 'tauS':
			return pd.Series(0, index = self.get('d_tauS'), name = self.n(var))
		elif var == 'tauLump':
			return pd.Series(0, index = self.get('d_tauLump'), name = self.n(var))
		elif var == 'TotTaxRev':
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
		return []

	def group_conditions(self,group):
		if group == 'g_exo':
			return {'qD': self.g('d_tauD'), 'qS': self.g('d_tauS'), 'vD': {'and': [self.g('s_tax'), self.g('n_tax')]},
					'tauD': {'and': [self.g('d_tauD'), {'not': self.g('tauDendo')}]}, 'tauS': self.g('d_tauS'), 'tauLump': self.g('d_tauLump'), 
					'PbT': self.g('d_tauS'), 'Peq': self.g('d_Peq')}
		elif group == 'g_endo':
			return {'TotTaxRev': None,'PwT': self.g('d_tauD')}
		elif group == 'g_calib_endo':
			return {'tauD': self.g('tauDendo')}
		elif group in self.gog:
			return self.gog_conditions(group)

	@property
	def exo_groups(self):
		""" Collect exogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ('g_exo','g_calib_endo')}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ['g_exo']}

	@property
	def endo_groups(self):
		""" Collect endogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in  ['g_endo']}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_endo','g_calib_endo')}

	# --- 		4: Define blocks 		--- #
	@property
	def blocktext(self):
		return {f"M_gov_{self.model.settings.name}": self.gclass.run(self.model.settings.name,block='std'), 
				f"M_gcalib_{self.model.settings.name}": self.gclass.run(self.model.settings.name,block='calib')}

	@property
	def mblocks(self):
		if self.state =='B':
			return set([f"M_gov_{self.model.settings.name}"])
		elif self.state in ('SC','DC'):
			return set([f"M_gov_{self.model.settings.name}", f"M_gcalib_{self.model.settings.name}"])

	def init_gclass(self):
		self.gclass.add_symbols(self.model.database,self.ns)
		self.gclass.add_conditions(self.model.database,self.ns)

	@staticmethod
	def add_t_to_variable(var,tindex):
		if tindex.name not in var.index.names:
			return pd.concat({i: var for i in tindex},names=tindex.names)
		else:
			return var

class g_dynamic(gmspython):
	""" government sector, static."""
	def __init__(self,GE_data=None,pickle_path=None,work_folder=None,kwargs_ns={},gclass='v1',gs_v='gs_v1',gs_vals={},**kwargs_gs):
		super().__init__(module='g_dynamic',pickle_path=pickle_path,work_folder=work_folder,databases=[GE_data],**kwargs_gs)
		if pickle_path is None:
			self.ns = {**self.ns, **self.namespace_sets(kwargs_ns), **self.namespace_variables(kwargs_ns)}
			self.add_global_settings(gs_v,kwargs_ns=kwargs_ns,kwargs_vals=gs_vals,dynamic=True)
			self.add_default_subsets(kwargs_ns=kwargs_ns)
			self.gclass = getattr(gams_government,gclass)(**kwargs_ns)

	# --- 			1: Default namespaces and subsets 			--- #
	def namespace_sets(self,kwargs):
		return {k: df(k,kwargs) for k in ('n','nn','n_tax','s','s_tax','s_G','d_tauS','d_tauD','d_tauLump','tauDendo','d_Peq')}

	def namespace_variables(self,kwargs):
		return {k: df(k,kwargs) for k in self.default_variables}

	def add_default_subsets(self,kwargs_ns={}):
		self.model.database[self.n('tauDendo')] = self.default_endo_tau
		self.ns['gsvngs'] = df('gsvngs',kwargs_ns)
		self.model.database[self.ns['gsvngs']] = pd.Index(['gsvngs'],name=self.ns['n'])
		self.model.database[self.ns['n']] = self.get('n').union(self.get('gsvngs')).unique()
		self.model.database[self.ns['s_G']] = pd.Index(['G'], name = self.ns['s'])
		self.model.database[self.ns['s']] = self.get('s').union(self.get('s_G')).unique()

	@property
	def default_endo_tau(self):
		""" pick random elements in tauD to adjust."""
		endo_tau = empty_index(self.get('d_tauD'))
		for s in self.get('d_tauD').levels[0]:
			endo_tau = endo_tau.insert(0,self.get('d_tauD')[self.get('d_tauD').get_level_values(0)==s][0])
		return endo_tau

	@property
	def default_variables(self):
		return ('Peq','PwT','PbT','qD','qS','vD','tauD','tauS','tauLump','TotTaxRev','irate','g_tvc')

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
		self.init_gclass()

	def ivfs(self,static,variables=['Peq','PwT','PbT','qD','qS','vD','tauD','tauS','tauLump'],merge=True):
		""" initialize variables from database w. static version """ 
		for var in variables:
			add_var = g_static.add_t_to_variable(static.get(self.ns[var]),self.get('txE'))
			if merge is True and self.ns[var] in self.model.database.symbols:
				self.model.database[self.ns[var]] = add_var.combine_first(self.get(var))
			else:
				self.model.database[self.ns[var]] = add_var

	def default_var_series(self,var):
		if var == 'Peq':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('d_Peq'),self.get('txE')),name = self.n(var))
		elif var=='PwT':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('d_tauD'),self.get('txE')), name = self.n(var))
		elif var =='PbT':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('d_tauS'),self.get('txE')), name = self.n(var))
		elif var == 'qD':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('d_tauD'),self.get('txE')), name = self.n(var))
		elif var == 'qS':
			return pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.get('d_tauS'),self.get('txE')), name = self.n(var))
		elif var == 'vD':
			sector_rev = DataBase_wheels.prepend_index_with_1dindex(pd.MultiIndex.from_product([self.get('s_tax'),self.get('n_tax')],names=self.g('s_tax').domains+self.g('n_tax').domains), self.get('t0'))
			gsvngs = DataBase_wheels.prepend_index_with_1dindex(pd.MultiIndex.from_product([self.get('s_G'),self.get('gsvngs')], names = self.g('s_tax').domains+self.g('gsvngs').domains), self.get('t'))
			return pd.Series(0, index = sector_rev.union(gsvngs), name = self.n(var))
		elif var == 'tauD':
			return pd.Series(0, index = DataBase_wheels.prepend_index_with_1dindex(self.get('d_tauD'),self.get('txE')), name = self.n(var))
		elif var == 'tauS':
			return pd.Series(0, index = DataBase_wheels.prepend_index_with_1dindex(self.get('d_tauS'),self.get('txE')), name = self.n(var))
		elif var == 'tauLump':
			return pd.Series(0, index = DataBase_wheels.prepend_index_with_1dindex(self.get('d_tauLump'),self.get('txE')), name = self.n(var))
		elif var == 'TotTaxRev':
			return pd.Series(0, index = self.get('txE'),name=self.n(var))
		elif var == 'irate':
			return pd.Series(self.get('R_LR')*(1+self.get('infl_LR')), index = self.get('txE'), name = self.ns['irate'])
		elif var == 'g_tvc':
			return pd.Series(0, index = pd.MultiIndex.from_product([self.get('s_G'),self.get('gsvngs')],names=self.g('s_G').domains+self.g('gsvngs').domains), name = self.n(var))

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
		return []

	def group_conditions(self,group):
		if group == 'g_exo':
			return {'qD': self.g('d_tauD'), 'qS': self.g('d_tauS'), 'vD': {'and': [self.g('s_tax'), self.g('n_tax')]}, 'tauS': self.g('d_tauS'), 'tauLump': self.g('d_tauLump'), 'PbT': self.g('d_tauS'), 'Peq': self.g('d_Peq'),
			'tauD': {'and': [self.g('d_tauD'), {'or': [self.g('tx0E'), {'and': [self.g('t0'), {'not': self.g('tauDendo')}]}]}]}}
		elif group == 'g_exo_dyn':
			return {'irate': None, 'vD': {'and': [self.g('gsvngs'),self.g('s_G'),self.g('t0')]}}
		elif group == 'g_endo':
			return {'TotTaxRev': None,'PwT': self.g('d_tauD'), 'vD': {'and': [self.g('gsvngs'),self.g('s_G'),self.g('tx0')]},'g_tvc': {'and': [self.g('gsvngs'), self.g('s_G')]}}
		elif group == 'g_calib_endo':
			return {'tauD': {'and': [self.g('tauDendo'), self.g('t0')]}}
		elif group in self.gog:
			return self.gog_conditions(group)

	@property
	def exo_groups(self):
		""" Collect exogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in ('g_exo','g_calib_endo','g_exo_dyn')}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_exo','g_exo_dyn')}

	@property
	def endo_groups(self):
		""" Collect endogenous groups """
		n = self.model.settings.name+'_'
		if self.state=='B':
			return {n+g: self.add_group(g,n=n) for g in  ['g_endo']}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ('g_endo','g_calib_endo')}

	# --- 		4: Define blocks 		--- #
	@property
	def blocktext(self):
		return {f"M_gov_{self.model.settings.name}": self.gclass.run(self.model.settings.name,block='std'), 
				f"M_gcalib_{self.model.settings.name}": self.gclass.run(self.model.settings.name,block='calib')}

	@property
	def mblocks(self):
		if self.state =='B':
			return set([f"M_gov_{self.model.settings.name}"])
		elif self.state in ('SC','DC'):
			return set([f"M_gov_{self.model.settings.name}", f"M_gcalib_{self.model.settings.name}"])

	def init_gclass(self):
		self.gclass.add_symbols(self.model.database,self.ns,dynamic=True)
		self.gclass.add_conditions(self.model.database,self.ns,dynamic=True)
