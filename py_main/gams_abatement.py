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
	""" Defines qsumU, os and qsumX"""
	def __init__(self):
		pass
	def add_symbols(self,db,ns):
		[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('n','ID_e2t','ID_e2u','ID_u2t','ID_e2ai','ID_e2ai2i','ID_i2t','qsumU','qsumX','os','qD')];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}
	def add_conditions(self):
		self.conditions = {'qsumU': self.ID_e2t.write(), 'os': self.ID_e2t.write(),'qsumX': self.ID_e2ai.write()}
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
		text = self.e_qsumU(f"E_ID_qsumU_{name}", self.conditions['qsumU'],nnn,e2t,e2u_2,qD_3)+'\n\t'
		text += self.e_os(f"E_ID_os_{name}", self.conditions['os'],nnn,e2u_2,u2t_2,qD_2,qD_3)+'\n\t'
		text += self.e_qsumX(f"E_ID_qsumX_{name}", self.conditions['qsumX'],nnn,nnnn,e2ai2i,e2t_2,i2t_2,qD_3,os_2)
		return text
	def e_qsumU(self,name,conditions,nnn,e2t,e2u_2,qD_3):
		#RHS = "1"
		RHS = f"""sum({nnn}$({e2t} and {e2u_2}), {qD_3})"""
		return equation(name,self.qsumU.doms(),conditions,self.qsumU.write(), RHS)
	def e_os(self,name,conditions,nnn,e2u_2,u2t_2,qD_2,qD_3):
		#RHS = "1"
		RHS = f"""sum({nnn}$({e2u_2} and {u2t_2}), {qD_3})/{qD_2}"""
		return equation(name,self.os.doms(),conditions,self.os.write(),RHS)
	def e_qsumX(self,name,conditions,nnn,nnnn,e2ai2i,e2t_2,i2t_2,qD_3,os_2):
		#RHS = "1"
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
		text += self.e_PwThat(f"E_ID_PwThat_{name}", self.conditions['PwThat'],self.a('n'),self.a('z'),self.a('phi', [(0,0), (0,1)]),self.a('PwT'),self.a('pMhat'), self.a("ID_i2ai"), self.a("n",[(0,1)]))
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
		[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('n','z','ai','ID_i2ai','qD','pM','pMhat')];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}
	def add_conditions(self):
		self.conditions = {'qD': self.ai.write(), 'pMhat': ''}
	def a(self,attr,lot_indices=[],l='',lag={}):
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)
	def run(self,name):
		if self.state == 'ID':
			text = self.e_qD(f"E_aggqD_ID_{name}", self.conditions['qD'], self.a('n',[(0,1)]), self.a('ID_i2ai',[(0,1),(1,0)]), self.a('qD',[(0,1)]))+'\n\t'
			text += self.e_pMhat_ID(f"E_pMhat_ID_{name}", self.conditions['pMhat'])
		return text
	def e_qD(self,name,conditions,nn,i2ai_2,qD_2):
		return equation(name,self.qD.doms(),conditions,self.qD.write(),f"""sum({nn}$({i2ai_2}), {qD_2})""")
	def e_pMhat_ID(self,name,conditions):
		return equation(name,self.pMhat.doms(), conditions, self.pMhat.write(),self.pM.write())

class currentapplications:
	def __init__(self,state='ID'):
		self.state=state
	def add_symbols(self,db,ns):
		[setattr(self,sym,db[rK_if_KE(ns,sym)]) for sym in ('n','e2t','e2u','qD','currapp')];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}
	def add_conditions(self):
		self.conditions = {'currapp_ID': self.ID_e2t.write()}
	def a(self,attr,lot_indices=[],l='',lag={}):
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)
	def run(self,name):
		if self.state == 'ID':
			text = self.e_currapp(f"E_currapp_ID_{name}", self.conditions['currapp_ID'], self.a('n',[(0,2)]), self.a('e2t'), self.a('e2u_2',[(1,2)]), self.a('qD'),self.a('qD',[(0,2)]),self.currapp)
		return text
	def e_currapp(self,name,conditions,nnn,e2t,e2u_2,qD,qD_3,currapp):
		RHS = f"""sum({nnn}$({e2t} and {e2u_u}), {qD_3})/{qD}"""
		return equation(name,currapp.doms(),conditions,currapp.write(),RHS)

# class currentapplications:

# 	def __init__(self, state="ID"):
# 		self.state = state

# 	def add_symbols(self, db, ns):
# 		syms_in_ns = ['n', 'qsumU', 'qD', "currapp_ID", "currapp_ID_subset", "map_currapp2sumUE", "currapp_EOP", "currapp_EOP_subset", "map_currapp2sumUM", "M0"]
# 		syms_in_ns += ["mu", "currapp_ID_modified", "currapp_ID_subset", "map_currapp_ID2T", "map_currapp_ID2E", "map_U2E",  "PwThat", "sigma", "gamma_tau", "qD"]
# 		syms = ["map_ID_BU", "map_ID_CU", "map_ID_TU", "bra_no_ID_BU"]
# 		[setattr(self,sym,db[ns[sym]]) for sym in syms_in_ns]
# 		[setattr(self, sym, db[sym]) for sym in syms]
# 		# [setattr(self, self.state + "_" + sym, db[df(self.state + "_" + sym, ns)]) for sym in ['currapp_ID_subset', ]]
# 		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}	

# 	def add_conditions(self):
# 		self.conditions = {'currapp_ID': getattr(self, "currapp_ID_subset").write(), 'currapp_EOP': getattr(self, "currapp_EOP_subset").write()}

# 	def a(self,attr,lot_indices=[],l='',lag={}):
# 		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
# 		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

# 	def run(self, type_f_UC=None):
# 		nn, nnn, nnnn = self.a("n", [(0,1)]), self.a("n", [(0,2)]), self.a("n", [(0,3)])
# 		nnnnn, nnnnnn, nnnnnnn =  self.a("n", [(0,4)]), self.a("n", [(0,5)]), self.a("n", [(0,6)])
# 		currapp = self.a("currapp_" + self.state)
# 		if self.state == "ID":
# 			currapp2sumU_upper = self.a("map_currapp2sumUE")
# 		elif self.state == "EOP":
# 			currapp2sumU_upper = self.a("map_currapp2sumUM")
# 		qsumU2 = self.a("qsumU", [(0, 1)])
# 		if self.state == "ID":
# 			quant3 = self.a("qD", [(0, 2)])
# 		elif self.state == "EOP":
# 			quant3 = self.a("M0", [(0, 2)])
# 		#currapp modified

# 		currapp_ID_modified = self.a("currapp_ID_modified")
# 		map_currapp_ID2T = self.a("map_currapp_ID2T")
# 		map_currapp_ID2E = self.a("map_currapp_ID2E", [(0,0), (1,2)])
# 		map_U2E = self.a("map_U2E", [(0, 3), (1,2)])
# 		map_ID_TU = self.a("map_ID_TU", [(0, 3), (1,1)])
# 		map_ID_CU45, map_ID_CU65 = self.a("map_ID_CU", [(0,3), (1,4)]), self.a("map_ID_CU", [(0,5), (1,4)])
# 		PwThat4, PwThat5, PwThat6, PwThat7 = self.a("PwThat", [(0,3)]), self.a("PwThat", [(0,4)]), self.a("PwThat", [(0,5)]), self.a("PwThat", [(0,6)])
# 		sigma5 = self.a("sigma", [(0, 4)])
# 		bra_no_ID_BU6 = self.a("bra_no_ID_BU", [(0, 5)])
# 		gamma_tau23 = self.a("gamma_tau", [(0,1), (1,2)])
# 		map_ID_BU67 = self.a("map_ID_BU", [(0, 5), (1,6)])
# 		qD3, qD5 = self.a("qD", [(0, 2)]), self.a("qD", [(0, 4)])
# 		mu45, mu65 = self.a("mu", [(0,3), (1,4)]), self.a("mu", [(0,5), (1,4)])
		
# 		name = "E_currentapplications_" + self.state
# 		doms = getattr(self, "currapp_" + self.state).doms()
# 		text = self.currentapplication(name, self.conditions["currapp_" + self.state], doms, currapp, nn, nnn, currapp2sumU_upper, qsumU2, quant3)
# 		if self.state == "ID":
# 			text += "\n\t" + self.eq_currapp_modified(type_f_UC, currapp_ID_modified, nn, nnn, map_currapp_ID2T, map_currapp_ID2E, nnnn, map_U2E, map_ID_TU, nnnnn, map_ID_CU45, mu45, PwThat5, PwThat4, sigma5, \
# 										nnnnnn, map_ID_CU65, bra_no_ID_BU6, mu65, PwThat6, gamma_tau23, nnnnnnn, map_ID_BU67, PwThat7, qD5, qD3)
# 		return text

# 	def currentapplication(self, name, condition, doms, currapp, nn, nnn, currapp2sumU_upper, qsumU2, quant3):
# 		LHS = f"{currapp}"
# 		RHS = f"sum([{nn}, {nnn}]$({currapp2sumU_upper}), {qsumU2}/{quant3})"
# 		return equation(name, doms, condition, LHS, RHS)

# 	def eq_currapp_modified(self, type_f_UC, currapp_ID_modified, nn, nnn, map_currapp_ID2T, map_currapp_ID2E, nnnn, map_U2E, map_ID_TU, nnnnn, map_ID_CU45, mu4, PwThat5, PwThat4, sigma5, \
# 							nnnnnn, map_ID_CU65, bra_no_ID_BU6, mu65, PwThat6, gamma_tau23, nnnnnnn, map_ID_BU67, PwThat7, qD5, qD3):
# 		LHS = f"""{currapp_ID_modified}"""
# 		if type_f_UC == "MNL":
# 			RHS = f" sum({nn}$({map_currapp_ID2T}), sum({nnn}$({map_currapp_ID2E}), sum({nnnn}$({map_U2E} and {map_ID_TU}), sum({nnnnn}$({map_ID_CU45}), ({mu4} * \n" + \
# 				  f" exp(({PwThat5} - {PwThat4})*{sigma5})) / (sum({nnnnnn}$({map_ID_CU65} and not {bra_no_ID_BU6}), {mu65} * exp(({PwThat5} - {PwThat6}) * {sigma5})) + \n"  + \
# 				  f" sum({nnnnnn}$({map_ID_CU65} and {bra_no_ID_BU6}), {mu65} * exp(({PwThat5} - ({gamma_tau23} * sum({nnnnnnn}$({map_ID_BU67}), {PwThat7}))) * {sigma5}))) * \n" + \
# 				  f" ({qD5}/{qD3})))))"
# 		else:
# 			RHS = f""" NOOOOOO """
# 			#f"""sum({nn}$({map_}), {mu} * exp(({PbT2}-{PwThat})*{sigma2}) * {qS2}/ sum({nnn}$({map_3}), {mu3}*exp(({PbT2}-{PwThat3})*{sigma2})))"""
# 		return equation("E_currapp_modified", self.currapp_ID_modified.doms(), self.conditions["currapp_ID"], LHS, RHS)

class sumXinE:
	def __init__(self):
		pass

	def add_symbols(self, db, ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ('n', 'nn', 'nnn', 'nnnn', 'nnnnn', 'qsumX', 'qD', 'map_sumXinE2baselineinputs', \
												   'sumXinEaggs', 'map_sumXinE2E','map_U2E', 'map_sumXinE2X')]

		[setattr(self, sym, db[sym]) for sym in ('kno_ID_TU', 'map_ID_TU', 'map_ID_TX')] #lavet dårligt, bruger ikke namespace lige pt.
		# [setattr(self, sym, db[df(sym, ns)]) for sym in ['sumXinEaggs', 'sumXrestaggs']]
		# if self.state == "ID":
		# 	[setattr(self, sym, db[df(sym, ns)]) for sym in ['map_sumXrest2X_ID']]
		# elif self.state == "EOP":
		# 	[setattr(self, sym, db[df(sym, ns)]) for sym in ['map_sumXrest2X']] #Both mappings so we can construct two blocks
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}
		
	def add_conditions(self):
		self.conditions = {'sumXinEaggs': getattr(self, "sumXinEaggs").write()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self):
		nn, nnn, nnnn, nnnnn = self.a("n", [(0, 1)]), self.a("n", [(0, 2)]), self.a("n", [(0, 3)]), self.a("n", [(0, 4)])
		
		qsumX = self.a("qsumX")
		map_sumXinE2baselineinputs = self.a("map_sumXinE2baselineinputs")
		qD2, qD3, qD4, qD5 = self.a("qD", [(0, 1)]), self.a("qD", [(0, 2)]), self.a("qD", [(0, 3)]), self.a("qD", [(0, 4)])
		map_sumXinE2E = self.a("map_sumXinE2E")
		kno_ID_TU = self.a("kno_ID_TU", [(0, 2)])
		map_ID_TU = self.a("map_ID_TU", [(0, 3), (1, 2)])
		map_U2E = self.a("map_U2E", [(0, 3)])
		map_sumXinE2X = self.a("map_sumXinE2X", [(0, 0), (1, 4)])
		map_ID_TX = self.a("map_ID_TX", [(0, 4), (1, 2)])

		text = self.sumXinE("E_sumXinE", self.conditions["sumXinEaggs"], qsumX, nn, map_sumXinE2baselineinputs, \
							qD2, map_sumXinE2E, nnn, kno_ID_TU, nnnn, map_ID_TU, map_U2E, qD4, qD3, nnnnn, map_sumXinE2X, map_ID_TX, qD5)
		return text

	def sumXinE(self, name, condition, qsumX, nn, map_sumXinE2baselineinputs, qD2, map_sumXinE2E, nnn, kno_ID_TU, nnnn, map_ID_TU, map_U2E, qD4, qD3, nnnnn, map_sumXinE2X, map_ID_TX, qD5):
		LHS = f"{qsumX}"
		RHS = f"sum({nn}$({map_sumXinE2baselineinputs}), {qD2})"
		RHS += f" + sum({nn}$({map_sumXinE2E}), sum({nnn}$({kno_ID_TU}), sum({nnnn}$({map_ID_TU} and {map_U2E}), {qD4}) / {qD3} * sum({nnnnn}$({map_sumXinE2X} and {map_ID_TX}), {qD5})))"
		return equation(name, self.qsumX.doms(), condition, LHS, RHS)

	#E_sumXiNE[n]$(sumXinEaggs[n])..   qsumX[n] = sum(nn$sumXinE2baselineinputs[n, nn], qD[nn]) + sum(nn$suMXinE2E[n, nn], sum(nnn$kno_ID_TU[nnn], [sum(nnnn$map_ID_TU[nnnn, nnn] and map_U2E[nnnn, nn], 
	#                                            qD[nnnn]]/qD[nnn] * sum(nnnnn$sumXinE2X[n, nnnnn] and map_ID_TX[nnnnn, nnn], qD[nnnnn])

class simplesumX:
	""" Collection of equations that define a variable as the simple sum of others """
	def __init__(self, state="ID"):
		self.state = state

	def add_symbols(self, db, ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ('n', 'qsumX', 'qD')]
		[setattr(self, sym, db[df(sym, ns)]) for sym in ['sumXinEaggs', 'sumXrestaggs']]
		if self.state == "ID":
			[setattr(self, sym, db[df(sym, ns)]) for sym in ['map_sumXrest2X_ID']]
		elif self.state == "EOP":
			[setattr(self, sym, db[df(sym, ns)]) for sym in ['map_sumXrest2X_EOP']] #Both mappings so we can construct two blocks
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}	
		
	def add_conditions(self):
		self.conditions = {'sumXrestaggs': getattr(self, "sumXrestaggs").write()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self):
		nn = self.a("n", [(0, 1)])
		# sumXaggs = self.state + "_" + "sumXaggs"
		qsumX = self.a("qsumX")
		qD2 = self.a("qD", [(0, 1)])

		if self.state == "ID":
			sumXrest2X_ID = self.a("map_sumXrest2X_ID")
			text = self.simplesum("E_sumX_ID", self.conditions["sumXrestaggs"], sumXrest2X_ID, qsumX, qD2, nn)
		elif self.state == "EOP":
			sumXrest2X_EOP = self.a("map_sumXrest2X_EOP")
			text = self.simplesum("E_sumX", self.conditions["sumXrestaggs"], sumXrest2X_EOP, qsumX, qD2, nn)
		return text

	def simplesum(self, name, condition, agg2ind, qagg, qD2, nn):
		LHS = f"{qagg}"
		RHS = f"sum({nn}$({agg2ind}), {qD2})"
		return equation(name, self.qsumX.doms(), condition, LHS, RHS)

class minimize_object:
	def __init__(self, state="IDcalibrate"):
		self.state = state

	def add_symbols(self,db,ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ("n", "minobj", "mu", "mubar", "map_ID_nonBUC", "map_ID_TC", "map_ID_BUC", \
													"currapp_ID_modified", "currapp_ID_subset", "map_U2E", "PwThat", \
													"sigma", "gamma_tau", "qD", \
													"muG", "sigmaG", "minobj_muG", "minobj_sigmaG", "weight_mu", "EOP_out", "weight_sigmaG", "weight_muG")]
		[setattr(self, sym, db[sym]) for sym in ['kno_no_ID_TX', "map_ID_BU", "map_ID_CU", "map_ID_TU", "bra_no_ID_BU", "map_ID_EC"]] #lavet dårligt, bruger ikke namespace lige pt.
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def add_conditions(self):
		self.conditions = {'currapp_ID': getattr(self, "currapp_ID_subset").write()}

	def run(self):
		n, nn, nnn, nnnn = self.a("n"), self.a("n", [(0,1)]), self.a("n", [(0,2)]), self.a("n", [(0,3)])
		nnnnn, nnnnnn, nnnnnnn =  self.a("n", [(0,4)]), self.a("n", [(0,5)]), self.a("n", [(0,6)])
		minobj = self.a("minobj")
		mu, mu34 = self.a("mu"), self.a("mu", [(0,2), (1,3)])
		# mu4, mu65 = self.a("mu", [(0,3), (1,4)]), self.a("mu", [(0,5), (1,4)])
		#ID
		map_ID_nonBUC = self.a("map_ID_nonBUC")
		kno_no_ID_TX = self.a("kno_no_ID_TX")
		map_ID_TC = self.a("map_ID_TC")
		map_ID_BUC3 = self.a("map_ID_BUC", [(0,2), (1,1)])
		map_ID_BU4 = self.a("map_ID_BU", [(0, 2), (1,3)])
		gamma_tau15 = self.a("gamma_tau", [(0,0), (1,4)])
		mubar = self.a("mubar")
		map_ID_EC25 = self.a("map_ID_EC", [(0, 1), (1,4)])
		#gamma_tau is implicitly defined
		# currapp_ID_modified = self.a("currapp_ID_modified")
		# map_currapp2TE = self.a("map_currapp2TE")
		# map_U2E = self.a("map_U2E", [(0, 3), (1,2)])
		# map_ID_TU = self.a("map_ID_TU", [(0, 3), (1,1)])
		# map_ID_CU45, map_ID_CU65 = self.a("map_ID_CU", [(0,3), (1,4)]), self.a("map_ID_CU", [(0,5), (1,4)])
		# PwThat4, PwThat5, PwThat6, PwThat7 = self.a("PwThat", [(0,3)]), self.a("PwThat", [(0,4)]), self.a("PwThat", [(0,5)]), self.a("PwThat", [(0,6)])
		# sigma5 = self.a("sigma", [(0, 4)])
		# bra_no_ID_BU6 = self.a("bra_no_ID_BU", [(0, 5)])
		# gamma_tau2 = self.a("gamma_tau", [(0,1)])
		# map_ID_BU67 = self.a("map_ID_BU", [(0, 5), (1,6)])
		# qD3, qD5 = self.a("qD", [(0, 2)]), self.a("qD", [(0, 4)])

		# minobj_mu, minobj_sigma = self.a("minobj_mu"), self.a("minobj_sigma")
		# minobj_mu_subset = self.a("minobj_mu_subset")
		# minobj_sigma_subset = self.a("minobj_sigma_subset")
		#EOP
		muG, sigmaG = self.a("muG"), self.a("sigmaG")
		minobj_muG, minobj_sigmaG = self.a("minobj_muG"), self.a("minobj_sigmaG")
		EOP_out = self.a("EOP_out")
		#Weights
		weight_mu = self.a("weight_mu")
		weight_muG, weight_sigmaG = self.a("weight_muG"), self.a("weight_sigmaG")
		# if self.state == "IDcalibrate":
		# 	text = self.ID_minimize_object(n, nn, minobj, mu, weight_mu, weight_sigma)
		if self.state == "EOPcalibrate":
			text = self.EOP_minimize_object(n, nn, minobj, mu, kno_no_ID_TX, map_ID_TC, nnn, map_ID_BUC3, nnnn, map_ID_BU4, mu34, nnnnn, map_ID_EC25, map_ID_nonBUC, mubar, gamma_tau15, \
											muG, sigmaG, EOP_out, weight_mu, weight_muG, weight_sigmaG, minobj_sigmaG, minobj_muG)
			# text += self.eq_currapp_modified(type_f_UC, currapp_ID_modified, nn, nnn, map_currapp2TE, nnnn, map_U2E, map_ID_TU, nnnnn, map_ID_CU45, mu4, PwThat5, PwThat4, sigma5, \
			# 								 nnnnnn, map_ID_CU65, bra_no_ID_BU6, mu65, PwThat6, gamma_tau2, nnnnnnn, map_ID_BU67, PwThat7, qD5, qD3)
		return text

	# def ID_minimize_object(self, n, nn, minobj, mu, weight_mu, weight_sigma):
	# 	LHS = f"{minobj}"
	# 	RHS = f"{weight_sigma} * sum({n}$({minobj_sigma_subset}), Sqr({sigma} - {minobj_sigma})) + {weight_mu} * sum([{n},{nn}]$({minobj_mu_subset}), Sqr({mu} - {minobj_mu}))" 
	# 	return equation("E_ID_minobj", "", "", LHS, RHS)

	# def eq_currapp_modified(self, type_f_UC, currapp_ID_modified, nn, nnn, map_currapp2TE, nnnn, map_U2E, map_ID_TU, nnnnn, map_ID_CU45, mu4, PwThat5, PwThat4, sigma5, \
	# 						nnnnnn, map_ID_CU65, bra_no_ID_BU6, mu65, PwThat6, gamma_tau2, nnnnnnn, map_ID_BU67, PwThat7, qD5, qD3):
	# 	LHS = f"""{currapp_ID_modified}"""
	# 	if type_f_UC == "MNL":
	# 		RHS = f" sum([{nn}, {nnn}]$({map_currapp2TE}), sum({nnnn}$({map_U2E} and {map_ID_TU}), sum({nnnnn}$({map_ID_CU45}), ({mu4} * \n" + \
	# 			  f" exp(({PwThat5} - {PwThat4})*{sigma5})) / (sum({nnnnnn}$({map_ID_CU65} and not {bra_no_ID_BU6}), {mu65} * exp(({PwThat5} - {PwThat6}) * {sigma5})) + \n"  + \
	# 			  f" sum({nnnnnn}$({map_ID_CU65} and {bra_no_ID_BU6}), {mu65} * exp(({PwThat5} - ({gamma_tau2} * sum({nnnnnnn}$({map_ID_BU67}), {PwThat7}))) * {sigma5}))) * \n" + \
	# 			  f" ({qD5}/{qD3}))))"
	# 	else:
	# 		RHS = f""" NOOOOOO """
	# 		#f"""sum({nn}$({map_}), {mu} * exp(({PbT2}-{PwThat})*{sigma2}) * {qS2}/ sum({nnn}$({map_3}), {mu3}*exp(({PbT2}-{PwThat3})*{sigma2})))"""
	# 	return equation("E_currapp_modified", self.currapp_ID_modified.doms(), self.conditions["currapp_ID"], LHS, RHS)

	def EOP_minimize_object(self, n, nn, minobj, mu, kno_no_ID_TX, map_ID_TC, nnn, map_ID_BUC3, nnnn, map_ID_BU4, mu34, nnnnn, map_ID_EC25, map_ID_nonBUC, mubar, gamma_tau15, \
							muG, sigmaG, EOP_out, weight_mu, weight_muG, weight_sigmaG, minobj_sigmaG, minobj_muG):
		LHS = f"{minobj}"
		RHS = f"sum({n}$({kno_no_ID_TX}), sum({nn}$({map_ID_TC}), Sqr(sum({nnn}$({map_ID_BUC3}), sum({nnnn}$({map_ID_BU4}), {mu34})) - sum({nnnnn}$({map_ID_EC25}), {gamma_tau15})) ) ) + " + \
				f"{weight_mu} * sum([{n},{nn}]$({map_ID_nonBUC}), Sqr({mu} - {mubar})) + " +\
				f"{weight_sigmaG} * sum({n}$({EOP_out}), Sqr({sigmaG} - {minobj_sigmaG})) + " + \
				f"{weight_muG} * sum({n}$({EOP_out}), Sqr({muG} - {minobj_muG}))"
		return equation("E_EOP_minobj", "", "", LHS, RHS)

class emission_accounts:
	def __init__(self, state="ID"):
		self.state = state

	def add_symbols(self, db, ns):
		syms = ("n", "phi", "M0", "map_M2X", "M_subset", "sumXinEaggs", "qsumX", "pMhat", "PwT", "PwThat", "ID_inp", "sumXrestaggs")
		if self.state == "EOP":
			syms += ("EOP_inp",)
		[setattr(self,sym,db[ns[sym]]) for sym in syms]
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def add_conditions(self):
		self.conditions = {'M_subset': self.M_subset.write(), "ID_PwThat":self.ID_inp.write()}
		if self.state == "EOP":
			self.conditions["EOP_PwThat"] = self.EOP_inp.write()

	def run(self, name):
		n, nn = self.a("n"), self.a("n", [(0,1)])
		phi, phi2 = self.a("phi"), self.a("phi", [(0,1), (1,0)])
		M0 = self.a("M0")
		# M02 = self.a("M0", [(0,1)])
		# M = self.a("M")
		map_M2X2 = self.a("map_M2X", [(0,1), (1,0)])
		#, M_subset = , self.a("M_subset")
		# map_M2C, map_M2C2 = self.a("map_M2C"), self.a("map_M2C", [(0,1), (1,0)])
		# qS, qS2 = self.a("qS"), self.a("qS", [(0,1)])
		# theta, theta2 = self.a("theta"), self.a("theta", [(0,1)])
		# pM, pM2 = self.a("pM"), self.a("pM", [(0,1)])
		# PbT, PbT2 = self.a("PbT"), self.a("PbT", [(0,1)])
		# muG, muG2 = self.a("muG"), self.a("muG", [(0,1)])
		# sigmaG, sigmaG2 = self.a("sigmaG"), self.a("sigmaG", [(0,1)])
		sumXinEaggs, sumXrestaggs = self.a("sumXinEaggs", [(0,1)]), self.a("sumXrestaggs", [(0,1)]) 
		qsumX = self.a("qsumX", [(0,1)])
		PwThat = self.a("PwThat")
		PwT = self.a("PwT")
		pMhat, pMhat2 = self.a("pMhat"), self.a("pMhat", [(0,1)])
		if self.state == "ID":
			text = self.preabatement_emissions(name, self.conditions["M_subset"], nn, phi, M0, sumXinEaggs, qsumX, sumXrestaggs) + "\n\t"
			text += self.adjusted_inputprice(name, "ID", self.conditions["ID_PwThat"], PwThat, PwT, nn, map_M2X2, phi2, pMhat2)
		elif self.state == "EOP":
			text = self.adjusted_inputprice(name, "EOP", self.conditions["EOP_PwThat"], PwThat, PwT, nn, map_M2X2, phi2, pMhat2)
		return text

	def preabatement_emissions(self, name, condition, nn, phi, M0, sumXinEaggs, qsumX, sumXrestaggs):
		LHS = f"{M0}"
		RHS = f"sum({nn}$({sumXinEaggs}), {phi}*{qsumX}) + sum({nn}$({sumXrestaggs}), {phi}*{qsumX})"
		return equation(f"E_preabatementM_{name}", self.M0.doms(), condition, LHS, RHS)

	def adjusted_inputprice(self, name, state, condition, PwThat, PwT, nn, map_M2X, phi, pMhat):
		LHS = f"{PwThat}"
		RHS = f"{PwT} + sum({nn}$({map_M2X}), {phi} * {pMhat})"
		return equation("E_" + state + f"_adjusted_inputprice_{name}", self.PwThat.doms(), condition, LHS, RHS)

class EOP:
	def __init__(self):
		pass

	def add_symbols(self, db, ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ("n", "phi", "M", "M0", "map_M2C", "map_M2X", "M_subset", \
													"qsumX", "qS", "theta", "muG", "sigmaG", "pM", "PbT", "EOP_out", "pMhat", "PwT", "PwThat")]
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def add_conditions(self):
		self.conditions = {'M_subset': self.M_subset.write(), "C_subset":self.EOP_out.write()}

	def run(self, name):
		n, nn = self.a("n"), self.a("n", [(0,1)])
		# phi, phi2 = self.a("phi"), self.a("phi", [(0,1), (1,0)])
		M0, M02 = self.a("M0"), self.a("M0", [(0,1)])
		M = self.a("M")
		# map_M2X2, M_subset = self.a("map_M2X", [(0,1), (1,0)]), self.a("M_subset")
		map_M2C, map_M2C2 = self.a("map_M2C"), self.a("map_M2C", [(0,1), (1,0)])
		qS, qS2 = self.a("qS"), self.a("qS", [(0,1)])
		theta, theta2 = self.a("theta"), self.a("theta", [(0,1)])
		pM, pM2 = self.a("pM"), self.a("pM", [(0,1)])
		PbT, PbT2 = self.a("PbT"), self.a("PbT", [(0,1)])
		muG, muG2 = self.a("muG"), self.a("muG", [(0,1)])
		sigmaG, sigmaG2 = self.a("sigmaG"), self.a("sigmaG", [(0,1)])
		# sumXaggs, qsumX = self.a("sumXaggs", [(0,1)]), self.a("qsumX", [(0,1)])
		# PwThat = self.a("PwThat")
		# PwT = self.a("PwT")
		pMhat = self.a("pMhat")
		text = self.postabatement_emissions(name, self.conditions["M_subset"], nn, M0, M, map_M2C, qS2) + "\n\t"
		text += self.endogenous_abatementC(name, self.conditions["C_subset"], qS, nn, M02, map_M2C2, theta, pM2, PbT, muG, sigmaG) + "\n\t"
		text += self.adjusted_emission_price(name, self.conditions["M_subset"], pMhat, pM, nn, map_M2C, theta2, PbT2, muG2, sigmaG2)
		return text
	
	def adjusted_emission_price(self, name, condition, pMhat, pM, nn, map_M2C, theta, PbT, muG, sigmaG):
		LHS = f"{pMhat}"
		RHS = f"{pM}*(1 - sum({nn}${map_M2C}, {theta} * errorf( ({pM} - {PbT} + {muG}) / ({sigmaG})))) + \n sum({nn}${map_M2C}, {theta} * errorf( ({pM} - {PbT} + {muG}) / ({sigmaG})) * ({PbT} + {muG} - Sqr({sigmaG}) * (@std_pdf(({pM} - {PbT} - {muG})/{sigmaG}) / errorf(({pM} - {PbT} - {muG})/{sigmaG}))))"
		return equation(f"E_adjusted_emission_price_{name}", self.pMhat.doms(), condition, LHS, RHS)

	def postabatement_emissions(self, name, condition, nn, M0, M, map_M2C, qS):
		LHS = f"{M}"
		RHS = f"{M0} - sum({nn}${map_M2C}, {qS})"
		return equation(f"E_postabatementM_{name}", self.M.doms(), condition, LHS, RHS)

	def endogenous_abatementC(self, name, condition, qS, nn, M0, map_M2C, theta, pM, PbT, muG, sigmaG):
		LHS = f"{qS}"
		RHS = f"sum({nn}${map_M2C}, {M0} * {theta} * errorf(({pM} - {PbT} + {muG})/({sigmaG})))"
		return equation(f"E_endogenous_abatementC_{name}", self.qS.doms(), condition, LHS, RHS)

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