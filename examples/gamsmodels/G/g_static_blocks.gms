$BLOCK M_gov_g_static 
	E_pwt_g_static[s,n]$(d_tauD[s,n])..	PwT[s,n] =E= Peq[n]+tauD[s,n];
	E_TTRev_g_static..	TotTaxRev =E= sum([s,n]$(d_tauS[s,n]), tauS[s,n]*qS[s,n])+sum([s,n]$(d_tauD[s,n]), tauD[s,n]*qD[s,n])+sum(s$(s_HH[s]),tauLump[s]);
	E_tauSprod_g_static[s,n]$(d_tauS[s,n] and not s_HH[s])..	tauS[s,n] =E= tauSflat[s,n]+tauLump[s]*PbT[s,n]/sum(nn$(d_tauS[s,nn]), qS[s,nn]*PbT[s,nn]);
	E_tauSHH_g_static[s,n]$(d_tauS[s,n] and s_HH[s])..	tauS[s,n] =E= tauSflat[s,n];
$ENDBLOCK
$BLOCK M_gcalib_g_static 
	E_TRprod_g_static[s,n]$(s_tax[s] and n_tax[n] and not s_HH[s])..	vD[s,n] =E= sum(nn$(d_tauS[s,nn]),tauS[s,nn]*qS[s,nn])+sum(nn$(d_tauD[s,nn]), tauD[s,nn]*qD[s,nn]);
	E_TRHH_g_static[s,n]$(s_HH[s] and n_tax[n])..	vD[s,n] =E= sum(nn$(d_tauS[s,nn]),tauS[s,nn]*qS[s,nn])+sum(nn$(d_tauD[s,nn]), tauD[s,nn]*qD[s,nn])+tauLump[s];
$ENDBLOCK
