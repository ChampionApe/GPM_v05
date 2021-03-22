$BLOCK M_gov_g_dynamic 
	E_pwt_g_dynamic[t,s,n]$(d_tauD[s,n] and txE[t])..	PwT[t,s,n] =E= Peq[t,n]+tauD[t,s,n];
	E_TTRev_g_dynamic[t]$(txE[t])..	TotTaxRev[t] =E= sum([s,n]$(d_tauS[s,n]), tauS[t,s,n]*qS[t,s,n])+sum([s,n]$(d_tauD[s,n]), tauD[t,s,n]*qD[t,s,n])+sum(s$(s_HH[s]),tauLump[t,s]);
	E_tauSprod_g_dynamic[t,s,n]$(d_tauS[s,n] and not s_HH[s] and txE[t])..	tauS[t,s,n] =E= tauSflat[t,s,n]+tauLump[t,s]*PbT[t,s,n]/sum(nn$(d_tauS[s,nn]), qS[t,s,nn]*PbT[t,s,nn]);
	E_tauSHH_g_dynamic[t,s,n]$(d_tauS[s,n] and s_HH[s] and txE[t])..	tauS[t,s,n] =E= tauSflat[t,s,n];
	E_lom_g_dynamic[t,s,n]$(txE[t] and gsvngs[n] and s_G[s])..	vD[t+1,s,n] =E= (vD[t,s,n]*irate[t]+TotTaxRev[t])/((1+g_LR)*(1+infl_LR));
	E_tvc_g_dynamic[t,s,n]$(tE[t] and gsvngs[n] and s_G[s])..	vD[t,s,n] =E= (1+g_tvc[s,n])*vD[t-1,s,n];
$ENDBLOCK
$BLOCK M_gcalib_g_dynamic 
	E_TRprod_g_dynamic[t,s,n]$(s_tax[s] and n_tax[n] and not s_HH[s] and t0[t])..	vD[t,s,n] =E= sum(nn$(d_tauS[s,nn]),tauS[t,s,nn]*qS[t,s,nn])+sum(nn$(d_tauD[s,nn]), tauD[t,s,nn]*qD[t,s,nn]);
	E_TRHH_g_dynamic[t,s,n]$(s_HH[s] and n_tax[n] and t0[t])..	vD[t,s,n] =E= sum(nn$(d_tauS[s,nn]),tauS[t,s,nn]*qS[t,s,nn])+sum(nn$(d_tauD[s,nn]), tauD[t,s,nn]*qD[t,s,nn])+tauLump[t,s];
$ENDBLOCK
