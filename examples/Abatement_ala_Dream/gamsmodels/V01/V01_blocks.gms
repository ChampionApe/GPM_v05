$BLOCK M_V01_NT
	E_V01_NT_ZP_out[s,n]$(V01_NT_out[s,n])..		pS[s,n]*qS[s,n]	=E= sum(nn$(V01_map[s,nn,n]), qD[s,nn]*sum(nnn$(V01_x2inp[s,nn,nnn]), pD[s,nnn]));
	E_V01_NT_ZP_nout[s,n]$(V01_NT_int[s,n])..		pD[s,n]*qD[s,n]	=E= sum(nn$(V01_map[s,nn,n]), qD[s,nn]*sum(nnn$(V01_x2inp[s,nn,nnn]), pD[s,nnn]));
	E_V01_NT_qD_out[s,n]$(V01_NT_bra_out[s,n])..	qD[s,n]			=E=	sum(nn$(V01_map[s,n,nn]), mu[s,n,nn]*(pS[s,nn]/sum(nnn$(V01_x2inp[s,n,nnn]), pD[s,nnn]))**(sigma[s,nn]) * qS[s,nn]);
	E_V01_NT_qD_nout[s,n]$(V01_NT_bra_nout[s,n])..	qD[s,n]			=E= sum(nn$(V01_map[s,n,nn]), mu[s,n,nn]*(pD[s,nn]/sum(nnn$(V01_x2inp[s,n,nnn]), pD[s,nnn]))**(sigma[s,nn]) * qD[s,nn]);
$ENDBLOCK

$BLOCK M_V01_T_always
	E_V01_T_qD[s,n]$(V01_T[s,n])..		qD[s,n]	=E= @TechLogit(pD[s,n],lambda[s,nn],sigma[s,nn],mu[s,n,nn],V01_map[s,n,nn]);
	E_V01_T_pES[s,n]$(V01_ES[s,n])..	pD[s,n]	=E= sum(nn$(V01_map[s,nn,n]), qD[s,nn]*theta[s,nn]*pD[s,nn]);
	E_V01_T_pT[s,n]$(V01_T[s,n])..		pD[s,n]	=E= sum(nn$(V01_map[s,nn,n]), mu[s,nn,n]*pD[s,nn]);
$ENDBLOCK

$BLOCK M_V01_T_base
	E_V01_T_sum[s,n]$(V01_ES[s,n])..	1 		=E= sum(nn$(V01_map[s,nn,n]), qD[s,nn]*theta[s,nn]);
$ENDBLOCK

$BLOCK M_V01_ACC
	E_V01_ACC_inp[s,n]$(V01_inp[s,n])..		qD[s,n]		=E= sum(nn$(V01_x2inp[s,nn,n]), qD[s,nn])+sum(nn$(V01_ES[s,nn]), qD[s,nn] * sum(nnn$(V01_map[s,nnn,nn] and V01_map[s,n,nnn]), mu[s,n,nnn]*qD[s,nnn]*theta[s,nnn]));
$ENDBLOCK
