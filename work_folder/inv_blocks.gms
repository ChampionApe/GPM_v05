$BLOCK M_nest 
	E_zp_out_nest[t,s,n]$(GE_out_nest[s,n] and txE[t])..	PbT[t,s,n]*qS[t,s,n] =E= sum(nn$(map_nest[s,nn,n]), qD[t,s,nn]*PwT[t,s,nn]);
	E_zp_nout_nest[t,s,n]$(kno_no_nest[s,n] and txE[t])..	PwT[t,s,n]*qD[t,s,n] =E= sum(nn$(map_nest[s,nn,n]), qD[t,s,nn]*PwT[t,s,nn]);
	E_q_out_nest[t,s,n]$(bra_o_nest[s,n] and txE[t])..	qD[t,s,n] =E= sum(nn$(map_nest[s,n,nn]), mu[s,n,nn] * (PbT[t,s,nn]/PwT[t,s,n])**(sigma[s,nn]) * qS[t,s,nn]);
	E_q_nout_nest[t,s,n]$(bra_no_nest[s,n] and txE[t])..	qD[t,s,n] =E= sum(nn$(map_nest[s,n,nn]), mu[s,n,nn] * (PwT[t,s,nn]/PwT[t,s,n])**(sigma[s,nn]) * qD[t,s,nn]);
$ENDBLOCK
$BLOCK M_inv_pw 
	E_pw_inv[t,s,n]$(GE_out[s,n] and txE[t])..	Peq[t,n] =E= (1+markup[s,n])*(PbT[t,s,n]*(1+tauLump[t,s]/sum(nn$(GE_out[s,nn]), qS[t,s,nn]*PbT[t,s,nn]))+tauS[t,s,n]+0);
$ENDBLOCK
