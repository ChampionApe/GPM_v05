import os,io,numpy as np, pandas as pd, DataBase, excel2py, openpyxl

def clean(db,clean_data):
	for var in db.variables['variables']:
		db[var] = db.get(var)[(x not in clean_data for x in db.get(var))]
		if np.nan in clean_data:
			db[var] = db.get(var).dropna()
	return db

class read_data:
	def main(data,name=None,clean_data=[np.nan,'NA',0],components=['domestic','trade','invest'],balanced_data_check=True):
		"""Read in production values/prices/quantities from 'data', and export to 'export_to'."""
		dbs = {}
		for key in data:
			with open(data[key],"rb") as file:
				in_mem_file = io.BytesIO(file.read())
			data[key] = openpyxl.load_workbook(in_mem_file,read_only=True,data_only=True)
		dbs['domestic'] = read_data.domestic(data['Production_v'])
		if 'trade' in components:
			dbs['trade'] = read_data.read_sheet_standard(data['Production_v'],'sec_trade')
			read_data.trade_from_domestic(dbs['domestic'],dbs['trade'])
		if 'HH' in components:
			dbs['HH'] = read_data.HH(data['Production_v'])
		if 'tax' in components:
			dbs['tax'] = read_data.tax(data['Production_v'])
		if 'invest' in components:
			dbs['invest'] = read_data.read_sheet_standard(data['Production_v'],'sec_invest')
			read_data.adjust_invest(dbs['domestic'],dbs['trade'],dbs['invest'],dur2inv=None)
		db = DataBase.GPM_database(name=name)
		[db.merge_dbs(db,db_i,'first') for db_i in dbs.values()];
		clean(db,clean_data)
		db['n_equi'] = db['vS'].index.levels[-1]
		unique_outputs = read_data.unique_outputs(db)
		# Assert that data is balanced:
		if balanced_data_check is True:
			checks = read_data.data_checks(db)
			if unique_outputs is True:
				for x in checks:
					assert max(abs(checks[x].dropna()))<1e-9, f"Data is not balanced; check {x} failed."
			else:
				for x in checks:
					if x not in 'sector':
						assert max(abs(checks[x].dropna()))<1e-9, f"Data is not balanced; check {x} failed."
		db.merge_dbs(db,read_data.read_sheet_standard(data['Production_p'],'sec_goods'),'first')
		if 'invest' in components:
			db.merge_dbs(db,read_data.read_sheet_standard(data['Production_p'],'sec_invest'),'first')
		read_data.adhoc_fix_prices(db)
		clean(db,clean_data)
		# Add quantities:
		db['qD'] = pd.Series(db['vD'].rctree_pd(db['PwT'])/db.get('PwT'),name='qD')
		db['qS'] = pd.Series(db['vS'].rctree_pd(db['Peq'])/db.get('PbT'),name='qS')
		for var in db.variables['variables']:
		    dummy_name = 'd_'+var
		    db[dummy_name] = db[var].index
		read_data.tax_domains(db)
		clean(db,clean_data)
		return db

	@staticmethod
	def read_sheet_standard(data,sheet):
		db = DataBase.GPM_database(alias=pd.MultiIndex.from_tuples([('n','nn')]))
		db.merge_dbs(db,excel2py.xl2PM.pm_from_workbook(data,{sheet: 'vars'}),'second')
		db.update_sets_from_types()
		return db

	@staticmethod
	def domestic(data):
		""" Input/output table, domestic sectors/goods"""
		db_dom = DataBase.GPM_database()
		db_dom.merge_dbs(db_dom,excel2py.xl2PM.pm_from_workbook(data,{'sec_domestic': 'vars'}),'second')
		db_dom.update_sets_from_types()
		db_dom['s_prod'] = db_dom['s']
		db_dom['n_prod'] = db_dom['n']
		db_dom['n_fg'] = db_dom['n']
		return db_dom

	@staticmethod
	def trade_from_domestic(db_dom,db_trade):
		db_trade['s_for'] = db_trade.get('s')[~db_trade.get('s').isin(db_dom.get('s_prod'))]
		db_trade['n_for'] = db_trade.get('vD').index.get_level_values('n')[db_trade.get('vD').index.get_level_values('s').isin(db_dom.get('s_prod'))].unique()
		db_trade['sfor_ndom'] = db_trade.get('vD')[db_trade.get('vD').index.get_level_values('s').isin(db_trade.get('s_for'))].index
		db_trade['sfor_nfor'] = pd.MultiIndex.from_product([db_trade.get('s_for'),db_trade.get('n_for')])

	@staticmethod
	def HH(data):
		""" read in some household aggregates"""
		db_HH = DataBase.GPM_database()
		db_HH.merge_dbs(db_HH,excel2py.xl2PM.pm_from_workbook(data,{'sec_HH':'vars'}), 'second')
		db_HH.update_sets_from_types()
		db_HH['s_HH'] = db_HH['s']
		db_HH['inp_HH'] = db_HH.get('vD').index
		db_HH['out_HH'] = db_HH.get('vS').index
		return db_HH

	@staticmethod
	def tax(data):
		""" taxes """
		db_tax = DataBase.GPM_database()
		db_tax.merge_dbs(db_tax,excel2py.xl2PM.pm_from_workbook(data,{'sec_tax': 'vars'}),'second')
		db_tax.update_sets_from_types()
		db_tax['n_tax'] = db_tax['n']
		db_tax['s_tax'] = db_tax['s']
		return db_tax

	@staticmethod
	def tax_domains(data):
		data['d_tauS'] = data.get('qS').index
		data['d_tauD'] = data.get('qD').index
		if 'dur' in data.symbols:
			data['d_tauD'] = data['d_tauD'].rctree_pd({'not': data['dur']})
		data['d_tauLump'] = data['vD'].rctree_pd(data['n_tax']).droplevel(-1).index
		for s in ('s_for','s_itory'):
			if s in data.symbols:
				data['d_tauLump'] = data.get('d_tauLump').drop(data.get(s))

	@staticmethod
	def unique_outputs(db):
		if max([len(db.get('vS').index.get_level_values('n')[db.get('vS').index.get_level_values('s')==x]) for (x,y) in db.get('vS').index if x in db.get('s_prod')])==1:
			return True
		else:
			return False

	@staticmethod
	def data_checks(db):
		domestic_supply = db.get('vS')[db.get('vS').index.get_level_values('s').isin(db.get('s_prod'))]
		demand_for_domestic = db.get('vD').groupby('n').sum()
		sector_check = domestic_supply-demand_for_domestic
		goods_balance = db.get('vS').groupby('n').sum()-db.get('vD')[db.get('vD').index.get_level_values('n').isin(db.get('n_equi'))].groupby('n').sum()
		# supply_check = db.get('vS').groupby('s').sum()-db.get('vD')[~(db.get('vD').index.get_level_values('n').isin(db.get('inv').union(db.get('n_itory'))))].groupby('s').sum()
		return {'sector': sector_check, 'goods': goods_balance}

	@staticmethod
	def trade_ss(db):
		db['sfor_nfor'] = db.get('PwT')[db.get('PwT').index.get_level_values('n').isin(db.get('n_for'))].index

	@staticmethod
	def adjust_invest(db_dom,db_trade,db_invest,dur2inv=None):
		db_invest['s_itory'] = pd.Index(['itory'],name='s')
		db_invest['s_inv'] = db_invest['vD'].index.get_level_values('s')[~db_invest['vD'].index.get_level_values('s').isin(db_dom.get('s_prod').union(db_invest.get('s_itory')).union(db_trade.get('s_for')))].unique()
		db_invest['inv'] = db_invest['vS'].index.get_level_values('n')[db_invest['vS'].index.get_level_values('s').isin(db_invest.get('s_inv'))].unique()
		if dur2inv is None:
			db_invest['dur2inv'] = pd.MultiIndex.from_tuples([(x.split('I_',1)[-1],x) for x in db_invest['inv']],names=['n','nn'])
		else:
			db_invest['dur2inv'] = dur2inv
		db_invest['dur'] = pd.Index(db_invest.get('dur2inv').get_level_values(0).unique(),name='n')
		# add inventory maps:
		db_invest['itoryD'] = db_invest['vD'].index[db_invest['vD'].index.get_level_values('s').isin(db_invest.get('s_itory'))]

	@staticmethod
	def adhoc_fix_prices(db):
		""" This extends the database to include initial values that are not in IO.""" 
		db_prices = DataBase.GPM_database()
		db['d_Peq'] = db['Peq'].index
		db_prices['Peq'] = pd.Series(1, index = db.get('n'), name = 'Peq')
		db.merge_dbs(db,db_prices,'first')
		if 'n_tax' in db.symbols:
			db_prices['PwT'] = pd.Series(1, index = db['vD'].rctree_pd({'and': [db['Peq'], {'not': db['n_tax']}]}).index, name = 'PwT') * db.get('Peq')
		else:
			db_prices['PwT'] = pd.Series(1, index = db['vD'].rctree_pd(db['Peq']).index, name = 'PwT') * db.get('Peq')
		db_prices['PbT'] = pd.Series(1, index = db['vS'].rctree_pd(db['Peq']).index, name = 'PbT') * db.get('Peq')
		db.merge_dbs(db,db_prices,'first')
		return db

def PE_from_GE(db_GE,setvalue,setname='s'):
	db_new = DataBase.GPM_database()
	if 'alias_set' in db_GE.symbols and setname in db_GE.alias_dict:
		db_new['alias_set'] = db_GE.get('alias_set')[db_GE.get('alias_set')!=setname]
		db_new['alias_map2'] = db_GE.get('alias_map2')[~db_GE.get('alias_map2').isin(db_GE.alias_dict[setname])]
		db_new['alias_'] = db_GE.get('alias_')[db_GE.get('alias_').get_level_values(0)!=setname]
	if setname in db_GE.alias_dict:
		for set_ in (set(db_GE.sets['sets'])-set(db_GE.alias_dict0[setname])-set(setname)-set(['alias_set','alias_map2'])):
			db_new[set_] = db_GE[set_]
	else:
		for set_ in (set(db_GE.sets['sets'])-set(setname)-set(['alias_set','alias_map2'])):
			db_new[set_] = db_GE[set_]
	for set_ in db_GE.sets['subsets']:
		if setname not in db_GE[set_].domains:
			db_new[set_] = db_GE[set_]
	for set_ in db_GE.sets['mappings']:
		if set_!='alias_':
			db_new[set_] = db_GE.get(set_) if setname not in db_GE[set_].domains else db_GE.get(set_)[db_GE.get(set_).get_level_values(setname)==setvalue].droplevel(level=setname).unique()
	for scalar in db_GE.variables['variables']+db_GE.parameters['parameters']:
		db_new[scalar] = db_GE[scalar]
	for var in db_GE.variables['variables']+db_GE.parameters['parameters']:
		db_new[var] = db_GE[var]
		if setname in db_new[var].domains:
			if len(db_new[var].domains)==1:
				db_new[var] = {**{'vals': db_new[var].vals[setvalue], 'gtype': 'scalar_'+db_new[var].gtype}, **{key:value for key,value in db_new[var].__dict__.items() if key not in ('vals','gtype')}}
			else:
				db_new[var].vals = db_new[var].vals[db_new[var].index.get_level_values(setname)==setvalue].droplevel(setname)
	return db_new