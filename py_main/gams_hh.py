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

class budget:
	def __init__(self,**kwargs):
		pass

	def add_symbols(self,db,ns,sector=None,dynamic=False):
		""" add gpy_symbols with writing methods. ns is a namespace to update symbol names if they are nonstandard """
		[setattr(self,sym,db[ns[sym]]) for sym in ('n','out','inp','PwT','PbT','qD','qS','sp','tauS','tauLump','Peq')];
		if sector is not None:
			setattr(self,'s_HH',db['s_HH'])
		if dynamic is True:
			[setattr(self,sym,db[df(sym,ns)]) for sym in ('txE','t0','tE','tx0E')];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,sector=None,dynamic=False):
		self.conditions = {'sp': '' if sector is None else self.s_HH.write(), 'pw': self.out.write()}
		if dynamic is True:
			self.conditions = {key: value+' and '+self.txE.write() for key,value in self.conditions.items()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		n,out,inp = self.a('n'),self.a('out'),self.a('inp')
		PwT,PbT,qD,qS = self.a('PwT'),self.a('PbT'),self.a('qD'),self.a('qS')
		sp,tauLump= self.a('sp'),self.a('tauLump')
		out = self.surplus(f"E_bdgt_{name}",conditions['sp'],n,out,inp,PbT,PwT,qD,qS,tauLump,sp)+'\n\t'
		out += self.pricewedge(f"E_pw_{name}",conditions['pw'])
		return out

	def surplus(self,name,conditions,n,out,inp,PbT,PwT,qD,qS,tauLump,sp):
		RHS = f"""sum({n}$({out}), {PbT}*{qS})-sum({n}$({inp}), {PwT}*{qD})-{tauLump}"""
		return equation(name,self.sp.doms(),conditions,sp,RHS)

	def pricewedge(self,name,conditions):
		RHS = f"""{self.PbT.write()}-{self.tauS.write()}"""
		return equation(name,self.PbT.doms(),conditions,self.Peq.write(),RHS)

class CES:
	""" collection of price indices / demand systems for ces nests """
	def __init__(self,version='std',**kwargs):
		""" Add version of the model (currently not applied in this module)"""
		self.version = version

	def add_symbols(self,db,ns_local,ns_global={},dynamic=False):
		""" add gpy_symbols with writing methods. ns is a namespace to update symbol names if they are nonstandard """
		for sym in ['map_','qd_qd','qs_qd']:
			setattr(self,sym,db[ns_local[sym]])
		for sym in ('PwT','PbT','qD','qS','mu','sigma','n'):
			setattr(self,sym,db[df(sym,ns_global)])
		if dynamic is True:
			for sym in ('txE','t0','tE','tx0E'):
				setattr(self,sym,db[df(sym,ns_global)])
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns_tree,dynamic=False):
		""" add gpy_symbols with writing methods. ns_tree is a namespace for relevant subsets to condition the equations on."""
		self.conditions = {'zp': db[ns_tree['kno']].write(), 'q_qsqd': db[ns_tree['qs_qd']].write(), 'q_qdqd': db[ns_tree['qd_qd']].write()}
		if dynamic is True:
			self.conditions = {key: value+' and '+self.txE.write() for key,value in self.conditions.items()}

	def a(self,attr,lot_indices=[],l='',lag={}):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag=lag)

	def run(self,name,conditions=None):
		conditions = self.conditions if conditions is None else conditions
		nn,mu,sigma2 = self.a('n',[(0,1)]),self.a('mu'),self.a('sigma',[(0,1)])
		map_,map_2 = self.a('map_'),self.a('map_',[(0,1),(1,0)])
		PwT, PwT2 = self.a('PwT'), self.a('PwT',[(0,1)])
		PbT, PbT2 = self.a('PbT'), self.a('PbT',[(0,1)])
		qD,qD2 = self.a('qD'), self.a('qD',[(0,1)])
		qS,qS2 = self.a('qS'), self.a('qS',[(0,1)])
		qs_qd2, qd_qd2 = self.a('qs_qd',[(0,1)]), self.a('qd_qd',[(0,1)])
		text  = self.zero_profit(f"E_zp_{name}",conditions['zp'],nn,map_2,qs_qd2,qd_qd2,qD,qD2,qS2,PwT,PwT2,PbT2)+'\n\t'
		text += self.demand(f"E_qout_{name}",conditions['q_qsqd'],nn,map_,mu,PwT,PwT2,PbT,qD,qD2,qS,sigma2,output=True)+'\n\t'
		text += self.demand(f"E_qnout_{name}",conditions['q_qdqd'],nn,map_,mu,PwT,PwT2,PbT,qD,qD2,qS,sigma2,output=False)
		return text

	def demand(self,name,conditions,nn,map_,mu,PwT,PwT2,PbT,qD,qD2,qS,sigma2,output=False):
		""" ces demand """
		if output is False:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PwT2}/{PwT})**({sigma2}) * {qD2})"""
			return equation(name,self.qD.doms(),conditions,qD,RHS)
		else:
			RHS = f"""sum({nn}$({map_}), {mu} * ({PwT2}/{PbT})**({sigma2}) * {qD2})"""
			return equation(name,self.qS.doms(),conditions,qS,RHS)

	def zero_profit(self,name,conditions,nn,map_2,qs_qd2,qd_qd2,qD,qD2,qS2,PwT,PwT2,PbT2):
		""" zero profits condition """
		RHS = f"""sum({nn}$({map_2} and {qs_qd2}), {qS2}*{PbT2})+sum({nn}$({map_2} and {qd_qd2}), {qD2}*{PwT2})"""
		return equation(name,self.PwT.doms(),conditions,f"{PwT}*{qD}",RHS)

class ramsey:
	""" Installation costs """
	def __init__(self,s=False,**kwargs):
		self.sector = s

	def add_symbols(self,db,ns):
		[setattr(self,sym,db[ns[sym]]) for sym in ('n','t','txE','tx0','t0','tE','int_temp','svngs','s_HH','disc','irate','qD','qS','PwT','vD','sp','crra','hh_tvc','g_LR','infl_LR')];
		if self.sector is not False:
			self.ss = db[self.sector]
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns):
		self.conditions = {'lom': f"{db[ns['txE']].write()} and {db[ns['svngs']].write()} and {db[ns['s_HH']].write()}",
						 'euler': f"{db[ns['tx0E']].write()} and {db[ns['int_temp']].write()}",
						   'tvc': f"{db[ns['tE']].write()} and {db[ns['svngs']].write()} and {db[ns['s_HH']].write()}"}

	def a(self,attr,lot_indices=[],l='',tlag=''):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag={self.t.name: tlag})
		
	def run(self,name):
		vD, vD_p1, vD_m1= self.a('vD'),self.a('vD',tlag='+1'), self.a('vD',tlag='-1')
		qD, qD_m1 = self.a('qD'),self.a('qD',tlag='-1')
		PwT,PwT_m1= self.a('PwT'),self.a('PwT',tlag='-1')
		g,infl = self.a('g_LR'),self.a('infl_LR')
		irate,disc,crra,sp,hh_tvc = self.a('irate'),self.a('disc'),self.a('crra'),self.a('sp'),self.a('hh_tvc')
		out = self.law_of_motion(f"E_lom_{name}", self.conditions['lom'],vD_p1,vD,irate,sp,g,infl)+'\n\t'
		out += self.euler_opt(f"E_euler_{name}", self.conditions['euler'],qD,qD_m1,PwT,PwT_m1,disc,irate,crra,g,infl)+'\n\t'
		out += self.tvc_condition(f"E_tvc_{name}", self.conditions['tvc'],vD,vD_m1,hh_tvc)
		return out

	def law_of_motion(self,name,conditions,vD_p1,vD,irate,sp,g,infl):
		RHS = f"""({vD}*{irate}+{sp})/((1+{g})*(1+{infl}))"""
		return equation(name,self.vD.doms(),conditions,vD_p1,RHS)

	def euler_opt(self,name,conditions,qD,qD_m1,PwT,PwT_m1,disc,irate,crra,g,infl):
		RHS = f"""{qD_m1}*({disc}*{irate}*({PwT_m1}/{PwT})/(1+{infl}))**(1/{crra})/(1+{g})"""
		return equation(name,self.qD.doms(),conditions,qD,RHS)

	def tvc_condition(self,name,conditions,vD,vD_m1,hh_tvc):
		RHS = f"""(1+{hh_tvc})*{vD_m1}"""
		return equation(name,self.vD.doms(),conditions,vD,RHS)