import pandas as pd, DataBase, DataBase_wheels
def equation(name,domains,conditions,LHS,RHS):
	return f"""{name}{domains}{'$('+conditions+')' if conditions != '' else conditions}..	{LHS} =E= {RHS};"""

def df(x,kwargs):
	"""
	Modify x using keyword arguments (dicts,kwarg).
	"""
	return x if x not in kwargs else kwargs[x]

def create_alias_dict(aliases,lot_indices=[]):
	return {aliases[i[0]]: aliases[i[1]] for i in lot_indices}

def ign_KeyError(dict_,key):
	try:
		return dict_[key]
	except KeyError:
		return None
def rK_if_KE(dict_,key):
	try:
		return dict_[key]
	except KeyError:
		return key

class CES:
	""" collection of price indices / demand systems for ces nests """
	def __init__(self,version='std',state=None,**kwargs):
		""" Add version of the model """
		self.version = version
		self.state = state

	def add_symbols(self,db,ns_local,ns_global={},dynamic=False):
		""" add gpy_symbols with writing methods. ns is a namespace to update symbol names if they are nonstandard """
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ['PbT','PwThat','qD','qS','mu','sigma','n']:
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
		PwThat, PwThat2 = self.a('PwThat'),self.a('PwThat',[(0,1)])
		PbT,PbT2 = self.a('PbT'),self.a('PbT',[(0,1)])
		qD,qD2 = self.a('qD'), self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'), self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_out_{name}",conditions['zp_out'],nn,map_2,qD,qD2,qS,PbT,PwThat,PwThat2,output=True)+'\n\t'
		text += self.zero_profit(f"E_zp_nout_{name}",conditions['zp_nout'],nn,map_2,qD,qD2,qS,PbT,PwThat,PwThat2,output=False)+'\n\t'
		text += self.demand(f"E_q_out_{name}",conditions['q_out'],nn,map_,mu,PwThat,PwThat2,PbT2,qD,qD2,qS2,sigma2,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}",conditions['q_nout'],nn,map_,mu,PwThat,PwThat2,PbT2,qD,qD2,qS2,sigma2,output=False)
		return text
		
	def demand(self,name,conditions,nn,map_,mu,PwThat,PwThat2,PbT2,qD,qD2,qS2,sigma2,output=False):
		""" ces demand """
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PwThat2}/{PwThat})**({sigma2}) * {qD2})"""
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PbT2}/{PwThat})**({sigma2}) * {qS2})"""
		return equation(name,self.qD.doms(),conditions,qD,RHS)

	def zero_profit(self,name,conditions,nn,map_2,qD,qD2,qS,PbT,PwThat,PwThat2,output=False):
		""" zero profits condition """
		RHS = f"""sum({nn}$({map_2}), {qD2}*{PwThat2})"""
		if output is True:
			return equation(name,self.PbT.doms(),conditions,f"{PbT}*{qS}",RHS)
		else:
			return equation(name,self.PwThat.doms(),conditions,f"{PwThat}*{qD}",RHS)

class CES_norm:
	""" collection of price indices / demand systems for ces nests """
	def __init__(self,version='std',state=None,**kwargs):
		""" Add version of the model """
		self.version = version
		self.state = state

	def add_symbols(self,db,ns_local,ns_global={},dynamic=False):
		""" add gpy_symbols with writing methods. ns is a namespace to update symbol names if they are nonstandard """
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ['PbT','PwThat','qD','qS','mu','sigma','n']:
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
		map_,map_2,map_3 = self.a('map_'),self.a('map_',[(0,1),(1,0)]), self.a('map_',[(0,2)])
		PwThat,PwThat2,PwThat3 = self.a('PwThat'), self.a('PwThat',[(0,1)]), self.a('PwThat',[(0,2)])
		PbT,PbT2 = self.a('PbT'),self.a('PbT',[(0,1)])
		qD,qD2 = self.a('qD'),self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'),self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_out_{name}",conditions['zp_out'],nn,map_2,qD,qD2,qS,PbT,PwThat,PwThat2,output=True)+'\n\t'
		text += self.zero_profit(f"E_zp_nout_{name}",conditions['zp_nout'],nn,map_2,qD,qD2,qS,PbT,PwThat,PwThat2,output=False)+'\n\t'
		text += self.demand(f"E_q_out_{name}", conditions['q_out'],nn,nnn,map_,map_3,mu,mu3,sigma2,PwThat,PwThat2,PwThat3,PbT2,qD,qD2,qS2,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}", conditions['q_nout'],nn,nnn,map_,map_3,mu,mu3,sigma2,PwThat,PwThat2,PwThat3,PbT2,qD,qD2,qS2,output=False)
		return text

	def demand(self,name,conditions,nn,nnn,map_,map_3,mu,mu3,sigma2,PwThat,PwThat2,PwThat3,PbT2,qD,qD2,qS2,output=False):
		""" ces demand """
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PwThat2}/{PwThat})**({sigma2}) * {qD2} / sum({nnn}$({map_3}), {mu3} * ({PwThat2}/{PwThat3})**({sigma2})))"""
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PbT2}/{PwThat})**({sigma2}) * {qS2} / sum({nnn}$({map_3}), {mu3} * ({PbT2}/{PwThat3})**({sigma2})))"""
		return equation(name,self.qD.doms(),conditions,qD,RHS)

	def zero_profit(self,name,conditions,nn,map_,qD,qD2,qS,PbT,PwThat,PwThat2,output=False):
		""" zero profits condition """
		RHS = f"""sum({nn}$({map_}), {qD2}*{PwThat2})"""
		if output is True:
			return equation(name,self.PbT.doms(),conditions,f"{PbT}*{qS}",RHS)
		else:
			return equation(name,self.PwThat.doms(),conditions,f"{PwThat}*{qD}",RHS)

class CET:
	""" collection of equations for CET nests """
	def __init__(self,version='std',state="ID",**kwargs):
		self.version = version
		self.state = state

	def add_symbols(self,db,ns_local,ns_global={},**kwargs):
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PbT','PwThat','qD','qS','mu','eta','n'):
			setattr(self,sym,db[df(sym,ns_global)])
		for sym in ['out']:
			setattr(self, self.state + "_" + sym, db[df(self.state + "_" + sym, ns_global)])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns_tree):
		self.conditions = {'zp': db[ns_tree['knots']].write(), 'q_out': db[ns_tree['bra_o']].write(),'q_nout': db[ns_tree['bra_no']].write()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		nn,mu,eta2,out2 = self.a('n',[(0,1)]),self.a('mu'),self.a('eta',[(0,1)]),self.a(self.state + "_" + 'out',[(0,1)])
		map_,map_2 = self.a('map_'),self.a('map_',[(0,1),(1,0)])
		PwThat, PwThat2 = self.a('PwThat'),self.a('PwThat',[(0,1)])
		PbT,PbT2 = self.a('PbT'),self.a('PbT',[(0,1)])
		qD,qD2 = self.a('qD'), self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'), self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_{name}",conditions['zp'],nn,map_2,out2,qD,qD2,qS2,PbT2,PwThat,PwThat2)+'\n\t'
		text += self.demand(f"E_q_out_{name}",conditions['q_out'],nn,map_,mu,PwThat,PwThat2,PbT,qD,qD2,qS,eta2,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}",conditions['q_nout'],nn,map_,mu,PwThat,PwThat2,PbT,qD,qD2,qS,eta2,output=False)
		return text

	def zero_profit(self,name,conditions,nn,map_2,out2,qD,qD2,qS2,PbT2,PwThat,PwThat2):
		RHS = f"""sum({nn}$({map_2} and {out2}), {qS2}*{PbT2})+sum({nn}$({map_2} and not {out2}), {qD2}*{PwThat2})"""
		return equation(name,self.PwThat.doms(),conditions,f"{PwThat}*{qD}",RHS)

	def demand(self,name,conditions,nn,map_,mu,PwThat,PwThat2,PbT,qD,qD2,qS,eta2,output=False):
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PwThat}/{PwThat2})**(-{eta2}) * {qD2})"""
			return equation(name,self.qD.doms(),conditions,qD,RHS)
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PbT}/{PwThat2})**(-{eta2}) * {qD2})"""
			return equation(name,self.qS.doms(),conditions,qS,RHS)

class CET_norm:
	""" collection of price indices / demand systems for CET nests """
	def __init__(self,version='std',state="ID",**kwargs):
		""" Add version of the model """
		self.version = version
		self.state = state

	def add_symbols(self,db,ns_local,ns_global={},**kwargs):
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PbT','PwThat','qD','qS','mu','eta','n'):
			setattr(self,sym,db[df(sym,ns_global)])
		for sym in ['out']:
			setattr(self, self.state + "_" + sym, db[df(self.state + "_" + sym, ns_global)])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns_tree):
		self.conditions = {'zp': db[ns_tree['knots']].write(), 'q_out': db[ns_tree['bra_o']].write(),'q_nout': db[ns_tree['bra_no']].write()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		out2,out3 = self.a(self.state + "_" + 'out',[(0,1)]), self.a(self.state + "_" + 'out',[(0,2)])
		nn,nnn = self.a('n',[(0,1)]), self.a('n',[(0,2)])
		mu,mu3 = self.a('mu'), self.a('mu',[(0,2)])
		eta2 = self.a('eta',[(0,1)])
		map_,map_2,map_3 = self.a('map_'),self.a('map_',[(0,1), (1,0)]), self.a('map_',[(0,2)])
		PwThat,PwThat2,PwThat3 = self.a('PwThat'), self.a('PwThat',[(0,1)]), self.a('PwThat',[(0,2)])
		PbT,PbT2,PbT3 = self.a('PbT'),self.a('PbT',[(0,1)]),self.a('PbT',[(0,2)])
		qD,qD2 = self.a('qD'),self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'),self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_{name}",conditions['zp'],nn,map_2,out2,qD,qD2,qS2,PbT2,PwThat,PwThat2)+'\n\t'
		text += self.demand(f"E_q_out_{name}",conditions['q_out'],nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwThat,PwThat2,PwThat3,PbT,PbT3,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}",conditions['q_nout'],nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwThat,PwThat2,PwThat3,PbT,PbT3,output=False)
		return text

	def demand(self,name,conditions,nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwThat,PwThat2,PwThat3,PbT,PbT3,output=False):
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PwThat}/{PwThat2})**(-{eta2}) * {qD2}/(sum({nnn}$({map_3} and {out3}), {mu3}*({PbT3}/{PwThat2})**(-{eta2}))+sum({nnn}$({map_3} and not {out3}), {mu3}*({PwThat3}/{PwThat2})**(-{eta2}))))"""
			return equation(name,self.qD.doms(),conditions,qD,RHS)
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PbT}/{PwThat2})**(-{eta2}) * {qD2}/(sum({nnn}$({map_3} and {out3}), {mu3}*({PbT3}/{PwThat2})**(-{eta2}))+sum({nnn}$({map_3} and not {out3}), {mu3}*({PwThat3}/{PwThat2})**(-{eta2}))))"""
			return equation(name,self.qS.doms(),conditions,qS,RHS)

	def zero_profit(self,name,conditions,nn,map_2,out2,qD,qD2,qS2,PbT2,PwThat,PwThat2):
		RHS = f"""sum({nn}$({map_2} and {out2}), {qS2}*{PbT2})+sum({nn}$({map_2} and not {out2}), {qD2}*{PwThat2})"""
		return equation(name,self.PwThat.doms(),conditions,f"{PwThat}*{qD}",RHS)


class MNL:
	""" collection of price indices / demand systems for MNL nests """
	def __init__(self,version='std',state=None,**kwargs):
		""" Add version of the model """
		self.version = version
		self.state = state

	def add_symbols(self,db,ns_local,ns_global={}):
		""" add gpy_symbols with writing methods. ns is a namespace to update symbol names if they are nonstandard """
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PbT','PwThat','qD','qS','mu','sigma','n'):
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
		PwThat,PwThat2,PwThat3 = self.a('PwThat'), self.a('PwThat',[(0,1)]), self.a('PwThat',[(0,2)])
		PbT,PbT2 = self.a('PbT'),self.a('PbT',[(0,1)])
		qD,qD2 = self.a('qD'),self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'),self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_out_{name}",conditions['zp_out'],nn,map_2,qD,qD2,qS,PbT,PwThat,PwThat2,output=True)+'\n\t'
		text += self.zero_profit(f"E_zp_nout_{name}",conditions['zp_nout'],nn,map_2,qD,qD2,qS,PbT,PwThat,PwThat2,output=False)+'\n\t'
		text += self.demand(f"E_q_out_{name}", conditions['q_out'],nn,nnn,map_,map_3,mu,mu3,sigma2,PwThat,PwThat2,PwThat3,PbT2,qD,qD2,qS2,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}", conditions['q_nout'],nn,nnn,map_,map_3,mu,mu3,sigma2,PwThat,PwThat2,PwThat3,PbT2,qD,qD2,qS2,output=False)
		return text

	def zero_profit(self,name,conditions,nn,map_,qD,qD2,qS,PbT,PwThat,PwThat2,output=False):
		""" zero profits condition """
		RHS = f"""sum({nn}$({map_}), {qD2}*{PwThat2})"""
		if output is True:
			return equation(name,self.PbT.doms(),conditions,f"{PbT}*{qS}",RHS)
		else:
			return equation(name,self.PwThat.doms(),conditions,f"{PwThat}*{qD}",RHS)

	def demand(self,name,conditions,nn,nnn,map_,map_3,mu,mu3,sigma2,PwThat,PwThat2,PwThat3,PbT2,qD,qD2,qS2,output=False):
		""" MNL demand """
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * exp(({PwThat2}-{PwThat})*{sigma2}) * {qD2}/ sum({nnn}$({map_3}), {mu3}*exp(({PwThat2}-{PwThat3})*{sigma2})))"""
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * exp(({PbT2}-{PwThat})*{sigma2}) * {qS2}/ sum({nnn}$({map_3}), {mu3}*exp(({PbT2}-{PwThat3})*{sigma2})))"""
		return equation(name,self.qD.doms(),conditions,qD,RHS)

class MNL_out:
	""" collection of price indices / demand systems for CET nests """
	def __init__(self,version='std',state="ID",**kwargs):
		""" Add version of the model """
		self.version = version
		self.state = state

	def add_symbols(self,db,ns_local,ns_global={},**kwargs):
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PbT','PwThat','qD','qS','mu','eta','n'):
			setattr(self,sym,db[df(sym,ns_global)])
		for sym in ['out']:
			setattr(self, self.state + "_" + sym, db[df(self.state + "_" + sym, ns_global)])
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
		eta2,out2,out3 = self.a('eta',[(0,1)]),self.a(self.state + "_" + 'out',[(0,1)]),self.a(self.state + "_" + 'out',[(0,2)])
		map_,map_2,map_3 = self.a('map_'),self.a('map_',[(0,1),(1,0)]), self.a('map_',[(0,2)])
		PwThat,PwThat2,PwThat3 = self.a('PwThat'), self.a('PwThat',[(0,1)]), self.a('PwThat',[(0,2)])
		PbT,PbT2,PbT3 = self.a('PbT'),self.a('PbT',[(0,1)]),self.a('PbT',[(0,2)])
		qD,qD2 = self.a('qD'),self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'),self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_{name}",conditions['zp'],nn,map_2,out2,qD,qD2,qS2,PbT2,PwThat,PwThat2)+'\n\t'
		text += self.demand(f"E_q_out_{name}",conditions['q_out'],nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwThat,PwThat2,PwThat3,PbT,PbT3,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}",conditions['q_nout'],nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwThat,PwThat2,PwThat3,PbT,PbT3,output=False)
		return text

	def demand(self,name,conditions,nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwThat,PwThat2,PwThat3,PbT,PbT3,output=False):
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * exp(({PwThat}-{PwThat2})*(-{eta2}))*{qD2}/(sum({nnn}$({map_3} and {out3}), {mu3}*exp(({PbT3}-{PwThat2})/(-{eta2})))+sum({nnn}$({map_3} and not {out3}), {mu3}*exp(({PwThat3}-{PwThat2})*(-{eta2})))))"""
			return equation(name,self.qD.doms(),conditions,qD,RHS)
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * exp(({PbT}-{PwThat2})*(-{eta2}))*{qD2}/(sum({nnn}$({map_3} and {out3}), {mu3}*exp(({PbT3}/{PwThat2})/(-{eta2})))+sum({nnn}$({map_3} and not {out3}), {mu3}*exp(({PwThat3}-{PwThat2})*(-{eta2})))))"""
			return equation(name,self.qS.doms(),conditions,qS,RHS)

	def zero_profit(self,name,conditions,nn,map_2,out2,qD,qD2,qS2,PbT2,PwThat,PwThat2):
		RHS = f"""sum({nn}$({map_2} and {out2}), {qS2}*{PbT2})+sum({nn}$({map_2} and not {out2}), {qD2}*{PwThat2})"""
		return equation(name,self.PwThat.doms(),conditions,f"{PwThat}*{qD}",RHS)


class linear_out:
	""" collection of price indices / demand systems for CET nests """
	def __init__(self,version='std',state="ID",**kwargs):
		""" Add version of the model """
		self.version = version
		self.state = state

	def add_symbols(self,db,ns_local,ns_global={},**kwargs):
		for sym in ['map_']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PbT','PwThat','qD','qS','mu','n'):
			setattr(self,sym,db[df(sym,ns_global)])
		for sym in ['out']:
			setattr(self, self.state + "_" + sym, db[df(self.state + "_" + sym, ns_global)])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns_tree):
		self.conditions = {'q_nout': db[ns_tree['knots']].write(), 'q_out': db[ns_tree['bra_o']].write(),'zp': db[ns_tree['bra_no']].write()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		nn,nnn = self.a('n',[(0,1)]), self.a('n',[(0,2)])
		mu,mu2,mu3 = self.a('mu'), self.a('mu',[(0,1), (1,0)]), self.a('mu',[(0,2)])
		out2,out3 = self.a(self.state + "_" + 'out',[(0,1)]),self.a(self.state + "_" + 'out',[(0,2)])
		map_,map_2,map_3 = self.a('map_'),self.a('map_',[(0,1),(1,0)]), self.a('map_',[(0,2)])
		PwThat,PwThat2,PwThat3 = self.a('PwThat'), self.a('PwThat',[(0,1)]), self.a('PwThat',[(0,2)])
		PbT,PbT2,PbT3 = self.a('PbT'),self.a('PbT',[(0,1)]),self.a('PbT',[(0,2)])
		qD,qD2 = self.a('qD'),self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'),self.a('qS',[(0,1)])
		text = self.zero_profit(f"E_zp_{name}",conditions['zp'],nn,map_,mu,PwThat2,PwThat)+'\n\t'
		# text += self.demand(f"E_q_out_{name}",conditions['q_out'],nn,nnn,map_,map_3,mu,mu3,out3,eta2,qD,qD2,qS,PwThat,PwThat2,PwThat3,PbT,PbT3,output=True)+'\n\t'
		text += self.demand(f"E_q_nout_{name}",conditions['q_nout'],nn,map_2,mu2,qD,qD2,output=False)
		return text

	def demand(self,name,condition,nn,map_2,mu2,qD,qD2,output=False):
		if output is False:
			RHS = f"""sum({nn}$({map_2}), {qD2}/{mu2}) """
			return equation(name,self.qD.doms(),condition,qD,RHS)

	def zero_profit(self,name,conditions,nn,map_,mu,PwThat2,PwThat):
		RHS = f"""sum({nn}$({map_}), {mu}*{PwThat2}) """
		return equation(name,self.PwThat.doms(),conditions,f"{PwThat}",RHS)

class ID_sum:
	""" Defines os and qsumX"""
	def __init__(self):
		pass
	def add_symbols(self,db,ns):
		[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('n','ID_e2t','ID_e2u','ID_u2t','ID_e2ai','ID_e2ai2i','ID_i2t','qsumX','os','qD')];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}
	def add_conditions(self):
		self.conditions = {'os': self.ID_e2t.write(),'qsumX': self.ID_e2ai.write()}
	def a(self,attr,lot_indices=[],l='',lag={}):
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)
	def run(self,name):
		nnn,nnnn = self.a('n',[(0,2)]), self.a('n',[(0,3)])
		e2t,e2t_2 = self.a('ID_e2t'), self.a('ID_e2t',[(1,3)])
		e2u_2 = self.a('ID_e2u',[(1,2)])
		qD_2,qD_3 = self.a('qD',[(0,1)]),self.a('qD',[(0,2)])
		u2t_2 = self.a('ID_u2t',[(0,2)])
		e2ai2i = self.a('ID_e2ai2i')
		i2t_2 = self.a('ID_i2t',[(0,2),(1,3)])
		os_2 = self.a('os',[(1,3)])
		text = self.e_os(f"E_ID_os_{name}", self.conditions['os'],nnn,e2u_2,u2t_2,qD_2,qD_3)+'\n\t'
		text += self.e_qsumX(f"E_ID_qsumX_{name}", self.conditions['qsumX'],nnn,nnnn,e2ai2i,e2t_2,i2t_2,qD_3,os_2)
		return text
	def e_os(self,name,conditions,nnn,e2u_2,u2t_2,qD_2,qD_3):
		RHS = f"""sum({nnn}$({e2u_2} and {u2t_2}), {qD_3})/{qD_2}"""
		return equation(name,self.os.doms(),conditions,self.os.write(),RHS)
	def e_qsumX(self,name,conditions,nnn,nnnn,e2ai2i,e2t_2,i2t_2,qD_3,os_2):
		RHS = f""" sum([{nnn},{nnnn}]$({e2ai2i} and {e2t_2} and {i2t_2}), {qD_3}*{os_2})"""
		return equation(name,self.qsumX.doms(),conditions,self.qsumX.write(),RHS)

class ID_emissions:
	def __init__(self):
		pass
	def add_symbols(self,db,ns):
		[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('n','z','ai','ID_inp','phi','qD','M0','PwT','PwThat','pMhat', "ID_i2ai")];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}
	def add_conditions(self):
		self.conditions = {'M0': '', 'PwThat': self.ID_inp.write()}
	def a(self,attr,lot_indices=[],l='',lag={}):
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)
	def run(self,name):
		text = self.e_M0(f"E_M0_{name}", self.conditions['M0'],self.a('n'),self.a('z'),self.a('ai'),self.a('phi'),self.a('qD'))+'\n\t'
		text += self.e_PwThat(f"E_ID_PwThat_{name}", self.conditions['PwThat'],self.a('n'),self.a('z'),self.a('phi', [(0,1)]),self.a('PwT'),self.a('pMhat'), self.a("ID_i2ai"), self.a("n",[(0,1)]))
		return text
	def e_M0(self,name,conditions,n,z,ai,phi,qD):
		#return equation(name,self.M0.doms(),conditions,self.M0.write(),f"""1""")
		return equation(name,self.M0.doms(),conditions,self.M0.write(),f"""sum({n}$({ai}), {phi}*{qD})""")
	def e_PwThat(self,name,conditions,n,z,phi,PwT,pMhat, i2ai, nn):
		#return equation(name,self.PwThat.doms(),conditions,self.PwThat.write(),f"""1""")
		return equation(name,self.PwThat.doms(),conditions,self.PwThat.write(),f"""{PwT}+sum({z}, sum({nn}$({i2ai}), {phi}*{pMhat}))""")

class aggregates:
	def __init__(self,state='ID'):
		self.state = state
	def add_symbols(self,db,ns):
		if self.state == 'ID':
			[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('n','z','ai','ID_i2ai','qD','pM','pMhat')];
		elif self.state == 'EOP':
			[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('n','z','ai','ID_i2ai','EOP_i2ai','m2c','qD','pM','pMhat','PbT','theta','muG','sigmaG')];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}
	def add_conditions(self):
		self.conditions = {'qD': self.ai.write(), 'pMhat': ''}
	def a(self,attr,lot_indices=[],l='',lag={}):
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)
	def run(self,name):
		if self.state == 'ID':
			text = self.e_qD(f"E_aggqD_ID_{name}", self.conditions['qD'], self.a('n',[(0,1)]), self.a('ID_i2ai',[(0,1),(1,0)]), self.a('qD',[(0,1)]))+'\n\t'
			text += self.e_pMhat_ID(f"E_pMhat_ID_{name}", self.conditions['pMhat'])
		elif self.state == 'EOP':
			text = self.e_qD_EOP(f"E_aggqD_EOP_{name}", self.conditions['qD'], self.a('n',[(0,1)]), self.a('ID_i2ai',[(0,1),(1,0)]), self.a('EOP_i2ai',[(0,1),(1,0)]), self.a('qD',[(0,1)]))+'\n\t'
			text += self.e_pMhat_EOP(f"E_pMhat_EOP_{name}",self.conditions['pMhat'],self.a('n'),self.a('m2c'),self.a('pM'),self.a('theta'),self.a('PbT'),self.a('muG'),self.a('sigmaG'))
		return text
	def e_qD(self,name,conditions,nn,i2ai_2,qD_2):
		return equation(name,self.qD.doms(),conditions,self.qD.write(),f"""sum({nn}$({i2ai_2}), {qD_2})""")
	def e_qD_EOP(self,name,conditions,nn,ID_i2ai_2,EOP_i2ai_2, qD_2):
		return equation(name,self.qD.doms(),conditions,self.qD.write(),f"""sum({nn}$({ID_i2ai_2} or {EOP_i2ai_2}), {qD_2})""")
	def e_pMhat_ID(self,name,conditions):
		return equation(name,self.pMhat.doms(), conditions, self.pMhat.write(),self.pM.write())
	def e_pMhat_EOP(self,name,conditions,n,m2c,pM,theta,PbT,muG,sigmaG):
		RHS = f"""{pM}+sum({n}$({m2c}), {theta}*(errorf(({pM}-{PbT}+{muG})/{sigmaG})*({PbT}-{pM}-{muG})-{sigmaG}*@std_pdf(({pM}-{PbT}+{muG})/{sigmaG})))"""
		return equation(name,self.pMhat.doms(),conditions,self.pMhat.write(),self.pM.write())

class currentapplications:
	def __init__(self):
		pass
	def add_symbols(self,db,ns):
		[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('n','ID_e2t','ID_e2u','map_ID_CU','map_ID_EC','bra_ID_TU','bra_ID_BU','kno_ID_TU','ID_u2t','sigma','mu','gamma_tau','PwThat','qD','currapp','s_uc','currapp_mod')];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}
	def add_conditions(self):
		self.conditions = {'currapp_ID': self.ID_e2t.write()+' and '+self.a('kno_ID_TU',[(0,1)]),
							 'share_uc': self.map_ID_CU.write()+' and '+self.bra_ID_TU.write(),
						  'currapp_mod': self.ID_e2t.write()+' and '+self.a('kno_ID_TU',[(0,1)])}
	def a(self,attr,lot_indices=[],l='',lag={}):
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)
	def run(self,name):
		nnn,nnnn,nnnnn = self.a('n',[(0,2)]), self.a('n',[(0,3)]), self.a('n',[(0,4)])
		ID_e2u_2, ID_e2u_3 = self.a('ID_e2u',[(1,2)]), self.a('ID_e2u',[(0,3),(1,0)])
		ID_e2t = self.a('ID_e2t')
		ID_u2c_2,ID_u2c_3 = self.a('map_ID_CU',[(0,2)]), self.a('map_ID_CU',[(0,2),(1,3)])
		ID_tu_3, ID_bu_3 = self.a('bra_ID_TU',[(0,2)]), self.a('bra_ID_BU',[(0,2)])
		ID_u2t_2, ID_u2t_3,ID_u2t_4 = self.a('ID_u2t',[(1,4)]), self.a('ID_u2t',[(0,2),(1,4)]), self.a('ID_u2t',[(0,2)])
		ID_c2e_2 = self.a('map_ID_EC',[(0,3),(1,0)])
		sigma_2 = self.a('sigma',[(0,1)])
		mu, mu_2 = self.a('mu'), self.a('mu',[(0,2)])
		gamma_tau_2 = self.a('gamma_tau',[(0,3),(1,4)])
		P, P_2, P_3, P_5 = self.a('PwThat'), self.a('PwThat',[(0,1)]), self.a('PwThat',[(0,2)]), self.a('PwThat',[(0,4)])
		qD, qD_3, qD_4 = self.a('qD'), self.a('qD',[(0,2)]), self.a('qD',[(0,3)])
		s_uc_2 = self.a('s_uc',[(0,2),(1,3)])
		text = self.e_currapp(f"E_currapp_ID_{name}", self.conditions['currapp_ID'], nnn, ID_u2t_4,ID_e2u_2, qD, qD_3, self.currapp) +'\n\t'
		text += self.e_s_uc(f"E_share_uc_{name}", self.conditions['share_uc'], nnn, nnnn, nnnnn, ID_u2c_2, ID_tu_3, ID_bu_3, ID_e2u_3, ID_u2t_2, ID_u2t_3, sigma_2, mu, mu_2, gamma_tau_2, P, P_2, P_3, P_5,self.s_uc)+'\n\t'
		text += self.e_currapp_mod(f"E_currapp_mod_{name}", self.conditions['currapp_mod'],nnn,nnnn,ID_u2t_4,ID_c2e_2,ID_u2c_3,s_uc_2,qD,qD_4,self.currapp_mod)
		return text
	def e_currapp(self,name,conditions,nnn,u2t_4,e2u_2,qD,qD_3,currapp):
		RHS = f"""sum({nnn}$({u2t_4} and {e2u_2}), {qD_3})/{qD}"""
		return equation(name,currapp.doms(),conditions,currapp.write(),RHS)
	def e_s_uc(self,name,conditions,nnn,nnnn,nnnnn,u2c_2,tu_3,bu_3,e2u_3,u2t_2,u2t_3,sigma_2,mu,mu_2,gamma_tau_2,P,P_2,P_3,P_5,s_uc):
		RHS = f"""{mu}*exp(({P_2}-{P})*{sigma_2})/(
	sum({nnn}$({u2c_2} and {tu_3}), {mu_2}*exp(({P_2}-{P_3})*{sigma_2}))+
	sum({nnn}$({u2c_2} and {bu_3}), {mu_2}*exp({sigma_2}*({P_2}-sum({nnnn}$({e2u_3}), sum({nnnnn}$({u2t_2}), {gamma_tau_2})*sum({nnnnn}$({u2t_3}), {P_5})))))
	)"""
		return equation(name,s_uc.doms(), conditions, s_uc.write(),RHS)
	def e_currapp_mod(self,name,conditions,nnn,nnnn,u2t_4,c2e_2,u2c_3,s_uc_2,qD,qD_4,currapp_mod):
		RHS = f"""sum([{nnn},{nnnn}]$({u2t_4} and {c2e_2} and {u2c_3}), {s_uc_2} * {qD_4}/{qD})"""
		return equation(name,currapp_mod.doms(),conditions,currapp_mod.write(),RHS)

class minimize_object:
	def __init__(self, state = 'ID'):
		self.state = state
	def add_symbols(self,db,ns):
		[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('n','map_gamma','map_ID_CU','bra_ID_TU','mu','mubar','weight_mu','gamma_tau','minobj')];
		if self.state == 'EOP':
			[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('kno_EOP_CU','muG','sigmaG','w_EOP','w_mu_EOP','muGbar','sigmaGbar')];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}
	def add_conditions(self):
		self.conditions = {'minobj': ''}
	def a(self,attr,lot_indices=[],l='',lag={}):
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)
	def run(self,name):
		n,nn = self.a('n'), self.a('n',[(0,1)])
		map_gamma, u2c,bu = self.a('map_gamma'), self.a('map_ID_CU'), self.a('bra_ID_TU')
		mu, mu_2 = self.a('mu'), self.a('mu',[(0,2),(1,3)])
		mubar, weight_mu, gamma_tau = self.a('mubar'), self.a('weight_mu'), self.a('gamma_tau')
		RHS_ID = self.e_minobj_ID_text(n,nn,map_gamma, u2c,bu,mu,mu_2,mubar,weight_mu,gamma_tau)
		if self.state == 'ID':
			return self.e_minobj(f"E_minobj_ID_{name}",self.conditions['minobj'],RHS_ID,self.minobj)
		elif self.state == 'EOP':
			RHS_EOP = self.e_minobj_EOP_text(n,self.a('kno_EOP_CU'),self.a('w_EOP'),self.a('w_mu_EOP'),self.a('muG'),self.a('muGbar'),self.a('sigmaG'),self.a('sigmaGbar'))
			return self.e_minobj(f"E_minobj_EOP_{name}",self.conditions['minobj'],RHS_ID+'+'+RHS_EOP,self.minobj)
	def e_minobj_ID_text(self,n,nn,map_gamma,u2c,bu,mu,mu_2,mubar,weight_mu,gamma_tau):
		return f"""sum({map_gamma}, Sqr({mu_2}-{gamma_tau}))+{weight_mu}*sum([{n},{nn}]$({u2c} and {bu}), Sqr({mu}-{mubar}))"""
	def e_minobj_EOP_text(self,n,kno_EOP_CU,w_EOP,w_mu_EOP,muG,muGbar,sigmaG,sigmaGbar):
		return f"""{w_EOP}*sum({n}$({kno_EOP_CU}), Sqr({muG}-{muGbar})+{w_mu_EOP}*Sqr({sigmaG}-{sigmaGbar}))"""
	def e_minobj(self,name,conditions,RHS,minobj):
		return equation(name,minobj.doms(), conditions, minobj.write(), RHS)

class currapp_EOP:
	def __init__(self):
		pass
	def add_symbols(self,db,ns):
		[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('n','m2u','m2t','map_EOP_TU','qD','M0','currapp_EOP')];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}
	def add_conditions(self):
		self.conditions = {'currapp_EOP': self.m2t.write()}
	def a(self,attr,lot_indices=[],l='',lag={}):
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)
	def run(self,name):
		return self.e_currapp_EOP(f"E_currapp_EOP_{name}", self.conditions['currapp_EOP'], self.a('n',[(0,1)]), self.a('map_EOP_TU',[(0,1),(1,0)]), self.a('m2u',[(0,1)]),self.a('qD',[(0,1)]),self.a('M0'),self.currapp_EOP)
	def e_currapp_EOP(self,name,conditions,nn,u2t_2,m2u_2,qD_2,M0,currapp_EOP):
		RHS = f"""sum({nn}$({u2t_2} and {m2u_2}), {qD_2})/{M0}"""
		return equation(name,currapp_EOP.doms(),conditions,currapp_EOP.write(),RHS)

class EOP_emissions:
	def __init__(self):
		pass
	def add_symbols(self,db,ns):
		[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('n','z','m2c','EOP_out','EOP_inp','EOP_i2ai','theta','phi','qS','qD','M0','M','pM','pMhat','PbT','PwT','PwThat','muG','sigmaG','epsi')];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}
	def add_conditions(self):
		self.conditions = {'qS': self.EOP_out.write(), 'M': '', 'PwThat': self.EOP_inp.write()}
	def a(self,attr,lot_indices=[],l='',lag={}):
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)
	def run(self,name):
		z,n,nn = self.a('z'), self.a('n'), self.a('n',[(0,1)])
		m2c,EOP_i2ai,phi_2 = self.a('m2c'), self.a('EOP_i2ai'),self.a('phi',[(0,1)])
		M0,M,theta = self.a('M0'), self.a('M'),self.a('theta')
		muG,sigmaG = self.a('muG'),self.a('sigmaG')
		pM,pMhat,PbT,PwT = self.a('pM'), self.a('pMhat'),self.a('PbT'), self.a('PwT')
		qS,epsi = self.a('qS'), self.a('epsi')
		text = self.e_qS(f"E_EOP_qS_{name}",self.conditions['qS'],z,m2c,theta,M0,pM,PbT,muG,sigmaG,epsi)+'\n\t'
		text += self.e_M(f"E_EOP_M_{name}",self.conditions['M'],n,m2c,M0,qS,epsi)+'\n\t'
		text += self.e_PwThat(f"E_EOP_PwThat_{name}",self.conditions['PwThat'],nn,z,phi_2,PwT,pMhat,EOP_i2ai)
		return text
	def e_qS(self,name,conditions,z,m2c,theta,M0,pM,PbT,muG,sigmaG,epsi):
		RHS = f"""sum({z}$({m2c}), {M0}*{theta}*errorf(({pM}-{PbT}+{muG})/{sigmaG}))+{epsi}"""
		return equation(name,self.qS.doms(),conditions,self.qS.write(),RHS)
	def e_M(self,name,conditions,n,m2c,M0,qS,epsi):
		RHS = f"""{M0}-sum({n}$({m2c}), {qS}-{epsi})"""
		return equation(name,self.M.doms(),conditions,self.M.write(),RHS)
	def e_PwThat(self,name,conditions,nn,z,phi,PwT,pMhat,i2ai):
		return equation(name,self.PwThat.doms(),conditions,self.PwThat.write(),RHS = f"""{PwT}+sum({z}, sum({nn}$({i2ai}), {phi}*{pMhat}))""")

class ict_v1:
	""" Installation costs """
	def __init__(self,s=False,**kwargs):
		self.ns = self.namespace(kwargs)
		self.sector = s

	@staticmethod
	def namespace(self,**kwargs):
		return {key: df(key,kwargs) for key in ('ic','ic_1','ic_2','ic_tvc','os')}

	def add_symbols(self,db,ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ('n','t','txE','tx0','t0','tE','dur','dur2inv','PwThat','qD','Rrate','rDepr','R_LR','g_LR','infl_LR','qS','PbT','out')];
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
		PwThat,PwThat2,PwThat2_m1 = self.a('PwThat'),self.a('PwThat',[(0,1)]), self.a('PwThat',[(0,1)],tlag='-1')
		ic, ic_1, ic_2, ic_tvc = self.a('ic'), self.a('ic_1'), self.a('ic_2'), self.a('ic_tvc')
		ic_12,ic_22 = self.a('ic_1',[(0,1)]), self.a('ic_2',[(0,1)])
		Rrate,rDepr,g,infl = self.a('Rrate'), self.a('rDepr'),self.a('g_LR'),self.a('infl_LR')
		qS, qS2 = self.a('qS'),self.a('qS',[(0,1)])
		PbT,PbT2,os,out2 = self.a('PbT'),self.a('PbT',[(0,1)]),self.a('os'), self.a('out',[(0,1)])
		out = self.law_of_motion(f"E_lom_{name}", self.conditions['lom'],qD_p1,qD,rDepr,qD2,dur2inv,nn,g)+'\n\t'
		out += self.price_capital(f"E_pk_{name}", self.conditions['pk'],PwThat,PwThat2_m1,PwThat2,qD_m1,qD2_m1,qD,qD2,Rrate,ic_1,ic_2,rDepr,nn,dur2inv,infl)+'\n\t'
		out += self.tvc_condition(f"E_Ktvc_{name}", self.conditions['Ktvc'],qD,qD_m1,ic_tvc)+'\n\t'
		out += self.outputshares(f"E_outs_{name}", self.conditions['os'],nn,qS,PbT,qS2,PbT2,os,out2)+'\n\t'
		out += self.invest_cost(f"E_instcost_{name}", self.conditions['instcost'],nn,nnn,dur2,dur2inv2,os,qS,qD2,qD3,ic,ic_12,ic_22)
		return out

	def law_of_motion(self,name,conditions,qD_p1,qD,rDepr,qD2,dur2inv,nn,g):
		RHS = f"""({qD}*(1-{rDepr})+sum({nn}$({dur2inv}), {qD2}))/(1+{g})"""
		return equation(name,self.qD.doms(),conditions,qD_p1,RHS)

	def price_capital(self,name,conditions,PwThat,PwThat2_m1,PwThat2,qD_m1,qD2_m1,qD,qD2,Rrate,ic_1,ic_2,rDepr,nn,dur2inv,infl):
		RHS = f"""sum({nn}$({dur2inv}),{Rrate}*({PwThat2_m1}/(1+{infl})+{ic_1}*({qD2_m1}/{qD_m1}-{ic_2}))+({ic_1}*0.5)*(sqr({ic_2}*{qD})-sqr({qD2}))/sqr({qD})-(1-{rDepr})*({PwThat2}+{ic_1}*({qD2}/{qD}-{ic_2})))"""
		return equation(name,self.PwThat.doms(),conditions,PwThat,RHS)

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

	def group_conditions(self,group):
		if group == 'itory_exo':
			return [{'ar1_itory': None}]

	def exo_groups(self):
		return ['itory_exo']

	def endo_groups(self):
		return []

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