$BLOCK M_lower_nests 
	E_zp_out_lower_nests[t,s,n]$(out_lower_nests[s,n] and txE[t])..	PbT[t,s,n]*qS[t,s,n] =E= sum(nn$(map_lower_nests[s,nn,n]), qD[t,s,nn]*PwT[t,s,nn]);
	E_zp_nout_lower_nests[t,s,n]$(kno_no_lower_nests[s,n] and txE[t])..	PwT[t,s,n]*qD[t,s,n] =E= sum(nn$(map_lower_nests[s,nn,n]), qD[t,s,nn]*PwT[t,s,nn]);
	E_q_out_lower_nests[t,s,n]$(bra_o_lower_nests[s,n] and txE[t])..	qD[t,s,n] =E= sum(nn$(map_lower_nests[s,n,nn]), mu[s,n,nn] * (PbT[t,s,nn]/PwT[t,s,n])**(sigma[s,nn]) * qS[t,s,nn]);
	E_q_nout_lower_nests[t,s,n]$(bra_no_lower_nests[s,n] and txE[t])..	qD[t,s,n] =E= sum(nn$(map_lower_nests[s,n,nn]), mu[s,n,nn] * (PwT[t,s,nn]/PwT[t,s,n])**(sigma[s,nn]) * qD[t,s,nn]);
$ENDBLOCK
$BLOCK M_upper_nest 
	E_zp_out_upper_nest[t,s,n]$(out_upper_nest[s,n] and txE[t])..	PbT[t,s,n]*qS[t,s,n] =E= sum(nn$(map_upper_nest[s,nn,n]), qD[t,s,nn]*PwT[t,s,nn]);
	E_zp_nout_upper_nest[t,s,n]$(kno_no_upper_nest[s,n] and txE[t])..	PwT[t,s,n]*qD[t,s,n] =E= sum(nn$(map_upper_nest[s,nn,n]), qD[t,s,nn]*PwT[t,s,nn]);
	E_q_out_upper_nest[t,s,n]$(bra_o_upper_nest[s,n] and txE[t])..	qD[t,s,n] =E= sum(nn$(map_upper_nest[s,n,nn]), mu[s,n,nn] * (PbT[t,s,nn]/PwT[t,s,n])**(sigma[s,nn]) * qS[t,s,nn]);
	E_q_nout_upper_nest[t,s,n]$(bra_no_upper_nest[s,n] and txE[t])..	qD[t,s,n] =E= sum(nn$(map_upper_nest[s,n,nn]), mu[s,n,nn] * (PwT[t,s,nn]/PwT[t,s,n])**(sigma[s,nn]) * qD[t,s,nn]);
$ENDBLOCK
$BLOCK M_p_pw 
	E_pw_p[t,s,n]$(out[s,n] and txE[t])..	Peq[t,n] =E= (1+markup[s,n])*(PbT[t,s,n]*(1+tauLump[t,s]/sum(nn$(out[s,nn]), qS[t,s,nn]*PbT[t,s,nn]))+tauS[t,s,n]+ic[t,s,n]);
$ENDBLOCK
$BLOCK M_p_cf 
	E_lom_p[t,s,n]$(txE[t] and dur[n] and s_prod[s])..	qD[t+1,s,n] =E= (qD[t,s,n]*(1-rDepr[t,s,n])+sum(nn$(dur2inv[n,nn]), qD[t,s,nn]))/(1+g_LR);
	E_pk_p[t,s,n]$(tx0E[t] and dur[n] and s_prod[s])..	PwT[t,s,n] =E= sum(nn$(dur2inv[n,nn]),Rrate[t]*(PwT[t-1,s,nn]/(1+infl_LR)+ic_1[s,n]*(qD[t-1,s,nn]/qD[t-1,s,n]-ic_2[s,n]))+(ic_1[s,n]*0.5)*(sqr(ic_2[s,n]*qD[t,s,n])-sqr(qD[t,s,nn]))/sqr(qD[t,s,n])-(1-rDepr[t,s,n])*(PwT[t,s,nn]+ic_1[s,n]*(qD[t,s,nn]/qD[t,s,n]-ic_2[s,n])));
	E_Ktvc_p[t,s,n]$(tE[t] and dur[n] and s_prod[s])..	qD[t,s,n] =E= (1+ic_tvc[s,n])*qD[t-1,s,n];
	E_outs_p[t,s,n]$(out[s,n] and txE[t] and s_prod[s])..	os[t,s,n] =E= qS[t,s,n]*PbT[t,s,n]/sum(nn$(out[s,nn]), qS[t,s,nn]*PbT[t,s,nn]);
	E_instcost_p[t,s,n]$(out[s,n] and txE[t] and s_prod[s])..	ic[t,s,n] =E= (os[t,s,n]/qS[t,s,n])*sum(nn$(dur[nn]), sum(nnn$(dur2inv[nn,nnn]), ic_1[s,nn]*0.5*qD[t,s,nn]*sqr(qD[t,s,nnn]/qD[t,s,nn]-ic_2[s,nn])));
$ENDBLOCK
