$BLOCK M_ID_EC 
	E_zp_out_ID_EC[n]$(ID_out_ID_EC[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_EC[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_ID_EC[n]$(kno_no_ID_EC[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_EC[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_ID_EC[n]$(bra_o_ID_EC[n])..	qD[n] =E= sum(nn$(map_ID_EC[n,nn]), mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]) * qS[nn] / sum(nnn$(map_ID_EC[nnn,nn]), mu[nnn,nn] * (PbT[nn]/PwThat[nnn])**(sigma[nn])));
	E_q_nout_ID_EC[n]$(bra_no_ID_EC[n])..	qD[n] =E= sum(nn$(map_ID_EC[n,nn]), mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]) * qD[nn] / sum(nnn$(map_ID_EC[nnn,nn]), mu[nnn,nn] * (PwThat[nn]/PwThat[nnn])**(sigma[nn])));
$ENDBLOCK
$BLOCK M_ID_CU 
	E_zp_out_ID_CU[n]$(ID_out_ID_CU[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_CU[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_ID_CU[n]$(kno_no_ID_CU[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_CU[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_ID_CU[n]$(bra_o_ID_CU[n])..	qD[n] =E= sum(nn$(map_ID_CU[n,nn]), mu[n,nn] * exp((PbT[nn]-PwThat[n])*sigma[nn]) * qS[nn]/ sum(nnn$(map_ID_CU[nnn,nn]), mu[nnn,nn]*exp((PbT[nn]-PwThat[nnn])*sigma[nn])));
	E_q_nout_ID_CU[n]$(bra_no_ID_CU[n])..	qD[n] =E= sum(nn$(map_ID_CU[n,nn]), mu[n,nn] * exp((PwThat[nn]-PwThat[n])*sigma[nn]) * qD[nn]/ sum(nnn$(map_ID_CU[nnn,nn]), mu[nnn,nn]*exp((PwThat[nn]-PwThat[nnn])*sigma[nn])));
$ENDBLOCK
$BLOCK M_ID_TU 
	E_zp_ID_TU[n]$(kno_ID_TU[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_TU[nn,n] and ID_out[nn]), qS[nn]*PbT[nn])+sum(nn$(map_ID_TU[nn,n] and not ID_out[nn]), qD[nn]*PwThat[nn]);
	E_q_out_ID_TU[n]$(bra_o_ID_TU[n])..	qS[n] =E= sum(nn$(map_ID_TU[n,nn]), mu[n,nn] * (PbT[n]/PwThat[nn])**(-eta[nn]) * qD[nn]/(sum(nnn$(map_ID_TU[nnn,nn] and ID_out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwThat[nn])**(-eta[nn]))+sum(nnn$(map_ID_TU[nnn,nn] and not ID_out[nnn]), mu[nnn,nn]*(PwThat[nnn]/PwThat[nn])**(-eta[nn]))));
	E_q_nout_ID_TU[n]$(bra_no_ID_TU[n])..	qD[n] =E= sum(nn$(map_ID_TU[n,nn]), mu[n,nn] * (PwThat[n]/PwThat[nn])**(-eta[nn]) * qD[nn]/(sum(nnn$(map_ID_TU[nnn,nn] and ID_out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwThat[nn])**(-eta[nn]))+sum(nnn$(map_ID_TU[nnn,nn] and not ID_out[nnn]), mu[nnn,nn]*(PwThat[nnn]/PwThat[nn])**(-eta[nn]))));
$ENDBLOCK
$BLOCK M_ID_TX 
	E_zp_out_ID_TX[n]$(ID_out_ID_TX[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_TX[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_ID_TX[n]$(kno_no_ID_TX[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_TX[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_ID_TX[n]$(bra_o_ID_TX[n])..	qD[n] =E= sum(nn$(map_ID_TX[n,nn]), mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_ID_TX[n]$(bra_no_ID_TX[n])..	qD[n] =E= sum(nn$(map_ID_TX[n,nn]), mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_ID_BU 
	E_zp_ID_BU[n]$(bra_no_ID_BU[n])..	PwThat[n] =E= sum(nn$(map_ID_BU[n,nn]), mu[n,nn]*PwThat[nn]) ;
	E_q_nout_ID_BU[n]$(kno_ID_BU[n])..	qD[n] =E= sum(nn$(map_ID_BU[nn,n]), qD[nn]/mu[nn,n]) ;
$ENDBLOCK
$BLOCK M_ID_BX 
	E_zp_out_ID_BX[n]$(ID_out_ID_BX[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_BX[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_ID_BX[n]$(kno_no_ID_BX[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_BX[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_ID_BX[n]$(bra_o_ID_BX[n])..	qD[n] =E= sum(nn$(map_ID_BX[n,nn]), mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_ID_BX[n]$(bra_no_ID_BX[n])..	qD[n] =E= sum(nn$(map_ID_BX[n,nn]), mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_ID_Y 
	E_zp_out_ID_Y[n]$(ID_out_ID_Y[n])..	PbT[n]*qS[n] =E= sum(nn$(map_ID_Y[nn,n]), qD[nn]*PwThat[nn]);
	E_zp_nout_ID_Y[n]$(kno_no_ID_Y[n])..	PwThat[n]*qD[n] =E= sum(nn$(map_ID_Y[nn,n]), qD[nn]*PwThat[nn]);
	E_q_out_ID_Y[n]$(bra_o_ID_Y[n])..	qD[n] =E= sum(nn$(map_ID_Y[n,nn]), mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]) * qS[nn]);
	E_q_nout_ID_Y[n]$(bra_no_ID_Y[n])..	qD[n] =E= sum(nn$(map_ID_Y[n,nn]), mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]) * qD[nn]);
$ENDBLOCK
$BLOCK M_atest_ID_sum 
	E_ID_os_atest[n,nn]$(ID_e2t[n,nn])..	os[n,nn] =E= sum(nnn$(ID_e2u[n,nnn] and ID_u2t[nnn,nn]), qD[nnn])/qD[nn];
	E_ID_qsumX_atest[n,nn]$(ID_e2ai[n,nn])..	qsumX[n,nn] =E=  sum([nnn,nnnn]$(ID_e2ai2i[n,nn,nnn] and ID_e2t[n,nnnn] and ID_i2t[nnn,nnnn]), qD[nnn]*os[n,nnnn]);
$ENDBLOCK
$BLOCK M_atest_ID_Em 
	E_M0_atest[z]..	M0[z] =E= sum(n$(ai[n]), phi[z,n]*qD[n]);
	E_ID_PwThat_atest[n]$(ID_inp[n])..	PwThat[n] =E= PwT[n]+sum(z, sum(nn$(ID_i2ai[n,nn]), phi[z,nn]*pMhat[z]));
$ENDBLOCK
$BLOCK M_atest_ID_agg 
	E_aggqD_ID_atest[n]$(ai[n])..	qD[n] =E= sum(nn$(ID_i2ai[nn,n]), qD[nn]);
	E_pMhat_ID_atest[z]..	pMhat[z] =E= pM[z];
$ENDBLOCK
$BLOCK M_atest_ID_calib_aux 
	E_currapp_ID_atest[n,nn]$(ID_e2t[n,nn] and kno_ID_TU[nn])..	currapp[n,nn] =E= sum(nnn$(ID_u2t[nnn,nn] and ID_e2u[n,nnn]), qD[nnn])/qD[n];
	E_share_uc_atest[n,nn]$(map_ID_CU[n,nn] and bra_ID_TU[n])..	s_uc[n,nn] =E= mu[n,nn]*exp((PwThat[nn]-PwThat[n])*sigma[nn])/(
	sum(nnn$(map_ID_CU[nnn,nn] and bra_ID_TU[nnn]), mu[nnn,nn]*exp((PwThat[nn]-PwThat[nnn])*sigma[nn]))+
	sum(nnn$(map_ID_CU[nnn,nn] and bra_ID_BU[nnn]), mu[nnn,nn]*exp(sigma[nn]*(PwThat[nn]-sum(nnnn$(ID_e2u[nnnn,n]), sum(nnnnn$(ID_u2t[n,nnnnn]), gamma_tau[nnnn,nnnnn])*sum(nnnnn$(ID_u2t[nnn,nnnnn]), PwThat[nnnnn])))))
	);
	E_currapp_mod_atest[n,nn]$(ID_e2t[n,nn] and kno_ID_TU[nn])..	currapp_mod[n,nn] =E= sum([nnn,nnnn]$(ID_u2t[nnn,nn] and map_ID_EC[nnnn,n] and map_ID_CU[nnn,nnnn]), s_uc[nnn,nnnn] * qD[nnnn]/qD[n]);
$ENDBLOCK
$BLOCK M_atest_ID_minobj 
	E_minobj_ID_atest..	minobj =E= sum(map_gamma[n,nn,nnn,nnnn], Sqr(mu[nnn,nnnn]-gamma_tau[n,nn]))+weight_mu*sum([n,nn]$(map_ID_CU[n,nn] and bra_ID_TU[n]), Sqr(mu[n,nn]-mubar[n,nn]));
$ENDBLOCK
