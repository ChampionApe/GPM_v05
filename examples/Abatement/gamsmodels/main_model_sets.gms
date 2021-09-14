sets
	alias_set
	alias_map2
	n
	z
	l1
;

alias(n,nn,nnn,nnnn,nnnnn);

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
	map_ID_Y[n,nn]
	kno_ID_Y[n]
	bra_ID_Y[n]
	inp_ID_Y[n]
	out_ID_Y[n]
	ID_out_ID_Y[n]
	kno_no_ID_Y[n]
	bra_o_ID_Y[n]
	bra_no_ID_Y[n]
	ID_t_all[n]
	ID_i2ai[n,nn]
	ai[n]
	ID_i2t[n,nn]
	ID_u2t[n,nn]
	ID_e2u[n,nn]
	ID_e2t[n,nn]
	ID_e2ai2i[n,nn,nnn]
	ID_e2ai[n,nn]
	map_gamma[n,nn,nnn,nnnn]
	ID_mu_endoincalib[n,nn]
	ID_mu_exo[n,nn]
	mu_l1_subset[n,nn]
	eta_l1_subset[n]
	sigma_l1_subset[n]
;

$GDXIN %ID_0%
$onMulti
$load alias_set
$load alias_map2
$load n
$load z
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
$load kno_ID_Y
$load bra_ID_Y
$load inp_ID_Y
$load out_ID_Y
$load ID_out_ID_Y
$load kno_no_ID_Y
$load bra_o_ID_Y
$load bra_no_ID_Y
$load ID_t_all
$load ai
$load eta_l1_subset
$load sigma_l1_subset
$load alias_
$load ID_map_all
$load map_ID_EC
$load map_ID_CU
$load map_ID_TU
$load map_ID_TX
$load map_ID_BU
$load map_ID_BX
$load map_ID_Y
$load ID_i2ai
$load ID_i2t
$load ID_u2t
$load ID_e2u
$load ID_e2t
$load ID_e2ai2i
$load ID_e2ai
$load map_gamma
$load ID_mu_endoincalib
$load ID_mu_exo
$load mu_l1_subset
$GDXIN
$offMulti
