sets
	alias_set
	alias_map2
	n
;

alias(n,nn,nnn);

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
	map_ID_IOCU[n,nn]
	kno_ID_IOCU[n]
	bra_ID_IOCU[n]
	inp_ID_IOCU[n]
	out_ID_IOCU[n]
	ID_out_ID_IOCU[n]
	bra_o_ID_IOCU[n]
	bra_no_ID_IOCU[n]
	map_ID_IOX[n,nn]
	kno_ID_IOX[n]
	bra_ID_IOX[n]
	inp_ID_IOX[n]
	out_ID_IOX[n]
	ID_out_ID_IOX[n]
	kno_no_ID_IOX[n]
	bra_o_ID_IOX[n]
	bra_no_ID_IOX[n]
	map_ID_UbaseX[n,nn]
	kno_ID_UbaseX[n]
	bra_ID_UbaseX[n]
	inp_ID_UbaseX[n]
	out_ID_UbaseX[n]
	ID_out_ID_UbaseX[n]
	kno_no_ID_UbaseX[n]
	bra_o_ID_UbaseX[n]
	bra_no_ID_UbaseX[n]
	ID_params_alwaysexo_mu[n,nn]
	ID_endovars_exoincalib_C[n]
	ID_tech_endoincalib_mu[n,nn]
	ID_tech_endoincalib_sigma[n]
	ID_minobj_mu_subset[n,nn]
	ID_minobj_sigma_subset[n]
	ID_sumUaggs[n]
	ID_sumU2U[n,nn]
	sumXaggs[n]
	sumX2X[n,nn]
	ID_sumX2X[n,nn]
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
	EOP_sumUaggs[n]
	EOP_sumU2U[n,nn]
	map_M2C[n,nn]
;

$GDXIN %ID_0%
$onMulti
$load alias_set
$load alias_map2
$load n
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
$load kno_ID_IOCU
$load bra_ID_IOCU
$load inp_ID_IOCU
$load out_ID_IOCU
$load ID_out_ID_IOCU
$load bra_o_ID_IOCU
$load bra_no_ID_IOCU
$load kno_ID_IOX
$load bra_ID_IOX
$load inp_ID_IOX
$load out_ID_IOX
$load ID_out_ID_IOX
$load kno_no_ID_IOX
$load bra_o_ID_IOX
$load bra_no_ID_IOX
$load kno_ID_UbaseX
$load bra_ID_UbaseX
$load inp_ID_UbaseX
$load out_ID_UbaseX
$load ID_out_ID_UbaseX
$load kno_no_ID_UbaseX
$load bra_o_ID_UbaseX
$load bra_no_ID_UbaseX
$load ID_endovars_exoincalib_C
$load ID_tech_endoincalib_sigma
$load ID_minobj_sigma_subset
$load ID_sumUaggs
$load sumXaggs
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
$load EOP_sumUaggs
$load alias_
$load ID_map_all
$load map_ID_EC
$load map_ID_CU
$load map_ID_TU
$load map_ID_TX
$load map_ID_IOCU
$load map_ID_IOX
$load map_ID_UbaseX
$load ID_params_alwaysexo_mu
$load ID_tech_endoincalib_mu
$load ID_minobj_mu_subset
$load ID_sumU2U
$load sumX2X
$load ID_sumX2X
$load map_M2X
$load EOP_map_all
$load map_EOP_CU
$load map_EOP_TU
$load map_EOP_TX
$load EOP_params_alwaysexo_mu
$load EOP_sumU2U
$load map_M2C
$GDXIN
$offMulti
