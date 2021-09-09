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
	map_T_inp[n,nn]
	kno_T_inp[n]
	bra_T_inp[n]
	inp_T_inp[n]
	out_T_inp[n]
	kno_no_T_inp[n]
	bra_o_T_inp[n]
	bra_no_T_inp[n]
	map_T_out[n,nn]
	kno_T_out[n]
	bra_T_out[n]
	inp_T_out[n]
	out_T_out[n]
	bra_o_T_out[n]
	bra_no_T_out[n]
	map_C[n,nn]
	kno_C[n]
	bra_C[n]
	inp_C[n]
	out_C[n]
	kno_no_C[n]
	bra_o_C[n]
	bra_no_C[n]
	map_E[n,nn]
	kno_E[n]
	bra_E[n]
	inp_E[n]
	out_E[n]
	kno_no_E[n]
	bra_o_E[n]
	bra_no_E[n]
	n_out[n]
	endo_PbT[n]
	exo_mu[n,nn]
;

$GDXIN %A1_0%
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
$load kno_T_inp
$load bra_T_inp
$load inp_T_inp
$load out_T_inp
$load kno_no_T_inp
$load bra_o_T_inp
$load bra_no_T_inp
$load kno_T_out
$load bra_T_out
$load inp_T_out
$load out_T_out
$load bra_o_T_out
$load bra_no_T_out
$load kno_C
$load bra_C
$load inp_C
$load out_C
$load kno_no_C
$load bra_o_C
$load bra_no_C
$load kno_E
$load bra_E
$load inp_E
$load out_E
$load kno_no_E
$load bra_o_E
$load bra_no_E
$load n_out
$load endo_PbT
$load alias_
$load map_all
$load map_T_inp
$load map_T_out
$load map_C
$load map_E
$load exo_mu
$GDXIN
$offMulti
