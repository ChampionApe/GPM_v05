$BLOCK M_ID_EC 
	E_zp_out_ID_EC[n]$(out_ID_EC[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_EC[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_ID_EC[n]$(kno_no_ID_EC[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_EC[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_ID_EC[n]$(bra_o_ID_EC[n])..	qD[n] =E= sum(nn$(map_ID_EC[n,nn]), mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]) * qS[nn] / sum(nnn$(map_ID_EC[nnn,nn]), mu[nnn,nn] * (PbT[nn]/PwThat[nnn])**(sigma[nn])));
	E_q_nout_ID_EC[n]$(bra_no_ID_EC[n])..	qD[n] =E= sum(nn$(map_ID_EC[n,nn]), mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]) * qD[nn] / sum(nnn$(map_ID_EC[nnn,nn]), mu[nnn,nn] * (PwThat[nn]/PwThat[nnn])**(sigma[nn])));
$ENDBLOCK
$BLOCK M_ID_CU 
	E_zp_out_ID_CU[n]$(out_ID_CU[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_CU[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_ID_CU[n]$(kno_no_ID_CU[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_CU[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_ID_CU[n]$(bra_o_ID_CU[n])..	qD[n] =E= sum(nn$(map_ID_CU[n,nn]), mu[n,nn] * exp((PbT[nn]-PwThat[n])*sigma[nn]) * qS[nn]/ sum(nnn$(map_ID_CU[nnn,nn]), mu[nnn,nn]*exp((PbT[nn]-PwThat[nnn])*sigma[nn])));
	E_q_nout_ID_CU[n]$(bra_no_ID_CU[n])..	qD[n] =E= sum(nn$(map_ID_CU[n,nn]), mu[n,nn] * exp((PwThat[nn]-PwThat[n])*sigma[nn]) * qD[nn]/ sum(nnn$(map_ID_CU[nnn,nn]), mu[nnn,nn]*exp((PwThat[nn]-PwThat[nnn])*sigma[nn])));
$ENDBLOCK
$BLOCK M_ID_TU 
	E_zp_ID_TU[n]$(kno_ID_TU[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_TU[nn,n] and out[nn]), qS[nn]*PbT[nn])+sum(nn$(map_ID_TU[nn,n] and not out[nn]), qD[nn]*PwThat[nn]);
	E_q_out_ID_TU[n]$(bra_o_ID_TU[n])..	qS[n] =E= sum(nn$(map_ID_TU[n,nn]), mu[n,nn] * (PbT[n]/PwThat[nn])**(-eta[nn]) * qD[nn]/(sum(nnn$(map_ID_TU[nnn,nn] and out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwThat[nn])**(-eta[nn]))+sum(nnn$(map_ID_TU[nnn,nn] and not out[nnn]), mu[nnn,nn]*(PwThat[nnn]/PwThat[nn])**(-eta[nn]))));
	E_q_nout_ID_TU[n]$(bra_no_ID_TU[n])..	qD[n] =E= sum(nn$(map_ID_TU[n,nn]), mu[n,nn] * (PwThat[n]/PwThat[nn])**(-eta[nn]) * qD[nn]/(sum(nnn$(map_ID_TU[nnn,nn] and out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwThat[nn])**(-eta[nn]))+sum(nnn$(map_ID_TU[nnn,nn] and not out[nnn]), mu[nnn,nn]*(PwThat[nnn]/PwThat[nn])**(-eta[nn]))));
$ENDBLOCK
$BLOCK M_ID_TX 
	E_zp_out_ID_TX[n]$(out_ID_TX[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_TX[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_ID_TX[n]$(kno_no_ID_TX[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_TX[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_ID_TX[n]$(bra_o_ID_TX[n])..	qD[n] =E= sum(nn$(map_ID_TX[n,nn]), mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_ID_TX[n]$(bra_no_ID_TX[n])..	qD[n] =E= sum(nn$(map_ID_TX[n,nn]), mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_ID_IOCU 
	E_zp_ID_IOCU[n]$(kno_ID_IOCU[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_IOCU[nn,n] and out[nn]), qS[nn]*PbT[nn])+sum(nn$(map_ID_IOCU[nn,n] and not out[nn]), qD[nn]*PwThat[nn]);
	E_q_out_ID_IOCU[n]$(bra_o_ID_IOCU[n])..	qS[n] =E= sum(nn$(map_ID_IOCU[n,nn]), mu[n,nn] * (PbT[n]/PwThat[nn])**(-eta[nn]) * qD[nn]/(sum(nnn$(map_ID_IOCU[nnn,nn] and out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwThat[nn])**(-eta[nn]))+sum(nnn$(map_ID_IOCU[nnn,nn] and not out[nnn]), mu[nnn,nn]*(PwThat[nnn]/PwThat[nn])**(-eta[nn]))));
	E_q_nout_ID_IOCU[n]$(bra_no_ID_IOCU[n])..	qD[n] =E= sum(nn$(map_ID_IOCU[n,nn]), mu[n,nn] * (PwThat[n]/PwThat[nn])**(-eta[nn]) * qD[nn]/(sum(nnn$(map_ID_IOCU[nnn,nn] and out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwThat[nn])**(-eta[nn]))+sum(nnn$(map_ID_IOCU[nnn,nn] and not out[nnn]), mu[nnn,nn]*(PwThat[nnn]/PwThat[nn])**(-eta[nn]))));
$ENDBLOCK
$BLOCK M_ID_IOX 
	E_zp_out_ID_IOX[n]$(out_ID_IOX[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_IOX[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_ID_IOX[n]$(kno_no_ID_IOX[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_IOX[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_ID_IOX[n]$(bra_o_ID_IOX[n])..	qD[n] =E= sum(nn$(map_ID_IOX[n,nn]), mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_ID_IOX[n]$(bra_no_ID_IOX[n])..	qD[n] =E= sum(nn$(map_ID_IOX[n,nn]), mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_ID_UbaseX 
	E_zp_out_ID_UbaseX[n]$(out_ID_UbaseX[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_UbaseX[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_ID_UbaseX[n]$(kno_no_ID_UbaseX[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_UbaseX[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_ID_UbaseX[n]$(bra_o_ID_UbaseX[n])..	qD[n] =E= sum(nn$(map_ID_UbaseX[n,nn]), mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_ID_UbaseX[n]$(bra_no_ID_UbaseX[n])..	qD[n] =E= sum(nn$(map_ID_UbaseX[n,nn]), mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_EOP_CU 
	E_zp_out_EOP_CU[n]$(out_EOP_CU[n])..	PbT[n]*qS[n] =E= sum(nn$(map_EOP_CU[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_EOP_CU[n]$(kno_no_EOP_CU[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_EOP_CU[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_EOP_CU[n]$(bra_o_EOP_CU[n])..	qD[n] =E= sum(nn$(map_EOP_CU[n,nn]), mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_EOP_CU[n]$(bra_no_EOP_CU[n])..	qD[n] =E= sum(nn$(map_EOP_CU[n,nn]), mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_EOP_TU 
	E_zp_EOP_TU[n]$(kno_EOP_TU[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_EOP_TU[nn,n] and out[nn]), qS[nn]*PbT[nn])+sum(nn$(map_EOP_TU[nn,n] and not out[nn]), qD[nn]*PwThat[nn]);
	E_q_out_EOP_TU[n]$(bra_o_EOP_TU[n])..	qS[n] =E= sum(nn$(map_EOP_TU[n,nn]), mu[n,nn] * (PbT[n]/PwThat[nn])**(-eta[nn]) * qD[nn]/(sum(nnn$(map_EOP_TU[nnn,nn] and out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwThat[nn])**(-eta[nn]))+sum(nnn$(map_EOP_TU[nnn,nn] and not out[nnn]), mu[nnn,nn]*(PwThat[nnn]/PwThat[nn])**(-eta[nn]))));
	E_q_nout_EOP_TU[n]$(bra_no_EOP_TU[n])..	qD[n] =E= sum(nn$(map_EOP_TU[n,nn]), mu[n,nn] * (PwThat[n]/PwThat[nn])**(-eta[nn]) * qD[nn]/(sum(nnn$(map_EOP_TU[nnn,nn] and out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwThat[nn])**(-eta[nn]))+sum(nnn$(map_EOP_TU[nnn,nn] and not out[nnn]), mu[nnn,nn]*(PwThat[nnn]/PwThat[nn])**(-eta[nn]))));
$ENDBLOCK
$BLOCK M_EOP_TX 
	E_zp_out_EOP_TX[n]$(out_EOP_TX[n])..	PbT[n]*qS[n] =E= sum(nn$(map_EOP_TX[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_EOP_TX[n]$(kno_no_EOP_TX[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_EOP_TX[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_EOP_TX[n]$(bra_o_EOP_TX[n])..	qD[n] =E= sum(nn$(map_EOP_TX[n,nn]), mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_EOP_TX[n]$(bra_no_EOP_TX[n])..	qD[n] =E= sum(nn$(map_EOP_TX[n,nn]), mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_Abatement_simplesum 
	E_sumU[n]$(sumUaggs[n])..	qsumU[n] =E= sum(nn$(sumU2U[n,nn]), qD[nn]);
	E_sumX[n]$(sumXaggs[n])..	qsumX[n] =E= sum(nn$(sumX2X[n,nn]), qD[nn]);
$ENDBLOCK
$BLOCK M_Abatement_EOP 
	E_preabatementM_EOP[n]$(M_subset[n])..	M0[n] =E= sum(nn$sumXaggs[nn], phi[n,nn]*qsumX[nn]);
	E_postabatementM_EOP[n]$(M_subset[n])..	M[n] =E= M0[n] - sum(nn$map_M2C[n,nn], qS[nn]);
	E_endogenous_abatementC_EOP[n]$(EOP_C_subset[n])..	qS[n] =E= sum(nn$map_M2C[nn,n], M0[nn] * theta[n] * errorf((pM[nn] - PbT[n] + muG[n])/(sigmaG[n])));
	E_adjusted_inputprice_EOP[n]$(inp[n])..	PwThat[n] =E= PwT[n] + sum(nn$map_M2X[nn,n], phi[nn,n] * pMhat[nn]);
	E_adjusted_emission_price_EOP[n]$(M_subset[n])..	pMhat[n] =E= pM[n]*(1 - sum(nn$map_M2C[n,nn], theta[nn] * errorf( (pM[n] - PbT[nn] + muG[nn]) / (sigmaG[nn])))) + 
 sum(nn$map_M2C[n,nn], errorf( (pM[n] - PbT[nn] + muG[nn]) / (sigmaG[nn])) * (PbT[nn] + muG[nn] - Sqr(sigmaG[nn]) * (@std_pdf((pM[n] - PbT[nn] - muG[nn])/sigmaG[nn]) / errorf((pM[n] - PbT[nn] - muG[nn])/sigmaG[nn]))));
$ENDBLOCK
