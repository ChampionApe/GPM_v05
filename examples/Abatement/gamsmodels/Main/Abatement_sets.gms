sets
	alias_set
	alias_map2
	n
;

alias(n,nn,nnn);

sets
	alias_[alias_set,alias_map2]
	map_all[n,nn]
	inp[n]
	out[n]
	int[n]
	fg[n]
	wT[n]
	kno_out[n]
	kno_inp[n]
	map_ID_EC[n,nn]
	kno_ID_EC[n]
	bra_ID_EC[n]
	inp_ID_EC[n]
	out_ID_EC[n]
	kno_no_ID_EC[n]
	bra_o_ID_EC[n]
	bra_no_ID_EC[n]
	map_ID_CU[n,nn]
	kno_ID_CU[n]
	bra_ID_CU[n]
	inp_ID_CU[n]
	out_ID_CU[n]
	kno_no_ID_CU[n]
	bra_o_ID_CU[n]
	bra_no_ID_CU[n]
	map_ID_TU[n,nn]
	kno_ID_TU[n]
	bra_ID_TU[n]
	inp_ID_TU[n]
	out_ID_TU[n]
	bra_o_ID_TU[n]
	bra_no_ID_TU[n]
	map_ID_TX[n,nn]
	kno_ID_TX[n]
	bra_ID_TX[n]
	inp_ID_TX[n]
	out_ID_TX[n]
	kno_no_ID_TX[n]
	bra_o_ID_TX[n]
	bra_no_ID_TX[n]
	map_ID_IOCU[n,nn]
	kno_ID_IOCU[n]
	bra_ID_IOCU[n]
	inp_ID_IOCU[n]
	out_ID_IOCU[n]
	bra_o_ID_IOCU[n]
	bra_no_ID_IOCU[n]
	map_ID_IOX[n,nn]
	kno_ID_IOX[n]
	bra_ID_IOX[n]
	inp_ID_IOX[n]
	out_ID_IOX[n]
	kno_no_ID_IOX[n]
	bra_o_ID_IOX[n]
	bra_no_ID_IOX[n]
	map_ID_UbaseX[n,nn]
	kno_ID_UbaseX[n]
	bra_ID_UbaseX[n]
	inp_ID_UbaseX[n]
	out_ID_UbaseX[n]
	kno_no_ID_UbaseX[n]
	bra_o_ID_UbaseX[n]
	bra_no_ID_UbaseX[n]
	map_EOP_CU[n,nn]
	kno_EOP_CU[n]
	bra_EOP_CU[n]
	inp_EOP_CU[n]
	out_EOP_CU[n]
	kno_no_EOP_CU[n]
	bra_o_EOP_CU[n]
	bra_no_EOP_CU[n]
	map_EOP_TU[n,nn]
	kno_EOP_TU[n]
	bra_EOP_TU[n]
	inp_EOP_TU[n]
	out_EOP_TU[n]
	bra_o_EOP_TU[n]
	bra_no_EOP_TU[n]
	map_EOP_TX[n,nn]
	kno_EOP_TX[n]
	bra_EOP_TX[n]
	inp_EOP_TX[n]
	out_EOP_TX[n]
	kno_no_EOP_TX[n]
	bra_o_EOP_TX[n]
	bra_no_EOP_TX[n]
	tech_endoincalib_sigma[n]
	tech_endoincalib_mu[n,nn]
	params_alwaysexo_mu[n,nn]
	endovars_exoincalib_sumU[n,nn]
	endovars_exoincalib_sumX[n,nn]
	endovars_exoincalib_C[n]
	sumUaggs[n]
	sumU2U[n,nn]
	sumXaggs[n]
	sumX2X[n,nn]
	n_out[n]
	endo_PbT[n]
	exo_mu[n,nn]
;

$GDXIN %Abatement_0%
$onMulti
$load alias_set
$load alias_map2
$load n
$load inp
$load out
$load int
$load fg
$load wT
$load kno_out
$load kno_inp
$load kno_ID_EC
$load bra_ID_EC
$load inp_ID_EC
$load out_ID_EC
$load kno_no_ID_EC
$load bra_o_ID_EC
$load bra_no_ID_EC
$load kno_ID_CU
$load bra_ID_CU
$load inp_ID_CU
$load out_ID_CU
$load kno_no_ID_CU
$load bra_o_ID_CU
$load bra_no_ID_CU
$load kno_ID_TU
$load bra_ID_TU
$load inp_ID_TU
$load out_ID_TU
$load bra_o_ID_TU
$load bra_no_ID_TU
$load kno_ID_TX
$load bra_ID_TX
$load inp_ID_TX
$load out_ID_TX
$load kno_no_ID_TX
$load bra_o_ID_TX
$load bra_no_ID_TX
$load kno_ID_IOCU
$load bra_ID_IOCU
$load inp_ID_IOCU
$load out_ID_IOCU
$load bra_o_ID_IOCU
$load bra_no_ID_IOCU
$load kno_ID_IOX
$load bra_ID_IOX
$load inp_ID_IOX
$load out_ID_IOX
$load kno_no_ID_IOX
$load bra_o_ID_IOX
$load bra_no_ID_IOX
$load kno_ID_UbaseX
$load bra_ID_UbaseX
$load inp_ID_UbaseX
$load out_ID_UbaseX
$load kno_no_ID_UbaseX
$load bra_o_ID_UbaseX
$load bra_no_ID_UbaseX
$load kno_EOP_CU
$load bra_EOP_CU
$load inp_EOP_CU
$load out_EOP_CU
$load kno_no_EOP_CU
$load bra_o_EOP_CU
$load bra_no_EOP_CU
$load kno_EOP_TU
$load bra_EOP_TU
$load inp_EOP_TU
$load out_EOP_TU
$load bra_o_EOP_TU
$load bra_no_EOP_TU
$load kno_EOP_TX
$load bra_EOP_TX
$load inp_EOP_TX
$load out_EOP_TX
$load kno_no_EOP_TX
$load bra_o_EOP_TX
$load bra_no_EOP_TX
$load tech_endoincalib_sigma
$load endovars_exoincalib_C
$load sumUaggs
$load sumXaggs
$load n_out
$load endo_PbT
$load alias_
$load map_all
$load map_ID_EC
$load map_ID_CU
$load map_ID_TU
$load map_ID_TX
$load map_ID_IOCU
$load map_ID_IOX
$load map_ID_UbaseX
$load map_EOP_CU
$load map_EOP_TU
$load map_EOP_TX
$load tech_endoincalib_mu
$load params_alwaysexo_mu
$load endovars_exoincalib_sumU
$load endovars_exoincalib_sumX
$load sumU2U
$load sumX2X
$load exo_mu
$GDXIN
$offMulti