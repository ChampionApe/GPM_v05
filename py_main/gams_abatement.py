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

class simplesumU:
	""" Collection of equations that define a variable as the simple sum of others """
	def __init__(self, state="ID"):
		self.state = state

	def add_symbols(self, db, ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ('n', 'qsumU', 'qD')]
		[setattr(self, self.state + "_" + sym, db[df(self.state + "_" + sym, ns)]) for sym in ['sumUaggs', 'sumU2U']]
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}	

	def add_conditions(self):
		self.conditions = {'sumUaggs': getattr(self, self.state + "_" + "sumUaggs").write()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self):
		nn = self.a("n", [(0, 1)])
		sumUaggs = self.state + "_" + "sumUaggs"
		sumU2U= self.a(self.state + "_" + "sumU2U")
		qsumU= self.a("qsumU")
		qD2 = self.a("qD", [(0, 1)])
		name_sumU = "E_sumU" + "_" + self.state
		text = self.simplesum(name_sumU, self.conditions["sumUaggs"], sumUaggs, sumU2U, qsumU, qD2, nn)
		return text

	def simplesum(self, name, conditions, agg, agg2ind, qagg, qD2, nn):
		LHS = f"{qagg}"
		RHS = f"sum({nn}$({agg2ind}), {qD2})"
		return equation(name, getattr(self, agg).doms(), conditions, LHS, RHS)

class simplesumX:
	""" Collection of equations that define a variable as the simple sum of others """
	def __init__(self, state="ID"):
		self.state = state

	def add_symbols(self, db, ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ('n', 'qsumX', 'qD')]
		[setattr(self, sym, db[df(sym, ns)]) for sym in ['sumXaggs']]
		if self.state == "ID":
			[setattr(self, sym, db[df(sym, ns)]) for sym in ['ID_sumX2X']]
		elif self.state == "EOP":
			[setattr(self, sym, db[df(sym, ns)]) for sym in ['sumX2X']] #Both mappings so we can construct two blocks
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}	
		
	def add_conditions(self):
		self.conditions = {'sumXaggs': getattr(self, "sumXaggs").write()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self):
		nn = self.a("n", [(0, 1)])
		# sumXaggs = self.state + "_" + "sumXaggs"
		qsumX = self.a("qsumX")
		qD2 = self.a("qD", [(0, 1)])

		if self.state == "ID":
			ID_sumX2X = self.a("ID_sumX2X")
			text = self.simplesum("E_sumX_ID", self.conditions["sumXaggs"], ID_sumX2X, qsumX, qD2, nn)
		elif self.state == "EOP":
			sumX2X = self.a("sumX2X")
			text = self.simplesum("E_sumX", self.conditions["sumXaggs"], sumX2X, qsumX, qD2, nn)
		return text

	def simplesum(self, name, condition, agg2ind, qagg, qD2, nn):
		LHS = f"{qagg}"
		RHS = f"sum({nn}$({agg2ind}), {qD2})"
		return equation(name, self.qsumX.doms(), condition, LHS, RHS)


    #NY LIGNING SKREVET AF FRA TAVLE: 
    #E_sumXiNE[n]$(sumXinaggs[n])..   qsumX[n] = sum(nn$sumXinE2baselineinputs[n, nn], qD[nn]) + sum(nn$suMXinE2E, sum(nnn$kno_ID_TU[nnn], [sum(nnnn$map_ID_TU[nnnn, nnn] and map_U2E[nnnn, nn], 
    #                                            qD[nnnn]]/qD[nnn] * sum(nnnnn$sumXinE2X[n, nnnnn] and map_ID_TX[nnnnn, nnn], qD[nnnnn])
    #)))


class minimize_object:
	def __init__(self, state="IDcalibrate"):
		self.state = state

	def add_symbols(self,db,ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ("n", "minobj", "mu", "minobj_mu", "sigma", "minobj_sigma", "minobj_sigma_subset", "minobj_mu_subset", \
													"muG", "sigmaG", "minobj_muG", "minobj_sigmaG", "weight_sigma", "weight_mu", "EOP_out", "weight_sigmaG", "weight_muG")]
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	# def add_conditions(self):
	# 	self.conditions = {'sumUaggs': self.sumUaggs.write(), 'sumXaggs': self.sumXaggs.write()}

	def run(self):
		n, nn = self.a("n"), self.a("n", [(0,1)])
		minobj = self.a("minobj")
		mu, sigma = self.a("mu"), self.a("sigma")
		#ID
		minobj_mu, minobj_sigma = self.a("minobj_mu"), self.a("minobj_sigma")
		minobj_mu_subset = self.a("minobj_mu_subset")
		minobj_sigma_subset = self.a("minobj_sigma_subset")
		#EOP
		muG, sigmaG = self.a("muG"), self.a("sigmaG")
		minobj_muG, minobj_sigmaG = self.a("minobj_muG"), self.a("minobj_sigmaG")
		EOP_out = self.a("EOP_out")
		#Weights
		weight_mu, weight_sigma = self.a("weight_mu"), self.a("weight_sigma")
		weight_muG, weight_sigmaG = self.a("weight_muG"), self.a("weight_sigmaG")
		if self.state == "IDcalibrate":
			text = self.ID_minimize_object(n, nn, minobj, mu, sigma, minobj_mu, minobj_sigma, minobj_mu_subset, minobj_sigma_subset, weight_mu, weight_sigma)
		elif self.state == "EOPcalibrate":
			text = self.EOP_minimize_object(n, nn, minobj, mu, sigma, minobj_mu, muG, minobj_sigma, sigmaG, minobj_mu_subset, \
											EOP_out, minobj_sigma_subset, weight_mu, weight_sigma, weight_muG, weight_sigmaG, minobj_sigmaG, minobj_muG)
		return text

	def ID_minimize_object(self, n, nn, minobj, mu, sigma, minobj_mu, minobj_sigma, minobj_mu_subset, minobj_sigma_subset, weight_mu, weight_sigma):
		LHS = f"{minobj}"
		RHS = f"{weight_sigma} * sum({n}$({minobj_sigma_subset}), Sqr({sigma} - {minobj_sigma})) + {weight_mu} * sum([{n},{nn}]$({minobj_mu_subset}), Sqr({mu} - {minobj_mu}))" 
		return equation("E_ID_minobj", "", "", LHS, RHS)

	def EOP_minimize_object(self, n, nn, minobj, mu, sigma, minobj_mu, muG, minobj_sigma, sigmaG, minobj_mu_subset, \
							EOP_out, minobj_sigma_subset, weight_mu, weight_sigma, weight_muG, weight_sigmaG, minobj_sigmaG, minobj_muG):
		LHS = f"{minobj}"
		RHS = f"{weight_sigma} * sum({n}$({minobj_sigma_subset}), Sqr({sigma} - {minobj_sigma})) +\n" + \
				f"{weight_mu} * sum([{n},{nn}]$({minobj_mu_subset}), Sqr({mu} - {minobj_mu})) +\n" +\
				f"{weight_sigmaG} * sum({n}$({EOP_out}), Sqr({sigmaG} - {minobj_sigmaG})) +\n" + \
				f"{weight_muG} * sum({n}$({EOP_out}), Sqr({muG} - {minobj_muG}))"
		return equation("E_EOP_minobj", "", "", LHS, RHS)

class emission_accounts:
	def __init__(self, state="ID"):
		self.state = state

	def add_symbols(self, db, ns):
		syms = ("n", "phi", "M0", "map_M2X", "M_subset", "sumXaggs", "qsumX", "pMhat", "PwT", "PwThat", "ID_inp")
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
		sumXaggs, qsumX = self.a("sumXaggs", [(0,1)]), self.a("qsumX", [(0,1)])
		PwThat = self.a("PwThat")
		PwT = self.a("PwT")
		pMhat, pMhat2 = self.a("pMhat"), self.a("pMhat", [(0,1)])
		if self.state == "ID":
			text = self.preabatement_emissions(name, self.conditions["M_subset"], nn, phi, M0, sumXaggs, qsumX) + "\n\t"
			text += self.adjusted_inputprice(name, "ID", self.conditions["ID_PwThat"], PwThat, PwT, nn, map_M2X2, phi2, pMhat2)
		elif self.state == "EOP":
			text = self.adjusted_inputprice(name, "EOP", self.conditions["EOP_PwThat"], PwThat, PwT, nn, map_M2X2, phi2, pMhat2)
		return text

	def preabatement_emissions(self, name, condition, nn, phi, M0, sumXaggs, qsumX):
		LHS = f"{M0}"
		RHS = f"sum({nn}$({sumXaggs}), {phi}*{qsumX})"
		return equation(f"E_preabatementM_{name}", self.M0.doms(), condition, LHS, RHS)

	def adjusted_inputprice(self, name, state, condition, PwThat, PwT, nn, map_M2X, phi, pMhat):
		LHS = f"{PwThat}"
		RHS = f"{PwT} + sum({nn}$({map_M2X}), {phi} * {pMhat})"
		return equation("E_" + state + f"_adjusted_inputprice_{name}", self.PwThat.doms(), condition, LHS, RHS)

class EOP:
	def __init__(self):
		pass

	def add_symbols(self, db, ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ("n", "phi", "M", "M0", "map_M2C", "map_M2X", "M_subset", "sumXaggs", \
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