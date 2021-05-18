$BLOCK M_ID_EC 
	E_zp_out_ID_EC[n]$(out_ID_EC[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_EC[nn,n]), qD[nn]*PwT[nn]);
	E_zp_nout_ID_EC[n]$(kno_no_ID_EC[n])..	PwT[n]*qD[n] =E= sum(nn$(map_ID_EC[nn,n]), qD[nn]*PwT[nn]);
	E_q_out_ID_EC[n]$(bra_o_ID_EC[n])..	qD[n] =E= sum(nn$(map_ID_EC[n,nn]), mu[n,nn] * (PbT[nn]/PwT[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_ID_EC[n]$(bra_no_ID_EC[n])..	qD[n] =E= sum(nn$(map_ID_EC[n,nn]), mu[n,nn] * (PwT[nn]/PwT[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_ID_CU 
	E_zp_out_ID_CU[n]$(out_ID_CU[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_CU[nn,n]), qD[nn]*PwT[nn]);
	E_zp_nout_ID_CU[n]$(kno_no_ID_CU[n])..	PwT[n]*qD[n] =E= sum(nn$(map_ID_CU[nn,n]), qD[nn]*PwT[nn]);
	E_q_out_ID_CU[n]$(bra_o_ID_CU[n])..	qD[n] =E= sum(nn$(map_ID_CU[n,nn]), mu[n,nn] * exp((PbT[nn]-PwT[n])*sigma[nn]) * qS[nn]/ sum(nnn$(map_ID_CU[nnn,nn]), mu[nnn,nn]*exp((PbT[nn]-PwT[nnn])*sigma[nn])));
	E_q_nout_ID_CU[n]$(bra_no_ID_CU[n])..	qD[n] =E= sum(nn$(map_ID_CU[n,nn]), mu[n,nn] * exp((PwT[nn]-PwT[n])*sigma[nn]) * qD[nn]/ sum(nnn$(map_ID_CU[nnn,nn]), mu[nnn,nn]*exp((PwT[nn]-PwT[nnn])*sigma[nn])));
$ENDBLOCK
$BLOCK M_ID_TU 
	E_zp_ID_TU[n]$(kno_ID_TU[n])..	PwT[n]*qD[n] =E= sum(nn$(map_ID_TU[nn,n] and out[nn]), qS[nn]*PbT[nn])+sum(nn$(map_ID_TU[nn,n] and not out[nn]), qD[nn]*PwT[nn]);
	E_q_out_ID_TU[n]$(bra_o_ID_TU[n])..	qS[n] =E= sum(nn$(map_ID_TU[n,nn]), mu[n,nn] * (PbT[n]/PwT[nn])**(-eta[nn]) * qD[nn]);
	E_q_nout_ID_TU[n]$(bra_no_ID_TU[n])..	qD[n] =E= sum(nn$(map_ID_TU[n,nn]), mu[n,nn] * (PwT[n]/PwT[nn])**(-eta[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_ID_TX 
	E_zp_out_ID_TX[n]$(out_ID_TX[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_TX[nn,n]), qD[nn]*PwT[nn]);
	E_zp_nout_ID_TX[n]$(kno_no_ID_TX[n])..	PwT[n]*qD[n] =E= sum(nn$(map_ID_TX[nn,n]), qD[nn]*PwT[nn]);
	E_q_out_ID_TX[n]$(bra_o_ID_TX[n])..	qD[n] =E= sum(nn$(map_ID_TX[n,nn]), mu[n,nn] * (PbT[nn]/PwT[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_ID_TX[n]$(bra_no_ID_TX[n])..	qD[n] =E= sum(nn$(map_ID_TX[n,nn]), mu[n,nn] * (PwT[nn]/PwT[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_ID_CbaseX 
	E_zp_out_ID_CbaseX[n]$(out_ID_CbaseX[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_CbaseX[nn,n]), qD[nn]*PwT[nn]);
	E_zp_nout_ID_CbaseX[n]$(kno_no_ID_CbaseX[n])..	PwT[n]*qD[n] =E= sum(nn$(map_ID_CbaseX[nn,n]), qD[nn]*PwT[nn]);
	E_q_out_ID_CbaseX[n]$(bra_o_ID_CbaseX[n])..	qD[n] =E= sum(nn$(map_ID_CbaseX[n,nn]), mu[n,nn] * (PbT[nn]/PwT[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_ID_CbaseX[n]$(bra_no_ID_CbaseX[n])..	qD[n] =E= sum(nn$(map_ID_CbaseX[n,nn]), mu[n,nn] * (PwT[nn]/PwT[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_ID_UbaseX 
	E_zp_out_ID_UbaseX[n]$(out_ID_UbaseX[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_UbaseX[nn,n]), qD[nn]*PwT[nn]);
	E_zp_nout_ID_UbaseX[n]$(kno_no_ID_UbaseX[n])..	PwT[n]*qD[n] =E= sum(nn$(map_ID_UbaseX[nn,n]), qD[nn]*PwT[nn]);
	E_q_out_ID_UbaseX[n]$(bra_o_ID_UbaseX[n])..	qD[n] =E= sum(nn$(map_ID_UbaseX[n,nn]), mu[n,nn] * (PbT[nn]/PwT[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_ID_UbaseX[n]$(bra_no_ID_UbaseX[n])..	qD[n] =E= sum(nn$(map_ID_UbaseX[n,nn]), mu[n,nn] * (PwT[nn]/PwT[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_EOP_CU 
	E_zp_out_EOP_CU[n]$(out_EOP_CU[n])..	PbT[n]*qS[n] =E= sum(nn$(map_EOP_CU[nn,n]), qD[nn]*PwT[nn]);
	E_zp_nout_EOP_CU[n]$(kno_no_EOP_CU[n])..	PwT[n]*qD[n] =E= sum(nn$(map_EOP_CU[nn,n]), qD[nn]*PwT[nn]);
	E_q_out_EOP_CU[n]$(bra_o_EOP_CU[n])..	qD[n] =E= sum(nn$(map_EOP_CU[n,nn]), mu[n,nn] * (PbT[nn]/PwT[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_EOP_CU[n]$(bra_no_EOP_CU[n])..	qD[n] =E= sum(nn$(map_EOP_CU[n,nn]), mu[n,nn] * (PwT[nn]/PwT[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_EOP_TU 
	E_zp_EOP_TU[n]$(kno_EOP_TU[n])..	PwT[n]*qD[n] =E= sum(nn$(map_EOP_TU[nn,n] and out[nn]), qS[nn]*PbT[nn])+sum(nn$(map_EOP_TU[nn,n] and not out[nn]), qD[nn]*PwT[nn]);
	E_q_out_EOP_TU[n]$(bra_o_EOP_TU[n])..	qS[n] =E= sum(nn$(map_EOP_TU[n,nn]), mu[n,nn] * (PbT[n]/PwT[nn])**(-eta[nn]) * qD[nn]);
	E_q_nout_EOP_TU[n]$(bra_no_EOP_TU[n])..	qD[n] =E= sum(nn$(map_EOP_TU[n,nn]), mu[n,nn] * (PwT[n]/PwT[nn])**(-eta[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_EOP_TX 
	E_zp_out_EOP_TX[n]$(out_EOP_TX[n])..	PbT[n]*qS[n] =E= sum(nn$(map_EOP_TX[nn,n]), qD[nn]*PwT[nn]);
	E_zp_nout_EOP_TX[n]$(kno_no_EOP_TX[n])..	PwT[n]*qD[n] =E= sum(nn$(map_EOP_TX[nn,n]), qD[nn]*PwT[nn]);
	E_q_out_EOP_TX[n]$(bra_o_EOP_TX[n])..	qD[n] =E= sum(nn$(map_EOP_TX[n,nn]), mu[n,nn] * (PbT[nn]/PwT[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_EOP_TX[n]$(bra_no_EOP_TX[n])..	qD[n] =E= sum(nn$(map_EOP_TX[n,nn]), mu[n,nn] * (PwT[nn]/PwT[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_Abatement_pw 
	E_pw_Abatement[n]$(out[n])..	Peq[n] =E= (1+markup[n])*(PbT[n]*(1+tauLump/sum(nn$(out[nn]), qS[nn]*PbT[nn]))+tauS[n]+0);
$ENDBLOCK
