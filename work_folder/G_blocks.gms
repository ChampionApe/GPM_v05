$BLOCK M_gov_G 
	E_pwt_G[t,s,n]$(d_tauD[s,n] and txE[t])..	PwT[t,s,n] =E= Peq[t,n]+tauD[t,s,n];
	E_TTREV_G[t]$(txE[t])..	TotTaxRev[t] =E= sum([s,n]$(d_tauS[s,n]), tauS[t,s,n]*qS[t,s,n])+sum([s,n]$(d_tauD[s,n]), tauD[t,s,n]*qD[t,s,n])+sum(s$(d_tauLump[s]),tauLump[t,s]);
	E_lom_G[t,s,n]$(txE[t] and gsvngs[n] and s_G[s])..	vD[t+1,s,n] =E= (vD[t,s,n]*irate[t]+TotTaxRev[t])/((1+g_LR)*(1+infl_LR));
	E_tvc_G[t,s,n]$(tE[t] and gsvngs[n] and s_G[s])..	vD[t,s,n] =E= (1+g_tvc[s,n])*vD[t-1,s,n];
$ENDBLOCK
$BLOCK M_gcalib_G 
	E_TR_G[t,s,n]$(s_tax[s] and n_tax[n] and t0[t])..	vD[t,s,n] =E= sum(nn$(d_tauS[s,nn]),tauS[t,s,nn]*qS[t,s,nn])+sum(nn$(d_tauD[s,nn]), tauD[t,s,nn]*qD[t,s,nn])+tauLump[t,s]$(d_tauLump[s]);
$ENDBLOCK
