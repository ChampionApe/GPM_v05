$BLOCK M_T_inp 
	E_zp_out_T_inp[n]$(out_T_inp[n])..	PbT[n]*qS[n] =E= sum(nn$(map_T_inp[nn,n]), qD[nn]*PwT[nn]);
	E_zp_nout_T_inp[n]$(kno_no_T_inp[n])..	PwT[n]*qD[n] =E= sum(nn$(map_T_inp[nn,n]), qD[nn]*PwT[nn]);
	E_q_out_T_inp[n]$(bra_o_T_inp[n])..	qD[n] =E= sum(nn$(map_T_inp[n,nn]), mu[n,nn] * (PbT[nn]/PwT[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_T_inp[n]$(bra_no_T_inp[n])..	qD[n] =E= sum(nn$(map_T_inp[n,nn]), mu[n,nn] * (PwT[nn]/PwT[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_T_out 
	E_zp_T_out[n]$(kno_T_out[n])..	PwT[n]*qD[n] =E= sum(nn$(map_T_out[nn,n] and out[nn]), qS[nn]*PbT[nn])+sum(nn$(map_T_out[nn,n] and not out[nn]), qD[nn]*PwT[nn]);
	E_q_out_T_out[n]$(bra_o_T_out[n])..	qS[n] =E= sum(nn$(map_T_out[n,nn]), mu[n,nn] * (PbT[n]/PwT[nn])**(-eta[nn]) * qD[nn]/(sum(nnn$(map_T_out[nnn,nn] and out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwT[nn])**(-eta[nn]))+sum(nnn$(map_T_out[nnn,nn] and not out[nnn]), mu[nnn,nn]*(PwT[nnn]/PwT[nn])**(-eta[nn]))));
	E_q_nout_T_out[n]$(bra_no_T_out[n])..	qD[n] =E= sum(nn$(map_T_out[n,nn]), mu[n,nn] * (PwT[n]/PwT[nn])**(-eta[nn]) * qD[nn]/(sum(nnn$(map_T_out[nnn,nn] and out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwT[nn])**(-eta[nn]))+sum(nnn$(map_T_out[nnn,nn] and not out[nnn]), mu[nnn,nn]*(PwT[nnn]/PwT[nn])**(-eta[nn]))));
$ENDBLOCK
$BLOCK M_C 
	E_zp_out_C[n]$(out_C[n])..	PbT[n]*qS[n] =E= sum(nn$(map_C[nn,n]), qD[nn]*PwT[nn]);
	E_zp_nout_C[n]$(kno_no_C[n])..	PwT[n]*qD[n] =E= sum(nn$(map_C[nn,n]), qD[nn]*PwT[nn]);
	E_q_out_C[n]$(bra_o_C[n])..	qD[n] =E= sum(nn$(map_C[n,nn]), mu[n,nn] * exp((PbT[nn]-PwT[n])*sigma[nn]) * qS[nn]/ sum(nnn$(map_C[nnn,nn]), mu[nnn,nn]*exp((PbT[nn]-PwT[nnn])*sigma[nn])));
	E_q_nout_C[n]$(bra_no_C[n])..	qD[n] =E= sum(nn$(map_C[n,nn]), mu[n,nn] * exp((PwT[nn]-PwT[n])*sigma[nn]) * qD[nn]/ sum(nnn$(map_C[nnn,nn]), mu[nnn,nn]*exp((PwT[nn]-PwT[nnn])*sigma[nn])));
$ENDBLOCK
$BLOCK M_E 
	E_zp_out_E[n]$(out_E[n])..	PbT[n]*qS[n] =E= sum(nn$(map_E[nn,n]), qD[nn]*PwT[nn]);
	E_zp_nout_E[n]$(kno_no_E[n])..	PwT[n]*qD[n] =E= sum(nn$(map_E[nn,n]), qD[nn]*PwT[nn]);
	E_q_out_E[n]$(bra_o_E[n])..	qD[n] =E= sum(nn$(map_E[n,nn]), mu[n,nn] * (PbT[nn]/PwT[n])**(sigma[nn]) * qS[nn] / sum(nnn$(map_E[nnn,nn]), mu[nnn,nn] * (PbT[nn]/PwT[nnn])**(sigma[nn])));
	E_q_nout_E[n]$(bra_no_E[n])..	qD[n] =E= sum(nn$(map_E[n,nn]), mu[n,nn] * (PwT[nn]/PwT[n])**(sigma[nn]) * qD[nn] / sum(nnn$(map_E[nnn,nn]), mu[nnn,nn] * (PwT[nn]/PwT[nnn])**(sigma[nn])));
$ENDBLOCK
$BLOCK M_A1_pw 
	E_pw_A1[n]$(out[n])..	Peq[n] =E= (1+markup[n])*(PbT[n]*(1+tauLump/sum(nn$(out[nn]), qS[nn]*PbT[nn]))+tauS[n]+0);
$ENDBLOCK
