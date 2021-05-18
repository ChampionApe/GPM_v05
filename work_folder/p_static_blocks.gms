$BLOCK M_lower_nests 
	E_zp_out_lower_nests[s,n]$(out_lower_nests[s,n])..	PbT[s,n]*qS[s,n] =E= sum(nn$(map_lower_nests[s,nn,n]), qD[s,nn]*PwT[s,nn]);
	E_zp_nout_lower_nests[s,n]$(kno_no_lower_nests[s,n])..	PwT[s,n]*qD[s,n] =E= sum(nn$(map_lower_nests[s,nn,n]), qD[s,nn]*PwT[s,nn]);
	E_q_out_lower_nests[s,n]$(bra_o_lower_nests[s,n])..	qD[s,n] =E= sum(nn$(map_lower_nests[s,n,nn]), mu[s,n,nn] * (PbT[s,nn]/PwT[s,n])**(sigma[s,nn]) * qS[s,nn]);
	E_q_nout_lower_nests[s,n]$(bra_no_lower_nests[s,n])..	qD[s,n] =E= sum(nn$(map_lower_nests[s,n,nn]), mu[s,n,nn] * (PwT[s,nn]/PwT[s,n])**(sigma[s,nn]) * qD[s,nn]);
$ENDBLOCK
$BLOCK M_upper_nest 
	E_zp_out_upper_nest[s,n]$(out_upper_nest[s,n])..	PbT[s,n]*qS[s,n] =E= sum(nn$(map_upper_nest[s,nn,n]), qD[s,nn]*PwT[s,nn]);
	E_zp_nout_upper_nest[s,n]$(kno_no_upper_nest[s,n])..	PwT[s,n]*qD[s,n] =E= sum(nn$(map_upper_nest[s,nn,n]), qD[s,nn]*PwT[s,nn]);
	E_q_out_upper_nest[s,n]$(bra_o_upper_nest[s,n])..	qD[s,n] =E= sum(nn$(map_upper_nest[s,n,nn]), mu[s,n,nn] * (PbT[s,nn]/PwT[s,n])**(sigma[s,nn]) * qS[s,nn]);
	E_q_nout_upper_nest[s,n]$(bra_no_upper_nest[s,n])..	qD[s,n] =E= sum(nn$(map_upper_nest[s,n,nn]), mu[s,n,nn] * (PwT[s,nn]/PwT[s,n])**(sigma[s,nn]) * qD[s,nn]);
$ENDBLOCK
$BLOCK M_p_static_pw 
	E_pw_p_static[s,n]$(out[s,n])..	Peq[n] =E= (1+markup[s,n])*(PbT[s,n]*(1+tauLump[s]/sum(nn$(out[s,nn]), qS[s,nn]*PbT[s,nn]))+tauS[s,n]+0);
$ENDBLOCK
