import DataBase
# Small scripts for investigating bugs in the code:
class compare_gmspython:
	""" collection of static methods comparing two or gmspython models"""
	@staticmethod
	def compare_endogenous(gms1, gms2):
		r = {'n_endo': {'gms1': 0, 'gms2': 0}, 'endo': {'gms1': {}, 'gms2': {}},'endo_gms1_not2': {}, 'endo_gms2_not1': {}}
		for var in gms1.model.database.variables['scalar_variables']:
			if gms1.var_endo(var) is not None:
				r['n_endo']['gms1'] += 1
				r['endo']['gms1'][var] = gms1.var_endo(var)
				if var in gms2.model.database.variables['scalar_variables'] and gms2.var_endo(var) is None:
					r['endo_gms1_not2'][var] = r['endo']['gms1'][var]
		for var in gms1.model.database.variables['variables']:
			if gms1.var_endo(var) is not None:
				r['n_endo']['gms1'] +=len(gms1.var_endo(var))
				r['endo']['gms1'][var] = gms1.var_endo(var)
				if var in gms2.model.database.variables['variables']:
					if gms2.var_endo(var) is None:
						r['endo_gms1_not2'][var] = gms1.var_endo(var)
					else:
						r['endo_gms1_not2'][var] = DataBase.gpy_symbol(gms1.var_endo(var)).rctree_pd({'not': DataBase.gpy_symbol(gms2.var_endo(var))})
				else:
					r['endo_gms1_not2'][var] = gms1.var_endo(var)
		for var in gms2.model.database.variables['scalar_variables']:
			if gms2.var_endo(var) is not None:
				r['n_endo']['gms2'] += 1
				r['endo']['gms2'][var] = gms2.var_endo(var)
				if var in gms1.model.database.variables['scalar_variables'] and gms1.var_endo(var) is None:
					r['endo_gms2_not1'][var] = r['endo']['gms2'][var]
		for var in gms2.model.database.variables['variables']:
			if gms2.var_endo(var) is not None:
				r['n_endo']['gms2'] +=len(gms2.var_endo(var))
				r['endo']['gms2'][var] = gms2.var_endo(var)
				if var in gms1.model.database.variables['variables']:
					if gms1.var_endo(var) is None:
						r['endo_gms2_not1'][var] = gms2.var_endo(var)
					else:
						r['endo_gms2_not1'][var] = DataBase.gpy_symbol(gms2.var_endo(var)).rctree_pd({'not': DataBase.gpy_symbol(gms1.var_endo(var))})
				else:
					r['endo_gms2_not1'][var] = gms2.var_endo(var)
		return r

class compare_data:
	""" small collection of static methods for comparing databases"""
	@staticmethod
	def common_index(db1,db2,var,xs=None,**kwargs):
		return DataBase.gpy_symbol(compare_data.get_db1(db1,db2,var,xs=xs,**kwargs))

	@staticmethod
	def get_db1(db1,db2,var,xs=None,**kwargs):
		return db1[var].rctree_pd(db2[var]) if xs is None else db1[var].rctree_pd(db2[var]).xs(xs,**kwargs)

	@staticmethod
	def get_db2(db1,db2,var,xs=None,**kwargs):
		return db2[var].rctree_pd(compare_data.common_index(db1,db2,var,xs=xs,**kwargs))

	@staticmethod
	def std_diagnostics_var(db1,db2,var,xs=None,figsize=(8,6),plot=True,**kwargs):
		var1,var2 = compare_data.get_db1(db1,db2,var,xs=xs,**kwargs), compare_data.get_db2(db1,db2,var,xs=xs,**kwargs)
		return {'maxdiff': max(abs(var1-var2)), 'plotdiff': (var1-var2).plot.bar(figsize=figsize) if plot is True else None}
