import DataBase, pandas as pd

def append_index_with_1dindex(index1,index2):
	"""
	index1 is a pandas index/multiindex. index 2 is a pandas index (not multiindex).
	Returns a pandas multiindex with the cartesian product of elements in (index1,index2). 
	NB: If index1 is a sparse multiindex, the cartesian product of (index1,index2) will keep this structure.
	"""
	return pd.MultiIndex.from_tuples([a+(b,) for a in index1 for b in index2],names=index1.names+index2.names) if isinstance(index1,pd.MultiIndex) else pd.MultiIndex.from_tuples([(a,b) for a in index1 for b in index2],names=index1.names+index2.names)

def prepend_index_with_1dindex(index1,index2):
	return pd.MultiIndex.from_tuples([(b,)+a for a in index1 for b in index2],names=index2.names+index1.names) if isinstance(index1,pd.MultiIndex) else pd.MultiIndex.from_tuples([(b,a) for a in index1 for b in index2],names=index2.names+index1.names)

def slice_in_and_out(all_,exceptions=[],add_to_specific=None):
	all_ = all_ if type(all_) is set else set(all_)
	all_ = all_ if add_to_specific is None else all_.intersection(set(add_to_specific))
	return all_-set(exceptions)

def repeat_variable_windex(var,index):
	if index.name not in var.index.names:
		return pd.concat({i: var for i in index},names=index.names)
	else:
		return var

class mi:
	""" small collection of multiindex operations """
	@staticmethod
	def map_v1(mi1,mi2,level=None,verify_integrity=False):
		""" swap level of multiindex by mapping from second multiindex. the name"""
		if type(level) is str:
			mi_map = {k:v for k,v in mi2}
			return mi1.set_levels([x if x not in mi_map else mi_map[x] for x in mi1.levels[mi1.names.index(level)]],level=level,verify_integrity=verify_integrity)
		elif type(level) is int:
			mi_map = {k:v for k,v in mi2}
			return mi1.set_levels([x if x not in mi_map else mi_map[x] for x in mi1.levels[level]],level=level,verify_integrity=verify_integrity)
		elif level is None:
			level = [x for x in mi1.names if x in mi2.names][0]
			mi_map = {k:v for k,v in mi2.swaplevel(i=level,j=0)}
			return mi1.set_levels([x if x not in mi_map else mi_map[x] for x in mi1.levels[mi1.names.index(level)]],level=level,verify_integrity=verify_integrity)

	@staticmethod 
	def v1_series(s,mi_map,level=None,**kwargs):
		return pd.Series(s.values,index = mi.map_v1(s.index,mi_map),name=s.name)

	@staticmethod
	def map_v2(mi1,mi2,level=None,name=None):
		""" Replace level of multiindex from mapping mi2. The name of the index level is updated as well."""
		if type(level) is str:
			mi_map = {k:v for k,v in mi2}
			name = [name] if name is not None else [n for n in mi2.names if n!=level]
		elif type(level) is int:
			mi_map = {k:v for k,v in mi2}
			name = [name] if name is not None else [mi2.names[n] for n in range(len(mi2.names)) if n!=level]
		elif level is None:
			level = [x for x in mi1.names if x in mi2.names][0]
			name = [name] if name is not None else [n for n in mi2.names if n!=level]
			mi_map = {k:v for k,v in mi2.swaplevel(i=level,j=0)}
		return pd.MultiIndex.from_tuples(zip(*([mi1.get_level_values(x) for x in mi1.droplevel(level).names]+[a])),names=mi1.droplevel(level).names+name)

class small_updates:
	"""
	Collection of auxiliary database methods. 
	"""
	@staticmethod
	def set_values(db,set_,ns,inplace=True):
		full_map = {x: x if x not in ns else ns[x] for x in db[set_]}
		for set_i in db.alias_all(set_):
			if set_i in db.symbols:
				db[set_i].vals = db[set_i].vals.map(full_map).unique()
			for set_ij in db.sets['subsets']:
				if set_i in db[set_ij].domains:
					db[set_ij].vals = db[set_ij].vals.map(full_map).unique()
			for map_ij in db.sets['mappings']:
				if set_i in db[map_ij].domains:
					db[map_ij].vals = db[map_ij].vals.set_levels(db[map_ij].vals.levels[db[map_ij].domains.index(set_i)].map(full_map),level=set_i,verify_integrity=False)
			for var in db.variables['variables']+db.parameters['parameters']:
				if set_i in db[var].domains:
					if len(db[var].domains)==1:
						db[var].vals.index = db[var].index.map(full_map)
					else:
						db[var].vals.index = db[var].index.set_levels(db[var].index.levels[db[var].domains.index(set_i)].map(full_map),level=set_i,verify_integrity=False)
		return db

	@staticmethod
	def add_index_to_sets(db,index_,exceptions=[],add_to_specific = None,prepend=True):
		all_ = slice_in_and_out(db.sets['subsets']+db.sets['mappings'],exceptions=exceptions,add_to_specific=add_to_specific)
		for set_ in all_:
			db[set_] = prepend_index_with_1dindex(db[set_].vals,index_) if prepend is True else append_index_with_1dindex(db[set_].vals,index_)
		return db

	@staticmethod
	def add_index_to_variables(db,index_,exceptions=[],add_to_specific = None):
		for var in slice_in_and_out(db.variables['variables']+db.parameters['parameters'],exceptions=exceptions,add_to_specific=add_to_specific):
			db[var].index = prepend_index_with_1dindex(db[var].index,index_)
		for scalar in slice_in_and_out(db.variables['scalar_variables'],exceptions=exceptions,add_to_specific=add_to_specific):
			db[scalar] = pd.Series(db.vals, index = index_,name=scalar)
		for scalar in slice_in_and_out(db.variables['scalar_parameters'],exceptions=exceptions,add_to_specific=add_to_specific):
			db[scalar] = DataBase.gpy_symbol(pd.Series(db[scalar].vals,index = index_,name=scalar),**{'gtype':'parameter'})

	@staticmethod
	def subset_db(db,index_,exceptions=[],add_to_specific=None):
		""" Only keep values from index_ """
		db[index_.name].vals = db.get(index_.name)[db.get(index_.name).isin(index_)] # subset the set itself
		for sym in slice_in_and_out(db.sets['subsets']+db.sets['mappings'],exceptions=exceptions,add_to_specific=add_to_specific):
			if index_.name in db[sym].domains:
				db[sym].vals = db.get(sym)[db.get(sym).get_level_values(index_.name).isin(index_)].unique()
		for sym in slice_in_and_out(db.parameters['parameters']+db.variables['variables'],exceptions=exceptions,add_to_specific=add_to_specific):
			if index_.name in db[sym].domains:
				db[sym].vals = db.get(sym)[db.get(sym).index.get_level_values(index_.name).isin(index_)]
		return db