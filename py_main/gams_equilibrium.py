import pandas as pd, DataBase, DataBase_wheels

def equation(name,domains,conditions,LHS,RHS):
	return f"""{name}{domains}{'$('+conditions+')' if conditions != '' else conditions}..	{LHS} =E= {RHS};"""

def df(x,kwargs):
	"""
	Modify x using keyword arguments (dicts,kwarg).
	"""
	return x if x not in kwargs else kwargs[x]

def create_alias_dict(aliases,list_of_tuples_indices=[]):
	return {aliases[i[0]]: aliases[i[1]] for i in list_of_tuples_indices}

def ign_KeyError(dict_,key):
	try:
		return dict_[key]
	except KeyError:
		return None

class v1:
	""" Equilibrium on goods markets, n_equi[n], where sum(s$(d_vS[t,s,n]), qS[t,s,n]) = sum(s$(d_vD[t,s,n]), qD[t,s,n])"""
	def __init__(self,**kwargs):
		pass

	def add_symbols(self,db,ns,dynamic=False):
		[setattr(self,sym,db[df(sym,ns)]) for sym in ('s','n_equi','d_qD','d_qS','qD','qS','Peq')];
		if dynamic is True:
			[setattr(self,sym,db[df(sym,ns)]) for sym in ('t','txE')];

	def add_conditions(self,db,ns,dynamic=False):
		self.conditions = {'equi_t0': f"{db[ns['n_equi']].write()}{' and {t0}'.format(t0=db[ns['t0']].write()) if 't0' in ns else ''}"}
		if dynamic is True:
			self.conditions['equi_tx0E'] = f"{db[ns['n_equi']].write()} and {db[ns['tx0E']].write()}"

	def a(self,attr,lot_indices=[],l=''):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l)

	def run(self,name,block='t0'):
		if block == 't0':
			return self.equilibrium(f"E_equi_{name}",self.conditions['equi_t0'])
		elif block == 'tx0E':
			return self.equilibrium(f"E_equi_tx0E_{name}",self.conditions['equi_tx0E'])

	def equilibrium(self,name,conditions):
		LHS = f"""sum({self.s.write()}$({self.d_qS.write()}), {self.qS.write()})"""
		RHS = f"""sum({self.s.write()}$({self.d_qD.write()}), {self.qD.write()})"""
		return equation(name,self.Peq.doms(),conditions,LHS,RHS)
