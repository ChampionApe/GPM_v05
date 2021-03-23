$BLOCK M_HH_agg 
	E_zp_HH_agg[t,s,n]$(kno_HH_agg[s,n] and txE[t])..	PwT[t,s,n]*qD[t,s,n] =E= sum(nn$(map_HH_agg[s,nn,n] and qs_qd_HH_agg[s,nn]), qS[t,s,nn]*PbT[t,s,nn])+sum(nn$(map_HH_agg[s,nn,n] and qd_qd_HH_agg[s,nn]), qD[t,s,nn]*PwT[t,s,nn]);
	E_qout_HH_agg[t,s,n]$(qs_qd_HH_agg[s,n] and txE[t])..	qS[t,s,n] =E= sum(nn$(map_HH_agg[s,n,nn]), mu[s,n,nn] * (PwT[t,s,nn]/PbT[t,s,n])**(sigma[s,nn]) * qD[t,s,nn]);
	E_qnout_HH_agg[t,s,n]$(qd_qd_HH_agg[s,n] and txE[t])..	qD[t,s,n] =E= sum(nn$(map_HH_agg[s,n,nn]), mu[s,n,nn] * (PwT[t,s,nn]/PwT[t,s,n])**(sigma[s,nn]) * qD[t,s,nn]);
$ENDBLOCK
$BLOCK M_bdgt_HH 
	E_bdgt_HH[t,s]$(s_HH[s] and txE[t])..	sp[t,s] =E= sum(n$(out_HH[s,n]), PbT[t,s,n]*qS[t,s,n])-sum(n$(inp_HH[s,n]), PwT[t,s,n]*qD[t,s,n])-tauLump[t,s];
	E_pw_HH[t,s,n]$(out_HH[s,n] and txE[t])..	Peq[t,n] =E= PbT[t,s,n]-tauS[t,s,n];
$ENDBLOCK
$BLOCK M_HH_dyn 
	E_lom_HH[t,s,n]$(txE[t] and svngs[n] and s_HH[s])..	vD[t+1,s,n] =E= (vD[t,s,n]*irate[t]+sp[t,s])/((1+g_LR)*(1+infl_LR));
	E_euler_HH[t,s,n]$(tx0E[t] and int_temp_HH[s,n])..	qD[t,s,n] =E= qD[t-1,s,n]*(disc[s]*irate[t]*(PwT[t-1,s,n]/PwT[t,s,n])/(1+infl_LR))**(1/crra[s,n])/(1+g_LR);
	E_tvc_HH[t,s,n]$(tE[t] and svngs[n] and s_HH[s])..	vD[t,s,n] =E= (1+hh_tvc[s,n])*vD[t-1,s,n];
$ENDBLOCK
