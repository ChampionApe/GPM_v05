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

class CES:
	""" collection of price indices / demand systems for ces nests """
	def __init__(self,version='std',**kwargs):
		""" Add version of the model """
		self.version = version

	def add_symbols(self,db,ns_local,ns_global={},dynamic=False):
		""" add gpy_symbols with writing methods. ns is a namespace to update symbol names if they are nonstandard """
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PbT','PwT','qD','qS','mu','sigma','n'):
			setattr(self,sym,db[df(sym,ns_global)])
		if dynamic is True:
			for sym in ('txE','t0','tE','tx0E'):
				setattr(self,sym,db[df(sym,ns_global)])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns_tree,dynamic=False):
		""" add gpy_symbols with writing methods. ns_tree is a namespace for relevant subsets to condition the equations on."""
		self.conditions = {'zp_out': db[ns_tree['tree_out']].write(),'zp_nout': db[ns_tree['kno_no']].write(), 'q_out': db[ns_tree['bra_o']].write(), 'q_nout': db[ns_tree['bra_no']].write()}
		if dynamic is True:
			self.conditions = {key: value+' and '+self.txE.write() for key,value in self.conditions.items()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		nn,mu,sigma2 = self.a('n',[(0,1)]),self.a('mu'),self.a('sigma',[(0,1)])
		map_,map_2 = self.a('map_'),self.a('map_',[(0,1),(1,0)])
		PwT, PwT2 = self.a('PwT'),self.a('PwT',[(0,1)])
		PbT,PbT2 = self.a('PbT'),self.a('PbT',[(0,1)])
		qD,qD2 = self.a('qD'), self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'), self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_out_{name}",conditions['zp_out'],nn,map_2,qD,qD2,qS,PbT,PwT,PwT2,output=True)+'\n\t'
		text += self.zero_profit(f"E_zp_nout_{name}",conditions['zp_nout'],nn,map_2,qD,qD2,qS,PbT,PwT,PwT2,output=False)+'\n\t'
		text += self.demand(f"E_q_out_{name}",conditions['q_out'],nn,map_,mu,PwT,PwT2,PbT2,qD,qD2,qS2,sigma2,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}",conditions['q_nout'],nn,map_,mu,PwT,PwT2,PbT2,qD,qD2,qS2,sigma2,output=False)
		return text
		
	def demand(self,name,conditions,nn,map_,mu,PwT,PwT2,PbT2,qD,qD2,qS2,sigma2,output=False):
		""" ces demand """
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PwT2}/{PwT})**({sigma2}) * {qD2})"""
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PbT2}/{PwT})**({sigma2}) * {qS2})"""
		return equation(name,self.qD.doms(),conditions,qD,RHS)

	def zero_profit(self,name,conditions,nn,map_2,qD,qD2,qS,PbT,PwT,PwT2,output=False):
		""" zero profits condition """
		RHS = f"""sum({nn}$({map_2}), {qD2}*{PwT2})"""
		if output is True:
			return equation(name,self.PbT.doms(),conditions,f"{PbT}*{qS}",RHS)
		else:
			return equation(name,self.PwT.doms(),conditions,f"{PwT}*{qD}",RHS)

class CES_norm:
	""" collection of price indices / demand systems for ces nests """
	def __init__(self,version='std',**kwargs):
		""" Add version of the model """
		self.version = version

	def add_symbols(self,db,ns_local,ns_global={},dynamic=False):
		""" add gpy_symbols with writing methods. ns is a namespace to update symbol names if they are nonstandard """
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PbT','PwT','qD','qS','mu','sigma','n'):
			setattr(self,sym,db[df(sym,ns_global)])
		if dynamic is True:
			for sym in ('txE','t0','tE','tx0E'):
				setattr(self,sym,db[df(sym,ns_global)])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns_tree,dynamic=False):
		""" add gpy_symbols with writing methods. ns_tree is a namespace for relevant subsets to condition the equations on."""
		self.conditions = {'zp_out': db[ns_tree['tree_out']].write(),'zp_nout': db[ns_tree['kno_no']].write(), 'q_out': db[ns_tree['bra_o']].write(), 'q_nout': db[ns_tree['bra_no']].write()}
		if dynamic is True:
			self.conditions = {key: value+' and '+self.txE.write() for key,value in self.conditions.items()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		nn,nnn = self.a('n',[(0,1)]), self.a('n',[(0,2)])
		mu,mu3 = self.a('mu'), self.a('mu',[(0,2)])
		sigma2 = self.a('sigma',[(0,1)])
		map_,map_2,map_3 = self.a('map_'),self.a('map_',[(0,1)]), self.a('map_',[(0,2)])
		PwT,PwT2,PwT3 = self.a('PwT'), self.a('PwT',[(0,1)]), self.a('PwT',[(0,2)])
		PbT,PbT2 = self.a('PbT'),self.a('PbT',[(0,1)])
		qD,qD2 = self.a('qD'),self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'),self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_out_{name}",conditions['zp_out'],nn,map_2,qD,qD2,qS,PbT,PwT,PwT2,output=True)+'\n\t'
		text += self.zero_profit(f"E_zp_nout_{name}",conditions['zp_nout'],nn,map_2,qD,qD2,qS,PbT,PwT,PwT2,output=False)+'\n\t'
		text += self.demand(f"E_q_out_{name}", conditions['q_out'],nn,nnn,map_,map_3,mu,mu3,sigma2,PwT,PwT2,PwT3,PbT2,qD,qD2,qS2,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}", conditions['q_nout'],nn,nnn,map_,map_3,mu,mu3,sigma2,PwT,PwT2,PwT3,PbT2,qD,qD2,qS2,output=False)
		return text

	def demand(self,name,conditions,nn,nnn,map_,map_3,mu,mu3,sigma2,PwT,PwT2,PwT3,PbT2,qD,qD2,qS2,output=False):
		""" ces demand """
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PwT2}/{PwT})**({sigma2}) * {qD2} / sum({nnn}$({map_3}), {mu_3} * ({PwT2}/{PwT3})**({sigma2})))"""
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PbT2}/{PwT})**({sigma2}) * {qS2} / sum({nnn}$({map_3}), {mu_3} * ({PbT2}/{PwT3})**({sigma2})))"""
		return equation(name,self.qD.doms(),conditions,qD,RHS)

	def zero_profit(self,name,conditions,nn,map_,qD,qD2,qS,PbT,PwT,PwT2,output=False):
		""" zero profits condition """
		RHS = f"""sum({nn}$({map_}), {qD2}*{PwT2})"""
		if output is True:
			return equation(name,self.PbT.doms(),conditions,f"{PbT}*{qS}",RHS)
		else:
			return equation(name,self.PwT.doms(),conditions,f"{PwT}*{qD}",RHS)

class CET:
	""" collection of equations for CET nests """
	def __init__(self,version='std',**kwargs):
		self.version = version

	def add_symbols(self,db,ns_local,ns_global={},**kwargs):
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PbT','PwT','qD','qS','mu','eta','n','out'):
			setattr(self,sym,db[df(sym,ns_global)])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns_tree):
		self.conditions = {'zp': db[ns_tree['knots']].write(), 'q_out': db[ns_tree['bra_o']].write(),'q_nout': db[ns_tree['bra_no']].write()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		nn,mu,eta2,out2 = self.a('n',[(0,1)]),self.a('mu'),self.a('eta',[(0,1)]),self.a('out',[(0,1)])
		map_,map_2 = self.a('map_'),self.a('map_',[(0,1),(1,0)])
		PwT, PwT2 = self.a('PwT'),self.a('PwT',[(0,1)])
		PbT,PbT2 = self.a('PbT'),self.a('PbT',[(0,1)])
		qD,qD2 = self.a('qD'), self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'), self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_{name}",conditions['zp'],nn,map_2,out2,qD,qD2,qS2,PbT2,PwT,PwT2)+'\n\t'
		text += self.demand(f"E_q_out_{name}",conditions['q_out'],nn,map_,mu,PwT,PwT2,PbT,qD,qD2,qS,eta2,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}",conditions['q_nout'],nn,map_,mu,PwT,PwT2,PbT,qD,qD2,qS,eta2,output=False)
		return text

	def zero_profit(self,name,conditions,nn,map_2,out2,qD,qD2,qS2,PbT2,PwT,PwT2):
		RHS = f"""sum({nn}$({map_2} and {out2}), {qS2}*{PbT2})+sum({nn}$({map_2} and not {out2}), {qD2}*{PwT2})"""
		return equation(name,self.PwT.doms(),conditions,f"{PwT}*{qD}",RHS)

	def demand(self,name,conditions,nn,map_,mu,PwT,PwT2,PbT,qD,qD2,qS,eta2,output=False):
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PwT}/{PwT2})**(-{eta2}) * {qD2})"""
			return equation(name,self.qD.doms(),conditions,qD,RHS)
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PbT}/{PwT2})**(-{eta2}) * {qD2})"""
			return equation(name,self.qS.doms(),conditions,qS,RHS)

class CET_norm:
	""" collection of price indices / demand systems for CET nests """
	def __init__(self,version='std',**kwargs):
		""" Add version of the model """
		self.version = version

	def add_symbols(self,db,ns_local,ns_global={},**kwargs):
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PbT','PwT','qD','qS','mu','eta','n','out'):
			setattr(self,sym,db[df(sym,ns_global)])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns_tree):
		self.conditions = {'zp': db[ns_tree['knots']].write(), 'q_out': db[ns_tree['bra_o']].write(),'q_nout': db[ns_tree['bra_no']].write()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		nn,nnn = self.a('n',[(0,1)]), self.a('n',[(0,2)])
		mu,mu3 = self.a('mu'), self.a('mu',[(0,2)])
		eta2 = self.a('eta',[(0,1)])
		map_,map_2,map_3 = self.a('map_'),self.a('map_',[(0,1)]), self.a('map_',[(0,2)])
		PwT,PwT2,PwT3 = self.a('PwT'), self.a('PwT',[(0,1)]), self.a('PwT',[(0,2)])
		PbT,PbT2,PbT3 = self.a('PbT'),self.a('PbT',[(0,1)]),self.a('PbT',[(0,2)])
		qD,qD2 = self.a('qD'),self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'),self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_{name}",conditions['zp'],nn,map_2,out2,qD,qD2,qS2,PbT2,PwT,PwT2)+'\n\t'
		text += self.demand(f"E_q_out_{name}",conditions['q_out'],nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwT,PwT2,PwT3,PbT,PbT3,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}",conditions['q_nout'],nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwT,PwT2,PwT3,PbT,PbT3,output=False)
		return text

	def demand(self,name,conditions,nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwT,PwT2,PwT3,PbT,PbT3,output=False):
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PwT}/{PwT2})**(-{eta2}) * {qD2}/(sum({nnn}$({map_3} and {out3}), {mu3}*({PbT3}/{PwT2})**(-{eta2}))+sum({nnn}$({map_3} and not {out3}), {mu3}*({PwT3}/{PwT2})**(-{eta2}))))"""
			return equation(name,self.qD.doms(),conditions,qD,RHS)
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PbT}/{PwT2})**(-{eta2}) * {qD2}/(sum({nnn}$({map_3} and {out3}), {mu3}*({PbT3}/{PwT2})**(-{eta2}))+sum({nnn}$({map_3} and not {out3}), {mu3}*({PwT3}/{PwT2})**(-{eta2}))))"""
			return equation(name,self.qS.doms(),conditions,qS,RHS)

	def zero_profit(self,name,conditions,nn,map_2,out2,qD,qD2,qS2,PbT2,PwT,PwT2):
		RHS = f"""sum({nn}$({map_2} and {out2}), {qS2}*{PbT2})+sum({nn}$({map_2} and not {out2}), {qD2}*{PwT2})"""
		return equation(name,self.PwT.doms(),conditions,f"{PwT}*{qD}",RHS)

class MNL:
	""" collection of price indices / demand systems for MNL nests """
	def __init__(self,version='std',**kwargs):
		""" Add version of the model """
		self.version = version

	def add_symbols(self,db,ns_local,ns_global={}):
		""" add gpy_symbols with writing methods. ns is a namespace to update symbol names if they are nonstandard """
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PbT','PwT','qD','qS','mu','sigma','n'):
			setattr(self,sym,db[df(sym,ns_global)])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns_tree):
		""" add gpy_symbols with writing methods. ns_tree is a namespace for relevant subsets to condition the equations on."""
		self.conditions = {'zp_out': db[ns_tree['tree_out']].write(),'zp_nout': db[ns_tree['kno_no']].write(), 'q_out': db[ns_tree['bra_o']].write(), 'q_nout': db[ns_tree['bra_no']].write()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		nn,nnn = self.a('n',[(0,1)]), self.a('n',[(0,2)])
		mu,mu3 = self.a('mu'), self.a('mu',[(0,2)])
		sigma2 = self.a('sigma',[(0,1)])
		map_,map_2,map_3 = self.a('map_'),self.a('map_',[(0,1),(1,0)]), self.a('map_',[(0,2)])
		PwT,PwT2,PwT3 = self.a('PwT'), self.a('PwT',[(0,1)]), self.a('PwT',[(0,2)])
		PbT,PbT2 = self.a('PbT'),self.a('PbT',[(0,1)])
		qD,qD2 = self.a('qD'),self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'),self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_out_{name}",conditions['zp_out'],nn,map_2,qD,qD2,qS,PbT,PwT,PwT2,output=True)+'\n\t'
		text += self.zero_profit(f"E_zp_nout_{name}",conditions['zp_nout'],nn,map_2,qD,qD2,qS,PbT,PwT,PwT2,output=False)+'\n\t'
		text += self.demand(f"E_q_out_{name}", conditions['q_out'],nn,nnn,map_,map_3,mu,mu3,sigma2,PwT,PwT2,PwT3,PbT2,qD,qD2,qS2,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}", conditions['q_nout'],nn,nnn,map_,map_3,mu,mu3,sigma2,PwT,PwT2,PwT3,PbT2,qD,qD2,qS2,output=False)
		return text

	def zero_profit(self,name,conditions,nn,map_,qD,qD2,qS,PbT,PwT,PwT2,output=False):
		""" zero profits condition """
		RHS = f"""sum({nn}$({map_}), {qD2}*{PwT2})"""
		if output is True:
			return equation(name,self.PbT.doms(),conditions,f"{PbT}*{qS}",RHS)
		else:
			return equation(name,self.PwT.doms(),conditions,f"{PwT}*{qD}",RHS)

	def demand(self,name,conditions,nn,nnn,map_,map_3,mu,mu3,sigma2,PwT,PwT2,PwT3,PbT2,qD,qD2,qS2,output=False):
		""" MNL demand """
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * exp(({PwT2}-{PwT})*{sigma2}) * {qD2}/ sum({nnn}$({map_3}), {mu3}*exp(({PwT2}-{PwT3})*{sigma2})))"""
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * exp(({PbT2}-{PwT})*{sigma2}) * {qS2}/ sum({nnn}$({map_3}), {mu3}*exp(({PbT2}-{PwT3})*{sigma2})))"""
		return equation(name,self.qD.doms(),conditions,qD,RHS)

class MNL_out:
	""" collection of price indices / demand systems for CET nests """
	def __init__(self,version='std',**kwargs):
		""" Add version of the model """
		self.version = version

	def add_symbols(self,db,ns_local,ns_global={},**kwargs):
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PbT','PwT','qD','qS','mu','eta','n','out'):
			setattr(self,sym,db[df(sym,ns_global)])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns_tree):
		self.conditions = {'zp': db[ns_tree['knots']].write(), 'q_out': db[ns_tree['bra_o']].write(),'q_nout': db[ns_tree['bra_no']].write()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		nn,nnn = self.a('n',[(0,1)]), self.a('n',[(0,2)])
		mu,mu3 = self.a('mu'), self.a('mu',[(0,2)])
		eta2 = self.a('eta',[(0,1)])
		map_,map_2,map_3 = self.a('map_'),self.a('map_',[(0,1)]), self.a('map_',[(0,2)])
		PwT,PwT2,PwT3 = self.a('PwT'), self.a('PwT',[(0,1)]), self.a('PwT',[(0,2)])
		PbT,PbT2,PbT3 = self.a('PbT'),self.a('PbT',[(0,1)]),self.a('PbT',[(0,2)])
		qD,qD2 = self.a('qD'),self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'),self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_{name}",conditions['zp'],nn,map_2,out2,qD,qD2,qS2,PbT2,PwT,PwT2)+'\n\t'
		text += self.demand(f"E_q_out_{name}",conditions['q_out'],nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwT,PwT2,PwT3,PbT,PbT3,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}",conditions['q_nout'],nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwT,PwT2,PwT3,PbT,PbT3,output=False)
		return text

	def demand(self,name,conditions,nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwT,PwT2,PwT3,PbT,PbT3,output=False):
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * exp(({PwT}-{PwT2})*(-{eta2}))*{qD2}/(sum({nnn}$({map_3} and {out3}), {mu3}*exp(({PbT3}-{PwT2})/(-{eta2})))+sum({nnn}$({map_3} and not {out3}), {mu3}*exp(({PwT3}-{PwT2})*(-{eta2})))))"""
			return equation(name,self.qD.doms(),conditions,qD,RHS)
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * exp(({PbT}-{PwT2})*(-{eta2}))*{qD2}/(sum({nnn}$({map_3} and {out3}), {mu3}*exp(({PbT3}/{PwT2})/(-{eta2})))+sum({nnn}$({map_3} and not {out3}), {mu3}*exp(({PwT3}-{PwT2})*(-{eta2})))))"""
			return equation(name,self.qS.doms(),conditions,qS,RHS)

	def zero_profit(self,name,conditions,nn,map_2,out2,qD,qD2,qS2,PbT2,PwT,PwT2):
		RHS = f"""sum({nn}$({map_2} and {out2}), {qS2}*{PbT2})+sum({nn}$({map_2} and not {out2}), {qD2}*{PwT2})"""
		return equation(name,self.PwT.doms(),conditions,f"{PwT}*{qD}",RHS)

class pricewedge:
	def __init__(self,**kwargs):
		pass

	def add_symbols(self,db,ns,dynamic=False):
		[setattr(self,sym,db[ns[sym]]) for sym in ('n','markup','tauS','tauLump','Peq','PbT','qS','out')];
		if dynamic is True:
			[setattr(self,sym,db[ns[sym]]) for sym in ('t','txE','ic') if sym in ns];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}			

	def add_conditions(self,db,dynamic=False):
		self.conditions = {'pw': self.out.write()}
		if dynamic is True:
			self.conditions = {key: value+' and '+self.txE.write() for key,value in self.conditions.items()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name):
		return self.pricewedge(f"E_pw_{name}",self.conditions['pw'],self.a('Peq'),self.a('PbT'),self.a('PbT',[(0,1)]),self.a('qS',[(0,1)]),self.a('markup'),self.a('tauS'),self.a('tauLump'),self.a('n',[(0,1)]),self.a('out',[(0,1)]))

	def pricewedge(self,name,conditions,Peq,PbT,PbT2,qS2,markup,tauS,tauLump,nn,out2):
		RHS = f"""(1+{markup})*({PbT}*(1+{tauLump}/sum({nn}$({out2}), {qS2}*{PbT2}))+{tauS}+{0 if not hasattr(self,'ic') else self.ic.write()})"""
		return equation(name,self.PbT.doms(),conditions,Peq,RHS)

class ict_v1:
	""" Installation costs """
	def __init__(self,s=False,**kwargs):
		self.ns = self.namespace(kwargs)
		self.sector = s

	@staticmethod
	def namespace(self,**kwargs):
		return {key: df(key,kwargs) for key in ('ic','ic_1','ic_2','ic_tvc','os')}

	def add_symbols(self,db,ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ('n','t','txE','tx0','t0','tE','dur','dur2inv','PwT','qD','Rrate','rDepr','R_LR','g_LR','infl_LR','qS','PbT','out')];
		if self.sector is not False:
			self.ss = db[self.sector]
		for sym in self.ns:
			db[self.ns[sym]] = self.default_var_series(sym)
			setattr(self,sym,db[self.ns[sym]])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns):
		self.conditions = {'lom': db[ns['txE']].write(), 'pk': db[ns['tx0E']].write(),'Ktvc': db[ns['tE']].write()}
		self.conditions = {key: value +' and '+db[ns['dur']].write() for key,value in self.conditions.items()}
		[self.conditions.__setitem__(k,f"{db[ns['out']].write()} and {db[ns['txE']].write()}") for k in ('os','instcost')];
		if self.sector is not False:
			self.conditions = {key: value +' and '+self.ss.write() for key,value in self.conditions.items()}

	def default_var_series(self,var):
		if var == 'ic':
			return DataBase.gpy_symbol(pd.Series(1, index = DataBase_wheels.prepend_index_with_1dindex(self.out.vals,self.txE.vals),name=self.ns[var]),**{'text':'sum of installation costs in sector s, scaled by value of outputs, per output'})
		elif var == 'os':
			return pd.Series(0.5, index = DataBase_wheels.prepend_index_with_1dindex(self.out.vals,self.txE.vals),name=self.ns[var])
		elif var =='ic_1' and self.sector is False:
			return pd.Series(0.1,index = self.dur.vals, name=self.ns[var])
		elif var =='ic_1' and self.sector is not False:
			return pd.Series(0.1, index = pd.MultiIndex.from_product([self.ss.vals, self.dur.vals]), name = self.ns[var])
		elif var == 'ic_2':
			return self.rDepr.rctree_pd(self.tE).droplevel(self.t.name)
		elif var == 'ic_tvc' and self.sector is False:
			return pd.Series(0, index = self.dur.vals, name = self.ns[var])
		elif var == 'ic_tvc' and self.sector is not False:
			return pd.Series(0, index = pd.MultiIndex.from_product([self.ss.vals,self.dur.vals]), name = self.ns[var])

	def group_conditions(self,group):
		if group == 'ict_exo':
			return [{'ic_1': self.dur, 'ic_2': self.dur, 'ic_tvc': self.dur}]
		elif group == 'ict_endo':
			return [{'ic': self.out,'os': self.out}]

	def exo_groups(self):
		return ['ict_exo']

	def endo_groups(self):
		return ['ict_endo']

	def sub_groups(self,n=None):
		return []

	def a(self,attr,lot_indices=[],l='',tlag=''):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag={self.t.name: tlag})

	def run(self,name):
		nn,nnn = self.a('n',[(0,1)]),self.a('n',[(0,2)])
		dur2inv,dur2inv2,dur2 = self.a('dur2inv'), self.a('dur2inv',[(0,1),(1,2)]),self.a('dur',[(0,1)])
		qD, qD_m1,qD_p1 = self.a('qD'),self.a('qD',tlag='-1'),self.a('qD',tlag='+1')
		qD2,qD2_m1,qD3 = self.a('qD',[(0,1)]),self.a('qD',[(0,1)],tlag='-1'), self.a('qD',[(0,2)])
		PwT,PwT2,PwT2_m1 = self.a('PwT'),self.a('PwT',[(0,1)]), self.a('PwT',[(0,1)],tlag='-1')
		ic, ic_1, ic_2, ic_tvc = self.a('ic'), self.a('ic_1'), self.a('ic_2'), self.a('ic_tvc')
		ic_12,ic_22 = self.a('ic_1',[(0,1)]), self.a('ic_2',[(0,1)])
		Rrate,rDepr,g,infl = self.a('Rrate'), self.a('rDepr'),self.a('g_LR'),self.a('infl_LR')
		qS, qS2 = self.a('qS'),self.a('qS',[(0,1)])
		PbT,PbT2,os,out2 = self.a('PbT'),self.a('PbT',[(0,1)]),self.a('os'), self.a('out',[(0,1)])
		out = self.law_of_motion(f"E_lom_{name}", self.conditions['lom'],qD_p1,qD,rDepr,qD2,dur2inv,nn,g)+'\n\t'
		out += self.price_capital(f"E_pk_{name}", self.conditions['pk'],PwT,PwT2_m1,PwT2,qD_m1,qD2_m1,qD,qD2,Rrate,ic_1,ic_2,rDepr,nn,dur2inv,infl)+'\n\t'
		out += self.tvc_condition(f"E_Ktvc_{name}", self.conditions['Ktvc'],qD,qD_m1,ic_tvc)+'\n\t'
		out += self.outputshares(f"E_outs_{name}", self.conditions['os'],nn,qS,PbT,qS2,PbT2,os,out2)+'\n\t'
		out += self.invest_cost(f"E_instcost_{name}", self.conditions['instcost'],nn,nnn,dur2,dur2inv2,os,qS,qD2,qD3,ic,ic_12,ic_22)
		return out

	def law_of_motion(self,name,conditions,qD_p1,qD,rDepr,qD2,dur2inv,nn,g):
		RHS = f"""({qD}*(1-{rDepr})+sum({nn}$({dur2inv}), {qD2}))/(1+{g})"""
		return equation(name,self.qD.doms(),conditions,qD_p1,RHS)

	def price_capital(self,name,conditions,PwT,PwT2_m1,PwT2,qD_m1,qD2_m1,qD,qD2,Rrate,ic_1,ic_2,rDepr,nn,dur2inv,infl):
		RHS = f"""sum({nn}$({dur2inv}),{Rrate}*({PwT2_m1}/(1+{infl})+{ic_1}*({qD2_m1}/{qD_m1}-{ic_2}))+({ic_1}*0.5)*(sqr({ic_2}*{qD})-sqr({qD2}))/sqr({qD})-(1-{rDepr})*({PwT2}+{ic_1}*({qD2}/{qD}-{ic_2})))"""
		return equation(name,self.PwT.doms(),conditions,PwT,RHS)

	def tvc_condition(self,name,conditions,qD,qD_m1,ic_tvc):
		RHS = f"""(1+{ic_tvc})*{qD_m1}"""
		return equation(name,self.qD.doms(),conditions,qD,RHS)

	def outputshares(self,name,conditions,nn,qS,PbT,qS2,PbT2,os,out2):
		RHS = f"""{qS}*{PbT}/sum({nn}$({out2}), {qS2}*{PbT2})"""
		return equation(name,self.qS.doms(),conditions,os,RHS)

	def invest_cost(self,name,conditions,nn,nnn,dur2,dur2inv2,os,qS,qD2,qD3,ic,ic_12,ic_22):
		RHS = f"""({os}/{qS})*sum({nn}$({dur2}), sum({nnn}$({dur2inv2}), {ic_12}*0.5*{qD2}*sqr({qD3}/{qD2}-{ic_22})))"""
		return equation(name,self.ic.doms(),conditions,ic,RHS)

class itoryD_v1:
	""" collection of price indices / demand systems for ces nests """
	def __init__(self,**kwargs):
		self.ns = self.namespace(kwargs)

	@staticmethod
	def namespace(self,**kwargs):
		return {key: df(key,kwargs) for key in ['ar1_itory']}

	def add_symbols(self,db,ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ('n','t','txE','tx0','t0','tE','itoryD','qD','g_LR')];
		for sym in self.ns:
			db[self.ns[sym]] = self.default_var_series(sym)
			setattr(self,sym,db[self.ns[sym]])

	def add_conditions(self,db,ns):
		self.conditions = {'ar': f"{db[ns['tx0E']].write()} and {db[ns['itoryD']].write()}"}

	def default_var_series(self,var):
		if var == 'ar1_itory':
			return 1

	def define_group(self,group):
		return {self.ns[var]: {'conditions': getattr(self,var).rctree_gams(group[var]), 'text': getattr(self,var).write()} for var in group}

	def group_conditions(self,group):
		if group == 'itory_exo':
			return {'ar1_itory': None}

	@property
	def gog(self):
		return []

	def exo_groups(self,name_prefix):
		return {name_prefix+g: self.define_group(self.group_conditions(g)) for g in ['itory_exo']}

	def endo_groups(self,name_prefix):
		return {}

	def sub_groups(self,n=None):
		return {}

	def a(self,attr,lot_indices=[],l='',tlag=''):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(l=l,lag={self.t.name: tlag})
		
	def run(self,name):
		qD, qD_m1 = self.a('qD'),self.a('qD',tlag='-1')
		ar,g = self.a('ar1_itory'), self.a('g_LR')
		return self.ar(f"E_{name}",self.conditions['ar'],qD,qD_m1,ar,g)

	def ar(self,name,conditions,qD,qD_m1,ar,g):
		RHS = f"""{qD_m1}*{ar}/(1+{g})"""
		return equation(name,self.qD.doms(),conditions,qD,RHS)