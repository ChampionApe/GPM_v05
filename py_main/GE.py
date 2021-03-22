from gmspython import *
import gams_equilibrium,global_settings

class GE_v1(gmspython):
	""" Initialize this using an integrated model with all components except this."""
	def __init__(self,pickle_path=None,work_folder=None, gs_v = 'gs_v1', gs_vals={}, equi = 'v1',kwargs_ns={},**kwargs_gs):
		""" this module is not written as a self-sustained module; it can only be run in the general equilibrium."""
		databases = [DataBase.GPM_database()] 
		super().__init__(module='GE_v1',pickle_path=pickle_path,work_folder=work_folder,databases=databases,**kwargs_gs)
		if pickle_path is None:
			self.add_global_settings(gs_v,kwargs_ns=kwargs_ns,kwargs_vals=gs_vals,dynamic=True)
			self.equi = getattr(gams_equilibrium,equi)()

	def namespace(self,kwargs):
		return {s: df(s,kwargs) for s in self.default_symbols}

	@property
	def default_symbols(self):
		return ('n','s','t','txE','tx0E','t0','n_equi','d_qD','d_qS','qS','qD','Peq','Peq_endo','qS_endo')
	
	def add_endo_subsets(self,model_i,ctree_kwargs={}):
		self.model.database[self.n('Peq_endo')] = self.default_peq_endo(model_i,ctree=dfelse('Peq_endo',None,ctree_kwargs))
		self.model.database[self.n('qS_endo')] = self.default_qs_endo(model_i,ctree=dfelse('qS_endo',None,ctree_kwargs))

	def init_from_model_i(self,model_i,kwargs_ns={},ctree_kwargs={}):
		self.add_namespace(model_i,kwargs=kwargs_ns)
		self.add_sym_from_model_i(model_i)
		self.add_endo_subsets(model_i,ctree_kwargs=ctree_kwargs)

	def add_namespace(self,model_i,kwargs={}):
		self.ns = {**self.ns,**self.namespace({**model_i.ns,**kwargs})}

	def add_sym_from_model_i(self,model_i):
		for sym in self.default_symbols:
			if self.n(sym) in model_i.model.database.symbols:
				self.model.database[self.n(sym)] = model_i.get(sym)

	def default_peq_endo(self,model_i,ctree=None):
		""" define the subset of prices to be endogenized in GE"""
		if ctree is None:
			return DataBase.gpy_symbol(model_i.var_exo('Peq')).rctree_pd({'not': [{'or': [model_i.g(x) for x in ('n_tax','n_for','dur','tE') if model_i.n(x) in model_i.model.database.symbols]}]}).index.droplevel(self.n('t')).unique()
		else:
			return DataBase.gpy_symbol(model_i.var_exo('Peq')).rctree_pd(ctree).index.droplevel(self.n('t')).unique()

	def default_qs_endo(self,model_i,ctree=None):
		if ctree is None:
			return model_i.var_exo('qS').index.droplevel(self.n('t')).unique()
		else:
			return DataBase.gpy_symbol(model_i.var_exo('qS')).rctree_pd(ctree).index.droplevel(self.n('t')).unique()

	def initialize_variables(self):
		self.equi.add_symbols(self.model.database,self.ns,dynamic=True)
		self.equi.add_conditions(self.model.database,self.ns,dynamic=True)

	# ---			3: Define groups	 		--- #
	def add_group(self,group,n=None):
		return self.define_group(self.group_conditions(group))

	def define_group(self,group):
		return {self.n(var): {'conditions': self.g(var).rctree_gams(group[var]), 'text': self.g(var).write()} for var in group}	

	def group_conditions(self,group):
		if group == 'ge_t0':
			return {'qS': {'and': [self.g('qS_endo'), self.g('t0')]}, 'Peq': {'and': [self.g('Peq_endo'),self.g('t0')]}}
		elif group == 'ge_tx0E':
			return {'qS': {'and': [self.g('qS_endo'), self.g('tx0E')]}, 'Peq': {'and': [self.g('Peq_endo'),self.g('tx0E')]}}

	@property
	def endo_groups(self):
		""" Collect endogenous groups """
		n = self.model.settings.name+'_'
		if self.state == 'B':
			return {n+g: self.add_group(g,n=n) for g in ('ge_t0','ge_tx0E')}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ['ge_tx0E']}

	@property
	def exo_groups(self):
		n = self.model.settings.name+'_'
		if self.state == 'B':
			return {}
		elif self.state in ('SC','DC'):
			return {n+g: self.add_group(g,n=n) for g in ['ge_t0']}

	@property 
	def sub_groups(self):
		return {}

	@property
	def gog(self):
		return []

	# --- 		4: Define blocks 		--- #
	@property
	def blocktext(self):
		return {f"M_{self.model.settings.name}_eqt0": self.equi.run(self.model.settings.name,block='t0'),
				f"M_{self.model.settings.name}_eqtx0E": self.equi.run(self.model.settings.name,block='tx0E')}
	@property
	def mblocks(self):
		if self.state == 'B':
			return set([f"M_{self.model.settings.name}_eqt0", f"M_{self.model.settings.name}_eqtx0E"])
		elif self.state in ('SC','DC'):
			return set([f"M_{self.model.settings.name}_eqtx0E"])
