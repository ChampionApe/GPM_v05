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

class v1:
	""" Simple setup for government sector: in general equilibrium. No balanced budget assumption."""
	def __init__(self,version='std',**kwargs):
		""" Add version of the model """
		self.version = version

	def add_symbols(self,db,ns_global={},dynamic=False):
		""" add gpy_symbols with writing methods. ns is a namespace to update symbol names if they are nonstandard """
		[setattr(self,sym,db[df(sym,ns_global)]) for sym in ('n','s','Peq','PwT','PbT','qD','qS','tauD','tauS','tauLump','TotTaxRev','d_tauD','d_tauS','d_tauLump','vD')];
		if dynamic is True:
			[setattr(self,sym,db[df(sym,ns_global)]) for sym in ('t','txE','t0','tE','tx0E','g_tvc','gsvngs','irate','g_LR','infl_LR')];
		self.aliases = {i: db.alias_dict0[self.n.name][i] for i in range(len(db.alias_dict0[self.n.name]))}

	def add_conditions(self,db,ns,dynamic=False):
		""" add gpy_symbols with writing methods. ns_tree is a namespace for relevant subsets to condition the equations on."""
		self.conditions = {'PwT': db[ns['d_tauD']].write(), 'TTRev': ''}
		self.conditions['calib_TR'] = f"{db[ns['s_tax']].write()} and {db[ns['n_tax']].write()}"
		if dynamic is True:
			self.conditions['PwT'] += ' and '+self.txE.write()
			self.conditions['TTRev'] = self.txE.write()
			self.conditions['calib_TR'] += ' and '+self.t0.write()
			self.conditions.update({'tvc': f"{db[ns['tE']].write()} and {db[ns['gsvngs']].write()} and {db[ns['s_G']].write()}",
									'lom': f"{db[ns['txE']].write()} and {db[ns['gsvngs']].write()} and {db[ns['s_G']].write()}"})

	def a(self,attr,lot_indices=[],l='',tlag=''):
		""" get the version of the symbol self.attr with alias from list of tuples with indices (lot_indices) and potentially .l added."""
		if hasattr(self,'t'):
			return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l,lag={self.t.name: tlag})
		else:
			return getattr(self,attr).write(alias=create_alias_dict(self.aliases,lot_indices),l=l)		

	def run(self,name,conditions=None,block='std'):
		conditions = self.conditions if conditions is None else conditions
		PwT, Peq = self.a('PwT'), self.a('Peq')
		qS,qS2, qD,qD2 = self.a('qS'),self.a('qS',[(0,1)]), self.a('qD'), self.a('qD',[(0,1)])
		tauD,tauD2, tauS,tauS2, tauLump = self.a('tauD'),self.a('tauD',[(0,1)]), self.a('tauS'),self.a('tauS',[(0,1)]), self.a('tauLump')
		d_tauD,d_tauD2, d_tauS,d_tauS2, d_tauLump = self.a('d_tauD'),self.a('d_tauD',[(0,1)]), self.a('d_tauS'),self.a('d_tauS',[(0,1)]), self.a('d_tauLump')
		s,n,nn = self.a('s'),self.a('n'), self.a('n',[(0,1)])
		TotTaxRev,vD = self.a('TotTaxRev'), self.a('vD')
		if block == 'std':
			text = self.pwt_eq(f"E_pwt_{name}", conditions['PwT'], PwT, Peq, tauD)+'\n\t'
			text += self.TTRev_eq(f"E_TTREV_{name}", conditions['TTRev'], TotTaxRev, tauS, tauD, tauLump, qS, qD, d_tauS, d_tauD, d_tauLump, s, n)
			if hasattr(self,'t'):
				text += '\n\t'+self.law_of_motion(f"E_lom_{name}", self.conditions['lom'],self.a('vD',tlag='+1'),vD,self.a('irate'),TotTaxRev,self.a('g_LR'),self.a('infl_LR'))+'\n\t'
				text += self.tvc_condition(f"E_tvc_{name}",self.conditions['tvc'],vD,self.a('vD',tlag='-1'),self.a('g_tvc'))
		elif block == 'calib':
			text = self.calibrate_tax_revenue(f"E_TR_{name}", self.conditions['calib_TR'], vD, qS2, qD2, tauS2, tauD2, nn, d_tauS2, d_tauD2, tauLump,d_tauLump)
		return text

	def pwt_eq(self,name,conditions,PwT,Peq,tauD):
		return equation(name,self.PwT.doms(),conditions,PwT,f"{Peq}+{tauD}")

	def TTRev_eq(self,name,conditions,TotTaxRev,tauS,tauD,tauLump,qS,qD,d_tauS,d_tauD,d_tauLump,s,n):
		RHS = f"""sum([{s},{n}]$({d_tauS}), {tauS}*{qS})+sum([{s},{n}]$({d_tauD}), {tauD}*{qD})+sum({s}$({d_tauLump}),{tauLump})"""
		return equation(name,self.TotTaxRev.doms(),conditions,TotTaxRev,RHS)

	def calibrate_tax_revenue(self,name,conditions,vD,qS2,qD2,tauS2,tauD2,nn,d_tauS2,d_tauD2,tauLump,d_tauLump):
		RHS = f"""sum({nn}$({d_tauS2}),{tauS2}*{qS2})+sum({nn}$({d_tauD2}), {tauD2}*{qD2})+{tauLump}$({d_tauLump})"""
		return equation(name,self.vD.doms(),conditions,vD,RHS)

	def law_of_motion(self,name,conditions,vD_p1,vD,irate,TotTaxRev,g,infl):
		RHS = f"""({vD}*{irate}+{TotTaxRev})/((1+{g})*(1+{infl}))"""
		return equation(name,self.vD.doms(),conditions,vD_p1,RHS)

	def tvc_condition(self,name,conditions,vD,vD_m1,g_tvc):
		RHS = f"""(1+{g_tvc})*{vD_m1}"""
		return equation(name,self.vD.doms(),conditions,vD,RHS)