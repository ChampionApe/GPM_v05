from gmspython import *
import gams_abatement,global_settings
from DB2Gams import OrdSet as OS
import excel2py
from scipy.stats import norm

class abate(gmspython):
	def __init__(self,nts={},tech=None,pickle_path=None,work_folder=None,kwargs_ns={},use_EOP=False,**kwargs_gs):
		databases = None if not nts else [nts['ID'].database.copy()]
		super().__init__(module='abate',pickle_path=pickle_path,work_folder=work_folder,databases=databases,**kwargs_gs)
		if pickle_path is None:
			self.setstate('ID',init=False)
			self.init_state_from_tree(nts['ID'],tech,'ID',kwargs_ns)
			if use_EOP:
				self.setstate('EOP',init=False)
				self.init_state_from_tree(nts['EOP'],tech,'EOP',kwargs_ns)

	# ------------------ 1: Initialization  ------------------ #
	def init_state_from_tree(self,nt,tech,state,kwargs_ns):
		self.ns.update({**self.namespace_global_sets(nt,state,kwargs_ns),**self.namespace_global_variables(kwargs_ns)})
		self.ns_local.update(self.namespace_local_sets(nt))
		DataBase.GPM_database.merge_dbs(self.model.database,nt.database,'first')
		[DataBase.GPM_database.merge_dbs(self.model.database,tree.database,'first') for tree in nt.trees.values()];
		self.add_sets(tech,state,kwargs_ns)

	# ---------------- 1.1: Namespaces and sets  ------------- #
	def namespace_global_sets(self,nt,state,kwargs):
		std_sets = {s: getattr(nt,s) for s in ['n','nn','nnn','nnnn']+[state+'_'+ss for ss in ('inp','out','int','wT','map_all','kno_out','kno_inp')] if s in nt.__dict__}
		self.sector = True if hasattr(nt,'s') else False
		std_sets['z'] = df('z',kwargs) # emissions
		if self.sector:
			std_sets['s_prod'] = df('s_prod',kwargs)
		return std_sets

	def add_aliases(self,list_of_tuples,ns={}):
		self.model.database.update_alias(pd.MultiIndex.from_tuples(list_of_tuples))
		self.ns.update({k[1]:df(k[1],ns) for k in list_of_tuples}) # add to namespace

	def namespace_local_sets(self,nt):
		"""create namespace for each tree by copying attributes."""
		return {tree: {attr: nt.trees[tree].__dict__[attr] for attr in nt.trees[tree].__dict__ if attr not in set(['tree','database']).union(nt.prune_trees)} for tree in nt.trees}

	def namespace_global_variables(self,kwargs):
		"""create global namespace for variables used in partial equilibrium model. kwargs modify the names."""
		return {varname: df(varname,kwargs) for varname in self.default_variables}

	@property
	def default_variables(self):
		syms = ['PbT','PwT','PwThat','pM','pMhat','qD','qS','qsumX','M0','M','phi','os','mu','sigma','eta','currapp','s_uc','currapp_mod','gamma_tau', "scale",'epsi']
		if 'calibrate' in self.state:
			syms += self.id_calibrate_vars
		if 'EOP' in self.state:
			syms += self.eop_vars
		if self.state == 'EOP_calibrate':
			syms += self.eop_calibrate_vars
		return syms
	@property
	def id_calibrate_vars(self):
		return ['weight_mu','mubar','minobj']
	@property
	def eop_vars(self):
		return ['muG','sigmaG','currapp_EOP']
	@property
	def eop_calibrate_vars(self):
		return ['w_mu_EOP','muGbar','sigmaGbar','w_EOP','theta']

	def add_sets(self,tech,state,kwargs):
		""" Define global 'levels' mappings and subsets, e.g. all technology goods across nesting trees. """
		if state=='ID':
			self.ns.update({s: df(s,kwargs) for s in ['ID_'+ss for ss in ['t_all','ai']]})
			self.ns.update({s: df(s,kwargs) for s in ['ID_'+ss for ss in ['i2ai','i2t','u2t','e2u','e2t','e2ai2i','e2ai','mu_endoincalib','mu_exo','map_gamma']]})
			[DataBase.GPM_database.add_or_merge(self.model.database,s,'second') for s in [tech['ID']['mu'], tech['ID']['current_coverages_split_ID'], tech['PwT'], tech["ID"]["current_applications_ID"], tech["ID"]["coverage_potentials_ID"], tech["ID"]["unit_costs_ID"]]]; 
			# level sets:
			self.model.database[self.n('ID_t_all')] = self.get('kno_ID_TX').union(self.get('kno_ID_BX'))
			self.model.database[self.n('ID_i2ai')] = tech['ID']['Q2P']
			self.model.database[self.n('ai')] = tech['ID']['Q2P'].levels[1].rename(self.n('n'))
			# Mappings:
			self.model.database[self.n('ID_i2t')] = self.get('ID_map_all')[(self.get('ID_map_all').get_level_values(self.n('n')).isin(self.get('ID_inp'))) & (self.get('ID_map_all').get_level_values(self.n('nn')).isin(self.get('ID_t_all')))]
			self.model.database[self.n('ID_u2t')] = self.get('ID_map_all')[(self.get('ID_map_all').get_level_values(self.n('n')).isin(self.get('bra_ID_CU'))) & (self.get('ID_map_all').get_level_values(self.n('nn')).isin(self.get('ID_t_all')))]
			self.model.database[self.n('ID_e2u')] = DataBase_wheels.appmap(self.get('map_ID_CU'),DataBase_wheels.map_from_mi(self.get('map_ID_EC'),self.n('n'),self.n('nn')),self.n('nn')).swaplevel(0,1).set_names([self.n('n'),self.n('nn')])
			self.model.database[self.n('ID_e2t')] = DataBase_wheels.appmap(self.get('ID_e2u'),DataBase_wheels.map_from_mi(self.get('ID_u2t'),self.n('n'),self.n('nn')),self.n('nn')).unique()
			t2i2ai = DataBase_wheels.mi.add_ndmi(self.get('ID_i2t').swaplevel(0,1).set_names([self.n('n'),self.n('nn')]),tech['ID']['Q2P'].set_names([self.n('nn'),self.n('nnn')]))
			self.model.database[self.n('ID_e2ai2i')] = DataBase_wheels.appmap(t2i2ai,DataBase_wheels.map_from_mi(self.get('ID_e2t'),self.n('nn'),self.n('n')),self.n('n')).swaplevel(1,2).set_names([self.n('n'),self.n('nn'),self.n('nnn')])
			self.model.database[self.n('ID_e2ai')] = self.get('ID_e2ai2i').droplevel(self.n('nnn')).unique()
			# Define e2t2c for non-baseline technologies:
			u2t2c = DataBase_wheels.mi.add_ndmi(self.get('map_ID_TU'), self.get('map_ID_CU').set_names([self.n('n'),self.n('nnn')])).droplevel(0) # drop the U level
			e2t2c = DataBase_wheels.mi.add_ndmi(u2t2c, self.get('map_ID_EC').set_names([self.n('nnn'),self.n('nnnn')])).swaplevel(0,2).swaplevel(1,2).set_names([self.n('n'),self.n('nn'),self.n('nnn')])
			# Define u2t2c for baseline technologies:
			u2t2c_B = DataBase_wheels.mi.add_ndmi(self.get('map_ID_BU'), self.get('map_ID_CU').set_names([self.n('n'),self.n('nnn')])).set_names([self.n('nnnn'),self.n('nnnnn'),self.n('nnn')])
			# Merge the two on the level of components, drop the component level and rename sets:
			self.model.database[self.n('map_gamma')] = DataBase_wheels.mi.add_ndmi(e2t2c,u2t2c_B).droplevel(2).set_names([self.n('n'),self.n('nn'),self.n('nnn'),self.n('nnnn')])
			u2t_BaseC = self.g('map_ID_BU').rctree_pd({'not': DataBase.gpy_symbol(self.get('map_gamma').droplevel(0).droplevel(0).set_names([self.n('n'),self.n('nn')]))})
			self.model.database[self.n('ID_mu_endoincalib')] = pd.MultiIndex.from_tuples(OS.union(*[s.tolist() for s in (self.get('map_ID_EC'), self.g('map_ID_CU').rctree_pd(self.g('bra_no_ID_TU')), self.get('map_ID_BX'), self.g('map_ID_Y').rctree_pd({"not":[self.g("kno_no_ID_Y")]}), self.g('map_ID_BU').rctree_pd({'not': DataBase.gpy_symbol(u2t_BaseC)}))]), names = [self.n('n'),self.n('nn')])
			self.model.database[self.n('ID_mu_exo')] = pd.MultiIndex.from_tuples(OS.union(*[s.tolist() for s in (self.get('map_ID_TX'), self.get('map_ID_TU'), self.g('map_ID_CU').rctree_pd(self.g('bra_ID_BU')), self.g("map_ID_Y").rctree_pd(self.g("kno_no_ID_Y")), u2t_BaseC)]), names = [self.n('n'),self.n('nn')])
		elif state == 'EOP':
			self.ns.update({s: df(s,kwargs) for s in ['m2c','m2t','m2u','theta']})
			[DataBase.GPM_database.add_or_merge(self.model.database,s,'second') for s in [tech['EOP']['mu'], tech["EOP"]["current_applications_EOP"], tech["EOP"]["coverage_potentials_EOP"], tech["EOP"]["unit_costs_EOP"]]];
			self.model.database[self.n('m2c')] = pd.MultiIndex.from_tuples([(k,j) for k,v in tech['EOP']['upper_categories'].items() for j in v], names = [self.n('z'),self.n('n')])
			self.model.database[self.n('EOP_i2ai')] = tech['EOP']['Q2P']
			u2m = DataBase_wheels.appmap(self.get('map_EOP_CU'), DataBase_wheels.map_from_mi(self.get('m2c'),self.n('n'),self.n('z')),self.n('nn'))
			self.model.database[self.n('m2t')] = DataBase_wheels.appmap(u2m,DataBase_wheels.map_from_mi(self.get('map_EOP_TU'),self.n('n'),self.n('nn')),self.n('n')).unique().swaplevel(0,1).set_names([self.n('z'),self.n('n')])
			self.model.database[self.n('m2u')] = DataBase_wheels.appmap(self.get('map_EOP_CU'),DataBase_wheels.map_from_mi(self.get('m2c'),self.n('n'),self.n('z')),self.n('nn')).swaplevel(0,1).set_names([self.n('z'),self.n('n')])
			self.model.database[self.n('theta')] = tech['EOP']['coverage_potentials_EOP'].swaplevel(0,1).rename(self.n('theta'))

	def df_var(self,val,var,domain=None,scalar=False):
		return pd.Series(val, index = domain, name = self.n(var)) if not scalar else DataBase.gpy_symbol(val,**{'name': self.n(var)})

	def default_var_series(self,var):
		if var=='PbT':
			if 'ID' in self.state:
				return self.df_var(1,var,domain=self.get('ID_out'))
			elif "EOP" in self.state:
				return self.df_var(1,var,domain=self.get('ID_out').union(self.get("EOP_out")))
		elif var == 'PwT':
			if 'ID' in self.state:
				return self.df_var(1,var,domain=self.get('ID_inp'))
			elif "EOP" in self.state:
				return self.df_var(1,var,domain=self.get('ID_inp').union(self.get("EOP_inp")))
		elif var == 'PwThat':
			if 'ID' in self.state:
				return self.df_var(1,var,domain=self.get('ID_wT'))
			elif "EOP" in self.state:
				return self.df_var(1,var,domain=self.get('ID_wT').union(self.get("EOP_wT")))
		elif var in ('pM','pMhat','M','M0'):
			return self.df_var(1,var,domain=self.get('z'))
		elif var == 'qD':
			if 'ID' in self.state:
				return self.df_var(1,var,domain=self.get('ID_wT').union(self.get('ai')))
			elif "EOP" in self.state:
				return self.df_var(1,var,domain=self.get('ID_wT').union(self.get("EOP_wT")).union(self.get('ai')))
		elif var == 'qS':
			if 'ID' in self.state:
				return self.df_var(10,var,domain=self.get('ID_out'))
			elif "EOP" in self.state:
				return self.df_var(10,var,domain=self.get('ID_out').union(self.get("EOP_out")))
		elif var == 'qsumX':
			return self.df_var(1,var,domain=self.get('ID_e2ai'))
		elif var == 'phi':
			return self.df_var(0,var,domain=pd.MultiIndex.from_product([self.get('z'),self.get('ai')]))
		elif var == 'os':
			return self.df_var(0.5,var,domain=self.get('ID_e2t'))
		elif var == 'mu':
			if 'ID' in self.state:
				return self.df_var(1,var,domain=self.get('ID_map_all'))
			elif "EOP" in self.state:
				return self.df_var(1,var,domain=self.get('ID_map_all').union(self.get("EOP_map_all")))
		elif var == 'sigma':
			s = self.df_var(0.001,var,domain=self.get('ID_kno_inp'))
			if 'ID' in self.state:
				return s
			elif "EOP" in self.state:
				return pd.concat([s, self.df_var(0.001, var, domain=self.get("kno_EOP_TX")), self.df_var(2, var, domain=self.get("kno_EOP_CU"))])
		elif var == 'eta':
			s = self.df_var(-0.001,var,domain=self.get('ID_kno_out'))
			if 'ID' in self.state:
				return s
			elif "EOP" in self.state:
				return pd.concat([s, self.df_var(-2,var,domain=self.get("EOP_kno_out"))])
		elif var in ('currapp','currapp_mod','gamma_tau'):
			return self.df_var(0.5,var,domain=self.g('ID_e2t').rctree_pd(DataBase.gpy_symbol(self.get('kno_ID_TU').rename(self.n('nn')))))
		elif var in ('s_uc','mubar'):
			return self.df_var(1,var,domain=self.g('map_ID_CU').rctree_pd(self.g('bra_ID_TU')))
		elif var in ('minobj','w_EOP'):
			return self.df_var(1,var,scalar=True)
		elif var in ('muG','muGbar'):
			return self.df_var(0,var,domain=self.get('kno_EOP_CU'))
		elif var in ('sigmaG','sigmaGbar'):
			return self.df_var(1,var,domain=self.get('kno_EOP_CU'))
		elif var in ('weight_mu', 'w_mu_EOP'):
			return self.df_var(10,var,scalar=True)
		elif var == 'currapp_EOP':
			return self.df_var(0.5,var,domain=self.get('m2t'))
		elif var == 'theta':
			return self.df_var(0.1,var,domain=self.get('m2c'))
		elif var == "scale":
			if "ID" in self.state:
				return self.df_var(1, var, domain=self.get("ID_kno_inp"))
			elif "EOP" in self.state:
				return self.df_var(1, var, domain=self.get("ID_kno_inp").union(self.get("EOP_kno_inp")))
		elif var == 'epsi':
			return self.df_var(1e-6,var,scalar=True)

	def initialize_variables(self,**kwargs):
		try:
			if kwargs['check_variables'] is True:
				for var in self.default_variables:
					if self.n(var) not in self.model.database.symbols:
						self.model.database[self.n(var)] = self.default_var_series(var)
					else:
						self.model.database[self.n(var)].vals = DataBase.merge_symbols(self.get(var),self.default_var_series(var))
		except KeyError:
			for var in self.default_variables:
				if self.n(var) not in self.model.database.symbols:
					self.model.database[self.n(var)] = self.default_var_series(var)
		if 'calibrate' in self.state:
			self.model.settings.set_conf('solve',self.add_solve + "\n") # Remove if statement for debugging state

	def initialize_variables_leontief(self):
		db = DataBase.GPM_database()
		qD = (self.get("mu")[self.g("map_ID_Y").rctree_pd(self.g("bra_o_ID_Y"))] * self.get("qS")[self.get("out_ID_Y")].values).droplevel(1) #E and Y quantity
		qD = qD.append((self.g("mu").rctree_pd(self.g("bra_no_ID_Y")) * qD[self.get("kno_no_ID_Y")].values).droplevel(1)) #X under Y quantity
		qD = qD.append((self.get("mu")[self.get("map_ID_EC")] * qD[self.get("kno_ID_EC")].rename_axis(self.n('nn'))).droplevel(1)) #C quantity
		qD = qD.append((self.get("current_coverages_split_ID") * qD[self.get("kno_ID_EC")].rename_axis(self.n('nn'))).droplevel(1)) #non-baseline U quantity
		mu = DataBase_wheels.mi.add_mi_series(qD[self.get("bra_ID_TU")], self.g("map_ID_CU").rctree_pd(self.g("bra_ID_TU"))) / \
				qD[self.g("map_ID_CU").rctree_pd(self.g("bra_ID_TU")).droplevel(0).drop_duplicates()] #non baseline U share of C (mu)
		mu = mu.append(pd.Series(1, index=self.g("map_ID_CU").rctree_pd(self.g("bra_ID_BU"))).subtract(mu[self.g("map_ID_CU").rctree_pd(self.g("bra_ID_TU"))].groupby(level=1).sum(), fill_value=0)) #baseline U share of C (mu)
		assert (mu > 0).all()
		qD = qD.append((mu[self.g("map_ID_CU").rctree_pd(self.g("bra_ID_BU"))] * qD[self.get("kno_ID_CU")].rename_axis(self.n('nn'))).droplevel(1)) #baseline U quantity
		qD = qD.append(DataBase_wheels.appmap_s(qD[self.get("bra_ID_CU")], DataBase_wheels.map_from_mi(self.get("ID_u2t"), "n", "nn")).groupby(by="n").sum()) #tech and baseline tech quantities
		qD = qD.append((self.get("mu")[self.get("map_ID_TX")] * qD[self.get("kno_ID_TX")].rename_axis(self.n('nn'))).droplevel(1)) #X under non baseline techs
		mu = mu.append(pd.Series(1, index=self.get("map_ID_BU"))) #baseline tech to U shares (gamma)
		mu = mu.append(pd.Series(1, index=self.get("map_ID_BX")) / pd.Series(1, index=self.get("map_ID_BX")).groupby("nn").sum()) #baseline tech to X shares (set equal to 1/N)
		PwThat = (pd.Series(0, index=self.get("ID_i2ai")) + (self.get("phi") * self.get("pM")).droplevel(0).rename_axis(self.n('nn')).groupby("nn").sum() + self.g("PwT").rctree_pd(self.g("ai")).rename_axis(self.n('nn'))).droplevel(1) #prices of all X
		qD = qD.append((mu[self.get("map_ID_BX")] * qD[self.get("kno_ID_BX")].rename_axis(self.n('nn'))).droplevel(1)) #X under baseline tech quantity  
		PwThat = PwThat.append((pd.Series(0, index=self.get("ID_i2t").union(self.g("map_ID_Y").rctree_pd(self.g("bra_no_ID_Y")))) + qD[self.get("ID_i2t").droplevel(1).union(self.get("bra_no_ID_Y"))] * \
			PwThat[self.get("ID_i2t").droplevel(1).union(self.get("bra_no_ID_Y"))]).groupby("nn").sum() / qD[self.get("kno_ID_BX").union(self.get("kno_ID_TX")).union(self.get("kno_no_ID_Y"))]) #Price of techs, baseline techs and Y aggregate
		PwThat = PwThat.append((pd.Series(0, index=self.get("map_ID_BU").union(self.get("map_ID_TU"))) + PwThat[self.get("ID_t_all")].rename_axis(self.n('nn'))).droplevel(1)) #Prices of technology goods
		PwThat = PwThat.append((pd.Series(0, index=self.get("map_ID_CU")) + qD[self.get("bra_ID_CU")] * PwThat[self.get("bra_ID_CU")]).groupby("nn").sum() / qD[self.get("kno_ID_CU")]) #Prices of C
		PwThat = (PwThat.append((pd.Series(0, index=self.get("map_ID_EC")) + qD[self.get("bra_ID_EC")] * PwThat[self.get("bra_ID_EC")]).groupby("nn").sum() / qD[self.get("kno_ID_EC")])).rename_axis(self.n('n')) #Prices of E
		PbT = ((pd.Series(0, index=self.g("map_ID_Y").rctree_pd(self.g("bra_o_ID_Y"))) + (qD[self.get("bra_o_ID_Y")] * PwThat[self.get("bra_o_ID_Y")])).groupby("nn").sum()).rename_axis(self.n('n')) / self.get("qS") #Price of final good
		db["qD"], db["mu"], db["PwThat"], db["PbT"] = qD, mu, PwThat, PbT
		DataBase.GPM_database.merge_dbs(self.model.database,db,'second')
		if self.state == "EOP":
			db = DataBase.GPM_database()
			qS = (((pd.Series(0, index=self.get("m2c")) + self.get("pM") - (pd.Series(0, index=DataBase_wheels.appmap(self.get('map_EOP_CU'),DataBase_wheels.map_from_mi(self.get('map_EOP_TU'),self.n('n'),self.n('nn')),self.n('n'))) + self.get("unit_costs_EOP")).droplevel(0).groupby("nn").min().rename_axis("n")) / self.default_var_series("sigmaG")).apply(norm.cdf)).droplevel(0)
			scale = 1/qS
			# qS = self.df_var(10,"qS",domain=self.get('EOP_out'))
			mu = pd.Series(1, self.get("map_EOP_CU")).groupby("nn").apply(lambda x: x/len(x)) #Shares from C to U simply 1/N
			qD = (qS.rename_axis(self.n('nn')) * mu).droplevel(1) #U quantities
			qD = qD.append(DataBase_wheels.appmap_s(qD[self.get("bra_EOP_CU")], DataBase_wheels.map_from_mi(self.get("map_EOP_TU"), "n", "nn")).groupby(by="n").sum()) #tech quantities
			scale = scale.append(1/qD[self.get("kno_EOP_TU")])
			qD = qD.append((self.get("mu")[self.get("map_EOP_TX")] * qD[self.get("kno_EOP_TX")].rename_axis(self.n('nn'))).droplevel(1)) #X inputs
			PwThat = (pd.Series(0, index=self.get("EOP_i2ai")) + (self.get("phi") * self.get("pM")).droplevel(0).rename_axis(self.n('nn')).groupby("nn").sum() + self.g("PwT").rctree_pd(self.g("ai")).rename_axis(self.n('nn'))).droplevel(1) #prices of all X
			PwThat = PwThat.append(((pd.Series(0, index=self.get("map_EOP_TX")) + qD[self.get("bra_EOP_TX")] * PwThat[self.get("bra_EOP_TX")]).groupby("nn").sum() / qD[self.get("kno_EOP_TX")]).rename_axis(self.n('n'))) #Price of technologies
			PwThat = PwThat.append((pd.Series(0, index=self.get("map_EOP_TU")) + PwThat[self.get("kno_EOP_TX")].rename_axis(self.n('nn'))).droplevel(1)) #Prices of technology goods
			PbT = ((pd.Series(0, index=self.get("map_EOP_CU"), name="PbT") + qD[self.get("bra_EOP_CU")] * PwThat[self.get("bra_EOP_CU")]).groupby("nn").sum() / qS).rename_axis(self.n('n')) #Price of components
			qS.name, scale.name, qD.name, PwThat.name, PbT.name = "qS", "scale", "qD", "PwThat", "PbT"
			db["qS"], db["scale"], db["qD"], db["mu"], db["PwThat"], db["PbT"] = qS, scale, qD, mu, PwThat, PbT
			DataBase.GPM_database.merge_dbs(self.model.database,db,'second')


	def add_calib_data(self, inputIO):
		db = excel2py.xl2PM.pm_from_workbook(inputIO,{'IO': 'vars'})
		db["currapp"] = self.get("current_applications_ID").rename("currapp")
		db["qD"] = db["qD"].vals.append((self.get("coverage_potentials_ID") * db.database.get("qD").vals.rename_axis(self.n('nn'))).droplevel(1))
		if 'EOP' in self.state:
			db["currapp_EOP"] = self.get("current_applications_EOP").rename("currapp_EOP")
		DataBase.GPM_database.merge_dbs(self.model.database,db,'second')

	# ------------------ 2: Groups  ------------------ #
	def group_conditions(self,group):
		if group == 'g_ID_alwaysexo':
			return [{'sigma': self.g('ID_kno_inp'), 'mu': self.g('ID_mu_exo'), 'eta': self.g('ID_kno_out'), 'phi': self.g('ai'),
			  		 'pM': None, 'PwT': self.g('ID_inp'), 'qS': self.g('ID_out'), "scale": self.g("ID_kno_inp"), 'epsi': None}]
		elif group == 'g_ID_alwaysendo':
			return [{'PwThat': {'or': [self.g('ID_int'), self.g('ID_inp')]}, 'PbT': self.g('ID_out'), 'pMhat': None,
					'qD': {'and': [{'or': [self.g('ID_int'), self.g('ID_inp')]}, {'not': [{'or': [self.g('kno_ID_EC'), self.g('kno_ID_CU')]}]}]}, 'os': self.g('ID_e2t'),
					 'M0': None, 's_uc': {'and': [self.g('map_ID_CU'), self.g('bra_ID_TU')]}}]
		elif group == 'g_ID_endoincalib':
			return [{'mu': self.g('ID_mu_endoincalib'), 'gamma_tau': {'and': [self.g('ID_e2t'), DataBase.gpy_symbol(self.get('kno_ID_TU').rename(self.n('nn')),**{'name': self.n('kno_ID_TU')})]}}]
		elif group == 'g_ID_exoincalib':
			return [{'qD': {'or': [self.g('ai'), self.g('kno_ID_EC'), self.g('kno_ID_CU')]}, 'qsumX': self.g('ID_e2ai'),
					 'currapp': {'and': [self.g('ID_e2t'), DataBase.gpy_symbol(self.get('kno_ID_TU').rename(self.n('nn')),**{'name': self.n('kno_ID_TU')})]},
					 'currapp_mod': {'and': [self.g('ID_e2t'), DataBase.gpy_symbol(self.get('kno_ID_TU').rename(self.n('nn')),**{'name': self.n('kno_ID_TU')})]}}]
		elif group == 'g_EOP_alwaysexo':
			return [{'sigma': self.g('EOP_kno_inp'), 'mu': self.g('EOP_map_all'), 'eta': self.g('EOP_kno_out'), 'theta': self.g('m2c'),'PwT': self.g('EOP_inp'), "scale":self.g("EOP_kno_inp")}]
		elif group == 'g_EOP_alwaysendo':
			return [{'PwThat': {'or': [self.g('EOP_int'), self.g('EOP_inp')]}, 'PbT': self.g('EOP_out'), 
					 'qD': {'or': [self.g('EOP_int'), self.g('EOP_inp')]}, 'qS': self.g('EOP_out'), 'M': None}]
		elif group == 'g_EOP_endoincalib':
			return [{'muG': self.g('kno_EOP_CU'), 'sigmaG': self.g('kno_EOP_CU')}]
		elif group == 'g_EOP_exoincalib':
			return [{'currapp_EOP': self.g('m2t')}]
		elif group == 'g_minobj_alwaysendo':
			return [{'minobj': None}]
		elif group == 'g_minobj_ID_alwaysexo':
			return [{'weight_mu': None, 'mubar': {'and': [self.g('map_ID_CU'), self.g('bra_ID_TU')]}}]
		elif group == 'g_minobj_EOP_alwaysexo':
			return [{'w_EOP': None, 'w_mu_EOP': None, 'muGbar': self.g('kno_EOP_CU'),'sigmaGbar': self.g('kno_EOP_CU')}]
		# elif group == 'g_debug':
		# 	return [{'testminobj': None}] # Debugging state

	@property
	def exo_groups(self):
		n = self.model.settings.name+'_'
		gs = OS(['g_ID_alwaysexo','g_ID_endoincalib'])
		if self.state == 'ID':
			return {n+g: self.add_group(g,n=n) for g in gs}
		elif self.state == 'ID_calibrate':
			return {n+g: self.add_group(g,n=n) for g in (gs+OS(['g_ID_exoincalib','g_minobj_ID_alwaysexo'])-OS(['g_ID_endoincalib']))}
		elif self.state == 'EOP':
			return {n+g: self.add_group(g,n=n) for g in (gs+OS(['g_EOP_alwaysexo','g_EOP_endoincalib']))}
		elif self.state == 'EOP_calibrate':
			return {n+g: self.add_group(g,n=n) for g in (gs+OS(['g_EOP_alwaysexo','g_ID_exoincalib','g_minobj_ID_alwaysexo','g_minobj_EOP_alwaysexo'])-OS(['g_ID_endoincalib']))}

	@property 
	def endo_groups(self):
		n = self.model.settings.name+'_'
		gs = OS(['g_ID_alwaysendo','g_ID_exoincalib'])
		# gs += OS(['g_debug']) # debugging state
		if self.state == 'ID':
			return {n+g: self.add_group(g,n=n) for g in gs}
		elif self.state == 'ID_calibrate':
			return {n+g: self.add_group(g,n=n) for g in (gs+OS(['g_ID_endoincalib','g_minobj_alwaysendo'])-OS(['g_ID_exoincalib']))}
		elif self.state == 'EOP':
			return {n+g: self.add_group(g,n=n) for g in (gs+OS(['g_EOP_alwaysendo','g_EOP_exoincalib']))}
		elif self.state == 'EOP_calibrate':
			return {n+g: self.add_group(g,n=n) for g in (gs+OS(['g_EOP_alwaysendo','g_ID_endoincalib','g_EOP_endoincalib','g_minobj_alwaysendo'])-OS(['g_ID_exoincalib']))}

	@property
	def add_solve(self):
		if self.state in ('ID_calibrate','EOP_calibrate'):
			return self.add_bounds + f"""solve {self.model.settings.get_conf('name')} using NLP min {self.g('minobj').write()};"""
		else:
			# return f"""solve {self.model.settings.get_conf('name')} using NLP min {'testminobj'};""" # debugging state
			return None


	@property
	def add_bounds(self):
		s = f"""{self.g("mu").write(l=".lo")}$({self.g("ID_mu_endoincalib").write()}) = 0;\n""" +\
			f"""{self.g("gamma_tau").write(l=".lo")}$({self.g("ID_e2t").write()} and {self.g("kno_ID_TU").write(alias={"n":"nn"})}) = 0;\n"""
		if self.state == "EOP_calibrate":
			return s + f"""{self.g("sigmaG").write(l=".lo")}$({self.g("kno_EOP_CU").write()}) = 0;\n"""
		else:
			return s


	# --- 		4: Define blocks 		--- #
	@property
	def blocktext(self):
		blocks = {**{f"M_{tree}": self.eqtext(tree) for tree in self.ns_local if tree.startswith('ID_')},
				  **{f"M_{self.model.settings.name}_ID_sum": self.init_ID_sum(),
					 f"M_{self.model.settings.name}_ID_Em": self.init_ID_emissions(),
					 f"M_{self.model.settings.name}_ID_agg": self.init_agg('ID'),
					 f"M_{self.model.settings.name}_ID_calib_aux": self.init_ID_calib_aux()}}
		# blocks.update({f"M_testminobj": self.M_testminobj}) # debugging state
		if 'calibrate' in self.state:
			blocks[f"M_{self.model.settings.name}_ID_minobj"]= self.init_minobj('ID')
		if 'EOP' in self.state:
			blocks.update({**{f"M_{tree}": self.eqtext(tree) for tree in self.ns_local if tree.startswith('EOP_')},
						   **{f"M_{self.model.settings.name}_EOP_agg": self.init_agg('EOP'),
							  f"M_{self.model.settings.name}_EOP_Em": self.init_EOP_emissions(),
							  f"M_{self.model.settings.name}_EOP_calib_aux": self.init_EOP_calib_aux()}})
		if self.state == 'EOP_calibrate':
			blocks[f"M_{self.model.settings.name}_EOP_minobj"] = self.init_minobj('EOP')
		return blocks
	@property
	def mblocks(self):
		mblocks = OS([f"M_{tree}" for tree in self.ns_local if tree.startswith('ID_')]+[f"M_{self.model.settings.name}_"+m for m in ('ID_sum','ID_Em','ID_agg','ID_calib_aux')])
		# mblocks += OS([f"M_testminobj"]) # debugging state
		if self.state == 'ID_calibrate':
			mblocks += OS([f"M_{self.model.settings.name}_ID_minobj"])
		elif 'EOP' in self.state:
			mblocks += OS([f"M_{tree}" for tree in self.ns_local if tree.startswith('EOP_')]+[f"M_{self.model.settings.name}_"+m for m in ('EOP_agg','EOP_Em','EOP_calib_aux')])
			mblocks -= OS([f"M_{self.model.settings.name}_ID_agg"])
		if self.state == 'EOP_calibrate':
			mblocks += OS([f"M_{self.model.settings.name}_EOP_minobj"])
		return mblocks
	# @property
	# def M_testminobj(self):
	# 	return f"E_testminobject..	testminobj =E= 0;" # Debugging state
	def init_ID_sum(self):
		s = getattr(gams_abatement,'ID_sum')()
		s.add_symbols(self.model.database,self.ns)
		s.add_conditions()
		return s.run(self.model.settings.name)
	def init_ID_emissions(self):
		s = getattr(gams_abatement,'ID_emissions')()
		s.add_symbols(self.model.database,self.ns)
		s.add_conditions()
		return s.run(self.model.settings.name)
	def init_agg(self,state):
		s = getattr(gams_abatement,'aggregates')(state=state)
		s.add_symbols(self.model.database,self.ns)
		s.add_conditions()
		return s.run(self.model.settings.name)
	def init_ID_calib_aux(self):
		s = getattr(gams_abatement,'currentapplications')()
		s.add_symbols(self.model.database,self.ns)
		s.add_conditions()
		return s.run(self.model.settings.name)
	def init_EOP_calib_aux(self):
		s = getattr(gams_abatement,'currapp_EOP')()
		s.add_symbols(self.model.database,self.ns)
		s.add_conditions()
		return s.run(self.model.settings.name)
	def init_EOP_emissions(self):
		s = getattr(gams_abatement,'EOP_emissions')()
		s.add_symbols(self.model.database,self.ns)
		s.add_conditions()
		return s.run(self.model.settings.name)
	def init_minobj(self,state):
		s = getattr(gams_abatement, 'minimize_object')(state=state)
		s.add_symbols(self.model.database,self.ns)
		s.add_conditions()
		return s.run(self.model.settings.name)
	def eqtext(self,tree_name):
		tree = self.ns_local[tree_name]
		if "ID" in tree_name:
			treestate = "ID"
		elif "EOP" in tree_name:
			treestate = "EOP"
		gams_class = getattr(gams_abatement,tree['type_f'])(version=tree['version'], state=treestate)
		gams_class.add_symbols(self.model.database,tree,ns_global=self.ns)
		gams_class.add_conditions(self.model.database,tree)
		return gams_class.run(tree_name)
