sets
	alias_set
	alias_map2
	n
	l1
;

alias(n,nn,nnn,nnnn,nnnnn,nnnnnn,nnnnnnn);

sets
	alias_[alias_set,alias_map2]
	ID_map_all[n,nn]
	ID_inp[n]
	ID_out[n]
	ID_int[n]
	fg[n]
	ID_wT[n]
	ID_kno_out[n]
	ID_kno_inp[n]
	map_ID_EC[n,nn]
	kno_ID_EC[n]
	bra_ID_EC[n]
	inp_ID_EC[n]
	out_ID_EC[n]
	ID_out_ID_EC[n]
	kno_no_ID_EC[n]
	bra_o_ID_EC[n]
	bra_no_ID_EC[n]
	map_ID_CU[n,nn]
	kno_ID_CU[n]
	bra_ID_CU[n]
	inp_ID_CU[n]
	out_ID_CU[n]
	ID_out_ID_CU[n]
	kno_no_ID_CU[n]
	bra_o_ID_CU[n]
	bra_no_ID_CU[n]
	map_ID_TU[n,nn]
	kno_ID_TU[n]
	bra_ID_TU[n]
	inp_ID_TU[n]
	out_ID_TU[n]
	ID_out_ID_TU[n]
	bra_o_ID_TU[n]
	bra_no_ID_TU[n]
	map_ID_TX[n,nn]
	kno_ID_TX[n]
	bra_ID_TX[n]
	inp_ID_TX[n]
	out_ID_TX[n]
	ID_out_ID_TX[n]
	kno_no_ID_TX[n]
	bra_o_ID_TX[n]
	bra_no_ID_TX[n]
	map_ID_BU[n,nn]
	kno_ID_BU[n]
	bra_ID_BU[n]
	inp_ID_BU[n]
	out_ID_BU[n]
	ID_out_ID_BU[n]
	bra_o_ID_BU[n]
	bra_no_ID_BU[n]
	map_ID_BX[n,nn]
	kno_ID_BX[n]
	bra_ID_BX[n]
	inp_ID_BX[n]
	out_ID_BX[n]
	ID_out_ID_BX[n]
	kno_no_ID_BX[n]
	bra_o_ID_BX[n]
	bra_no_ID_BX[n]
	map_ID_Y_in[n,nn]
	kno_ID_Y_in[n]
	bra_ID_Y_in[n]
	inp_ID_Y_in[n]
	out_ID_Y_in[n]
	ID_out_ID_Y_in[n]
	kno_no_ID_Y_in[n]
	bra_o_ID_Y_in[n]
	bra_no_ID_Y_in[n]
	map_ID_Y_out[n,nn]
	kno_ID_Y_out[n]
	bra_ID_Y_out[n]
	inp_ID_Y_out[n]
	out_ID_Y_out[n]
	ID_out_ID_Y_out[n]
	bra_o_ID_Y_out[n]
	bra_no_ID_Y_out[n]
	ID_params_alwaysexo_mu[n,nn]
	ID_endovars_exoincalib_E[n]
	ID_endovars_exoincalib_C[n]
	ID_tech_endoincalib_mu[n,nn]
	map_ID_TC[n,nn]
	map_ID_BUC[n,nn]
	map_ID_nonBUC[n,nn]
	map_T2E[n,nn]
	currapp_ID_subset[n]
	map_currapp_ID2T[n,nn]
	map_currapp_ID2E[n,nn]
	map_currapp2sumUE[n,nn,nnn]
	ID_sumUaggs[n]
	ID_sumU2U[n,nn]
	sumXinEaggs[n]
	sumXrestaggs[n]
	map_sumXrest2X_ID[n,nn]
	map_sumXinE2X[n,nn]
	map_sumXinE2E[n,nn]
	map_sumXinE2baselineinputs[n,nn]
	map_U2E[n,nn]
	map_M2X[n,nn]
	M_subset[n]
	EOP_map_all[n,nn]
	EOP_inp[n]
	EOP_out[n]
	EOP_int[n]
	EOP_wT[n]
	EOP_kno_out[n]
	EOP_kno_inp[n]
	map_EOP_CU[n,nn]
	kno_EOP_CU[n]
	bra_EOP_CU[n]
	inp_EOP_CU[n]
	out_EOP_CU[n]
	EOP_out_EOP_CU[n]
	kno_no_EOP_CU[n]
	bra_o_EOP_CU[n]
	bra_no_EOP_CU[n]
	map_EOP_TU[n,nn]
	kno_EOP_TU[n]
	bra_EOP_TU[n]
	inp_EOP_TU[n]
	out_EOP_TU[n]
	EOP_out_EOP_TU[n]
	bra_o_EOP_TU[n]
	bra_no_EOP_TU[n]
	map_EOP_TX[n,nn]
	kno_EOP_TX[n]
	bra_EOP_TX[n]
	inp_EOP_TX[n]
	out_EOP_TX[n]
	EOP_out_EOP_TX[n]
	kno_no_EOP_TX[n]
	bra_o_EOP_TX[n]
	bra_no_EOP_TX[n]
	EOP_params_alwaysexo_mu[n,nn]
	currapp_EOP_subset[n]
	map_currapp2sumUM[n,nn,nnn]
	EOP_sumUaggs[n]
	EOP_sumU2U[n,nn]
	map_sumXrest2X_EOP[n,nn]
	map_M2C[n,nn]
	sigma_l1_subset[n]
	eta_l1_subset[n]
;

$GDXIN %ID_0%
$onMulti
$load alias_set
$load alias_map2
$load n
$load l1
$load ID_inp
$load ID_out
$load ID_int
$load fg
$load ID_wT
$load ID_kno_out
$load ID_kno_inp
$load kno_ID_EC
$load bra_ID_EC
$load inp_ID_EC
$load out_ID_EC
$load ID_out_ID_EC
$load kno_no_ID_EC
$load bra_o_ID_EC
$load bra_no_ID_EC
$load kno_ID_CU
$load bra_ID_CU
$load inp_ID_CU
$load out_ID_CU
$load ID_out_ID_CU
$load kno_no_ID_CU
$load bra_o_ID_CU
$load bra_no_ID_CU
$load kno_ID_TU
$load bra_ID_TU
$load inp_ID_TU
$load out_ID_TU
$load ID_out_ID_TU
$load bra_o_ID_TU
$load bra_no_ID_TU
$load kno_ID_TX
$load bra_ID_TX
$load inp_ID_TX
$load out_ID_TX
$load ID_out_ID_TX
$load kno_no_ID_TX
$load bra_o_ID_TX
$load bra_no_ID_TX
$load kno_ID_BU
$load bra_ID_BU
$load inp_ID_BU
$load out_ID_BU
$load ID_out_ID_BU
$load bra_o_ID_BU
$load bra_no_ID_BU
$load kno_ID_BX
$load bra_ID_BX
$load inp_ID_BX
$load out_ID_BX
$load ID_out_ID_BX
$load kno_no_ID_BX
$load bra_o_ID_BX
$load bra_no_ID_BX
$load kno_ID_Y_in
$load bra_ID_Y_in
$load inp_ID_Y_in
$load out_ID_Y_in
$load ID_out_ID_Y_in
$load kno_no_ID_Y_in
$load bra_o_ID_Y_in
$load bra_no_ID_Y_in
$load kno_ID_Y_out
$load bra_ID_Y_out
$load inp_ID_Y_out
$load out_ID_Y_out
$load ID_out_ID_Y_out
$load bra_o_ID_Y_out
$load bra_no_ID_Y_out
$load ID_endovars_exoincalib_E
$load ID_endovars_exoincalib_C
$load currapp_ID_subset
$load ID_sumUaggs
$load sumXinEaggs
$load sumXrestaggs
$load M_subset
$load EOP_inp
$load EOP_out
$load EOP_int
$load EOP_wT
$load EOP_kno_out
$load EOP_kno_inp
$load kno_EOP_CU
$load bra_EOP_CU
$load inp_EOP_CU
$load out_EOP_CU
$load EOP_out_EOP_CU
$load kno_no_EOP_CU
$load bra_o_EOP_CU
$load bra_no_EOP_CU
$load kno_EOP_TU
$load bra_EOP_TU
$load inp_EOP_TU
$load out_EOP_TU
$load EOP_out_EOP_TU
$load bra_o_EOP_TU
$load bra_no_EOP_TU
$load kno_EOP_TX
$load bra_EOP_TX
$load inp_EOP_TX
$load out_EOP_TX
$load EOP_out_EOP_TX
$load kno_no_EOP_TX
$load bra_o_EOP_TX
$load bra_no_EOP_TX
$load currapp_EOP_subset
$load EOP_sumUaggs
$load sigma_l1_subset
$load eta_l1_subset
$load alias_
$load ID_map_all
$load map_ID_EC
$load map_ID_CU
$load map_ID_TU
$load map_ID_TX
$load map_ID_BU
$load map_ID_BX
$load map_ID_Y_in
$load map_ID_Y_out
$load ID_params_alwaysexo_mu
$load ID_tech_endoincalib_mu
$load map_ID_TC
$load map_ID_BUC
$load map_ID_nonBUC
$load map_T2E
$load map_currapp_ID2T
$load map_currapp_ID2E
$load map_currapp2sumUE
$load ID_sumU2U
$load map_sumXrest2X_ID
$load map_sumXinE2X
$load map_sumXinE2E
$load map_sumXinE2baselineinputs
$load map_U2E
$load map_M2X
$load EOP_map_all
$load map_EOP_CU
$load map_EOP_TU
$load map_EOP_TX
$load EOP_params_alwaysexo_mu
$load map_currapp2sumUM
$load EOP_sumU2U
$load map_sumXrest2X_EOP
$load map_M2C
$GDXIN
$offMulti
