import pandas as pd
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

class Armington_v1:
	""" Simple isoelastic demand equations with mappings from domestic-to-foreign goods/prices"""
	def __init__(self,version='std',**kwargs):
		""" Add version of the model """
		self.version = version

	def add_symbols(self,db,ns_local,ns_global={},dynamic=False):
		""" add gpy_symbols with writing methods. ns is a namespace to update symbol names if they are nonstandard """
		for sym in ['dom2for']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PwT','Peq','qD','phi','sigma','n'):
			setattr(self,sym,db[df(sym,ns_global)])
		if dynamic is True:
			for sym in ('txE','t0','tE','tx0E'):
				setattr(self,sym,db[df(sym,ns_global)])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns_tree,dynamic=False):
		""" add gpy_symbols with writing methods. ns_tree is a namespace for relevant subsets to condition the equations on."""
		self.conditions = {'fdemand': db[ns_tree['sfor_ndom']].write()}
		if dynamic is True:
			self.conditions = {key: value+' and '+self.txE.write() for key,value in self.conditions.items()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		nn,phi,sigma = self.a('n',[(0,1)]),self.a('phi'),self.a('sigma')
		map_ = self.a('dom2for')
		PwT, Peq2 = self.a('PwT'),self.a('Peq',[(0,1)])
		qD = self.a('qD')
		text = self.demand(f"E_fdemand_{name}",conditions['fdemand'],nn,map_,phi,PwT,Peq2,qD,sigma)
		return text

	def demand(self,name,conditions,nn,map_,phi,PwT,Peq2,qD,sigma):
		""" armington demand """
		RHS = f"""sum({nn}$({map_}), {phi} * ({Peq2}/{PwT})**({sigma}))""" 
		return equation(name,self.qD.doms(),conditions,qD,RHS)
