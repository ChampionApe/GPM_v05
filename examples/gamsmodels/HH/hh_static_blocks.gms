$BLOCK M_HH 
	E_zp_HH[s,n]$(kno_HH[s,n])..	PwT[s,n]*qD[s,n] =E= sum(nn$(map_HH[s,nn,n] and qs_qd_HH[s,nn]), qS[s,nn]*PbT[s,nn])+sum(nn$(map_HH[s,nn,n] and qd_qd_HH[s,nn]), qD[s,nn]*PwT[s,nn]);
	E_qout_HH[s,n]$(qs_qd_HH[s,n])..	qS[s,n] =E= sum(nn$(map_HH[s,n,nn]), mu[s,n,nn] * (PwT[s,nn]/PbT[s,n])**(sigma[s,nn]) * qD[s,nn]);
	E_qnout_HH[s,n]$(qd_qd_HH[s,n])..	qD[s,n] =E= sum(nn$(map_HH[s,n,nn]), mu[s,n,nn] * (PwT[s,nn]/PwT[s,n])**(sigma[s,nn]) * qD[s,nn]);
$ENDBLOCK
$BLOCK M_bdgt_hh_static 
	E_bdgt_hh_static[s]$(s_HH[s])..	sp[s] =E= sum(n$(out_HH_agg[s,n]), PbT[s,n]*qS[s,n])-sum(n$(inp_HH_agg[s,n]), PwT[s,n]*qD[s,n])-tauLump[s];
	E_pw_hh_static[s,n]$(out_HH_agg[s,n])..	Peq[n] =E= PbT[s,n]-tauS[s,n];
$ENDBLOCK
