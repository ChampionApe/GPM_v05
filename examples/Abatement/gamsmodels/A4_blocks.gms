$BLOCK M_ID_EC 
	E_sout_ID_EC[n,nn]$(map_ID_EC[n,nn] and bra_o_ID_EC[n])..	share[n,nn] =E= mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn])/sum(nnn$(map_ID_EC[nnn,nn]), mu[nnn,nn] * (PbT[nn]/PwThat[nnn])**(sigma[nn]));
	E_snout_ID_EC[n,nn]$(map_ID_EC[n,nn] and bra_no_ID_EC[n])..	share[n,nn] =E= mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn])/sum(nnn$(map_ID_EC[nnn,nn]), mu[nnn,nn] * (PwThat[nn]/PwThat[nnn])**(sigma[nn]));
	E_pout_ID_EC[n]$(ID_out_ID_EC[n])..	PbT[n] =E= sum(nn$(map_ID_EC[nn,n]), share[nn,n]*PwThat[nn]);
	E_pnout_ID_EC[n]$(kno_no_ID_EC[n])..	PwThat[n] =E= sum(nn$(map_ID_EC[nn,n]), share[nn,n]*PwThat[nn]);
	E_qout_ID_EC[n]$(bra_o_ID_EC[n])..	qD[n] =E= sum(nn$(map_ID_EC[n,nn]), share[n,nn]*qS[nn])+epsi;
	E_qnout_ID_EC[n]$(bra_no_ID_EC[n])..	qD[n] =E= sum(nn$(map_ID_EC[n,nn]), share[n,nn]*(qD[nn]-epsi))+epsi;
$ENDBLOCK
$BLOCK M_ID_CU 
	E_sout_ID_CU[n,nn]$(map_ID_CU[n,nn] and bra_o_ID_CU[n])..	share[n,nn] =E= mu[n,nn] * exp((PbT[nn]-PwThat[n])*sigma[nn])/sum(nnn$(map_ID_CU[nnn,nn]), mu[nnn,nn] * exp((PbT[nn]-PwThat[nnn])*sigma[nn]));
	E_snout_ID_CU[n,nn]$(map_ID_CU[n,nn] and bra_no_ID_CU[n])..	share[n,nn] =E= mu[n,nn] * exp((PwThat[nn]-PwThat[n])*sigma[nn])/sum(nnn$(map_ID_CU[nnn,nn]), mu[nnn,nn] * exp((PwThat[nn]-PwThat[nnn])*sigma[nn]));
	E_pout_ID_CU[n]$(ID_out_ID_CU[n])..	PbT[n] =E= sum(nn$(map_ID_CU[nn,n]), share[nn,n]*PwThat[nn]);
	E_pnout_ID_CU[n]$(kno_no_ID_CU[n])..	PwThat[n] =E= sum(nn$(map_ID_CU[nn,n]), share[nn,n]*PwThat[nn]);
	E_qout_ID_CU[n]$(bra_o_ID_CU[n])..	qD[n] =E= sum(nn$(map_ID_CU[n,nn]), share[n,nn]*qS[nn])+epsi;
	E_qnout_ID_CU[n]$(bra_no_ID_CU[n])..	qD[n] =E= sum(nn$(map_ID_CU[n,nn]), share[n,nn]*(qD[nn]-epsi))+epsi;
$ENDBLOCK
$BLOCK M_ID_TU 
	E_p_ID_TU[n]$(kno_ID_TU[n])..	PwThat[n] =E= sum(nn$(map_ID_TU[nn,n] and ID_out[nn]), share[nn,n]*PbT[nn])+sum(nn$(map_ID_TU[nn,n] and not ID_out[nn]), share[nn,n]*PwThat[nn]);
	E_sout_ID_TU[n,nn]$(map_ID_TU[n,nn] and bra_o_ID_TU[n])..	share[n,nn] =E= mu[n,nn]*(PbT[n]/PwThat[nn])**(-eta[nn])/(sum(nnn$(map_ID_TU[nnn,nn] and ID_out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwThat[nn])**(-eta[nn]))+sum(nnn$(map_ID_TU[nnn,nn] and not ID_out[nnn]), mu[nnn,nn]*(PwThat[nnn]/PwThat[nn])**(-eta[nn])));
	E_snout_ID_TU[n,nn]$(map_ID_TU[n,nn] and bra_no_ID_TU[n])..	share[n,nn] =E= mu[n,nn]*(PwThat[n]/PwThat[nn])**(-eta[nn])/(sum(nnn$(map_ID_TU[nnn,nn] and ID_out[nnn]), mu[nnn,nn]*(PbT[nnn]/PwThat[nn])**(-eta[nn]))+sum(nnn$(map_ID_TU[nnn,nn] and not ID_out[nnn]), mu[nnn,nn]*(PwThat[nnn]/PwThat[nn])**(-eta[nn])));
	E_qout_ID_TU[n]$(bra_o_ID_TU[n])..	qS[n] =E= sum(nn$(map_ID_TU[n,nn]), share[n,nn]*qD[nn]);
	E_qnout_ID_TU[n]$(bra_no_ID_TU[n])..	qD[n] =E= sum(nn$(map_ID_TU[n,nn]), share[n,nn]*qD[nn]);
$ENDBLOCK
$BLOCK M_ID_TX 
	E_sout_ID_TX[n,nn]$(map_ID_TX[n,nn] and bra_o_ID_TX[n])..	share[n,nn] =E= mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]);
	E_snout_ID_TX[n,nn]$(map_ID_TX[n,nn] and bra_no_ID_TX[n])..	share[n,nn] =E= mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]);
	E_pout_ID_TX[n]$(ID_out_ID_TX[n])..	PbT[n] =E= sum(nn$(map_ID_TX[nn,n]),share[nn,n]*PwThat[nn]);
	E_pnout_ID_TX[n]$(kno_no_ID_TX[n])..	PwThat[n] =E= sum(nn$(map_ID_TX[nn,n]),share[nn,n]*PwThat[nn]);
	E_qout_ID_TX[n]$(bra_o_ID_TX[n])..	qD[n] =E= sum(nn$(map_ID_TX[n,nn]), share[n,nn]*qS[nn])+epsi;
	E_qnout_ID_TX[n]$(bra_no_ID_TX[n])..	qD[n] =E= sum(nn$(map_ID_TX[n,nn]), share[n,nn]*(qD[nn]-epsi))+epsi;
$ENDBLOCK
$BLOCK M_ID_BU 
	E_pout_ID_BU[n]$(bra_o_ID_BU[n])..	PbT[n] =E= sum(nn$(map_ID_BU[n,nn]),mu[n,nn]*PwThat[nn]);
	E_pnout_ID_BU[n]$(bra_no_ID_BU[n])..	PwThat[n] =E= sum(nn$(map_ID_BU[n,nn]),mu[n,nn]*PwThat[nn]);
	E_sout_ID_BU[n,nn]$(map_ID_BU[n,nn] and bra_o_ID_BU[n])..	share[n,nn] =E= qS[n]/qD[nn];
	E_snout_ID_BU[n,nn]$(map_ID_BU[n,nn] and bra_no_ID_BU[n])..	share[n,nn] =E= qD[n]/qD[nn];
	E_q_ID_BU[n]$(kno_ID_BU[n])..	qD[n] =E= sum(nn$(map_ID_BU[nn,n] and ID_out[nn]), qS[nn]/mu[nn,n])+sum(nn$(map_ID_BU[nn,n] and not ID_out[nn]), qD[nn]/mu[nn,n]);
$ENDBLOCK
$BLOCK M_ID_BX 
	E_sout_ID_BX[n,nn]$(map_ID_BX[n,nn] and bra_o_ID_BX[n])..	share[n,nn] =E= mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]);
	E_snout_ID_BX[n,nn]$(map_ID_BX[n,nn] and bra_no_ID_BX[n])..	share[n,nn] =E= mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]);
	E_pout_ID_BX[n]$(ID_out_ID_BX[n])..	PbT[n] =E= sum(nn$(map_ID_BX[nn,n]),share[nn,n]*PwThat[nn]);
	E_pnout_ID_BX[n]$(kno_no_ID_BX[n])..	PwThat[n] =E= sum(nn$(map_ID_BX[nn,n]),share[nn,n]*PwThat[nn]);
	E_qout_ID_BX[n]$(bra_o_ID_BX[n])..	qD[n] =E= sum(nn$(map_ID_BX[n,nn]), share[n,nn]*qS[nn])+epsi;
	E_qnout_ID_BX[n]$(bra_no_ID_BX[n])..	qD[n] =E= sum(nn$(map_ID_BX[n,nn]), share[n,nn]*(qD[nn]-epsi))+epsi;
$ENDBLOCK
$BLOCK M_ID_Y 
	E_sout_ID_Y[n,nn]$(map_ID_Y[n,nn] and bra_o_ID_Y[n])..	share[n,nn] =E= mu[n,nn] * (PbT[nn]/PwThat[n])**(sigma[nn]);
	E_snout_ID_Y[n,nn]$(map_ID_Y[n,nn] and bra_no_ID_Y[n])..	share[n,nn] =E= mu[n,nn] * (PwThat[nn]/PwThat[n])**(sigma[nn]);
	E_pout_ID_Y[n]$(ID_out_ID_Y[n])..	PbT[n] =E= sum(nn$(map_ID_Y[nn,n]),share[nn,n]*PwThat[nn]);
	E_pnout_ID_Y[n]$(kno_no_ID_Y[n])..	PwThat[n] =E= sum(nn$(map_ID_Y[nn,n]),share[nn,n]*PwThat[nn]);
	E_qout_ID_Y[n]$(bra_o_ID_Y[n])..	qD[n] =E= sum(nn$(map_ID_Y[n,nn]), share[n,nn]*qS[nn])+epsi;
	E_qnout_ID_Y[n]$(bra_no_ID_Y[n])..	qD[n] =E= sum(nn$(map_ID_Y[n,nn]), share[n,nn]*(qD[nn]-epsi))+epsi;
$ENDBLOCK
$BLOCK M_A4_ID_sum 
	E_ID_os_A4[n,nn]$(ID_e2t[n,nn] and kno_ID_TU[nn])..	os[n,nn] =E= sum(nnn$(ID_e2u[n,nnn] and ID_u2t[nnn,nn]), qD[nnn])/qD[nn];
	E_ID_qsumX_A4[n,nn]$(ID_e2ai[n,nn])..	qsumX[n,nn] =E= sum([nnn]$(ID_e2ai2i[n,nn,nnn] and bra_ID_BX[nnn]), qD[nnn]) + sum([nnn,nnnn]$(ID_e2ai2i[n,nn,nnn] and ID_e2t[n,nnnn] and ID_i2t[nnn,nnnn] and kno_ID_TU[nnnn]), qD[nnn]*os[n,nnnn]);
$ENDBLOCK
$BLOCK M_A4_ID_Em 
	E_M0_A4[z]..	M0[z] =E= sum(n$(ai[n]), phi[z,n]*qD[n]);
	E_ID_PwThat_A4[n]$(ID_inp[n])..	PwThat[n] =E= PwT[n]+sum(z, sum(nn$(ID_i2ai[n,nn]), phi[z,nn]*pMhat[z]));
$ENDBLOCK
$BLOCK M_A4_ID_agg 
	E_aggqD_ID_A4[n]$(ai[n])..	qD[n] =E= sum(nn$(ID_i2ai[nn,n]), qD[nn]);
	E_pMhat_ID_A4[z]..	pMhat[z] =E= pM[z];
$ENDBLOCK
$BLOCK M_A4_ID_calib_aux 
	E_currapp_ID_A4[n,nn]$(ID_e2t[n,nn] and kno_ID_TU[nn])..	currapp[n,nn] =E= sum(nnn$(ID_u2t[nnn,nn] and ID_e2u[n,nnn]), qD[nnn])/qD[n]+epsi;
	E_share_uc_A4[n,nn]$(map_ID_CU[n,nn] and bra_ID_TU[n])..	s_uc[n,nn] =E= mu[n,nn]*exp((PwThat[nn]-PwThat[n])*sigma[nn])/(
	sum(nnn$(map_ID_CU[nnn,nn] and bra_ID_TU[nnn]), mu[nnn,nn]*exp((PwThat[nn]-PwThat[nnn])*sigma[nn]))+
	sum(nnn$(map_ID_CU[nnn,nn] and bra_ID_BU[nnn]), mu[nnn,nn]*exp(sigma[nn]*(PwThat[nn]-sum(nnnn$(ID_e2u[nnnn,n]), sum(nnnnn$(ID_u2t[n,nnnnn]), gamma_tau[nnnn,nnnnn])*sum(nnnnn$(ID_u2t[nnn,nnnnn]), PwThat[nnnnn])))))
	);
	E_currapp_mod_A4[n,nn]$(ID_e2t[n,nn] and kno_ID_TU[nn])..	currapp_mod[n,nn] =E= sum([nnn,nnnn]$(ID_u2t[nnn,nn] and map_ID_EC[nnnn,n] and map_ID_CU[nnn,nnnn]), s_uc[nnn,nnnn] * qD[nnnn]/qD[n])+epsi;
$ENDBLOCK
$BLOCK M_A4_ID_minobj 
	E_minobj_ID_A4..	minobj =E= sum(map_gamma[n,nn,nnn,nnnn], Sqr(mu[nnn,nnnn]-gamma_tau[n,nn]))+weight_mu*sum([n,nn]$(map_ID_CU[n,nn] and bra_ID_TU[n]), Sqr(mu[n,nn]-mubar[n,nn]));
$ENDBLOCK
