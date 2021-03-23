$BLOCK M_gov_g_static 
	E_pwt_g_static[s,n]$(d_tauD[s,n])..	PwT[s,n] =E= Peq[n]+tauD[s,n];
	E_TTREV_g_static..	TotTaxRev =E= sum([s,n]$(d_tauS[s,n]), tauS[s,n]*qS[s,n])+sum([s,n]$(d_tauD[s,n]), tauD[s,n]*qD[s,n])+sum(s$(d_tauLump[s]),tauLump[s]);
$ENDBLOCK
$BLOCK M_gcalib_g_static 
	E_TR_g_static[s,n]$(s_tax[s] and n_tax[n])..	vD[s,n] =E= sum(nn$(d_tauS[s,nn]),tauS[s,nn]*qS[s,nn])+sum(nn$(d_tauD[s,nn]), tauD[s,nn]*qD[s,nn])+tauLump[s]$(d_tauLump[s]);
$ENDBLOCK
