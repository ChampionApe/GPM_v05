sets
	n
	alias_map2
	alias_set
;

alias(n,nnn,nn);

sets
	out_T_inp[n]
	endo_PbT[n]
	bra_o_C[n]
	bra_T_inp[n]
	map_T_out[n,nn]
	n_out[n]
	inp_T_inp[n]
	bra_no_C[n]
	bra_o_T_inp[n]
	bra_no_T_out[n]
	out_C[n]
	exo_mu[n,nn]
	alias_[alias_set,alias_map2]
	map_E[n,nn]
	int[n]
	kno_T_inp[n]
	kno_no_T_inp[n]
	bra_o_E[n]
	inp_T_out[n]
	out_T_out[n]
	kno_C[n]
	out_E[n]
	wT[n]
	kno_inp[n]
	fg[n]
	bra_E[n]
	kno_T_out[n]
	kno_no_C[n]
	map_T_inp[n,nn]
	kno_E[n]
	bra_no_T_inp[n]
	bra_o_T_out[n]
	inp[n]
	kno_out[n]
	kno_no_E[n]
	bra_T_out[n]
	inp_C[n]
	out[n]
	bra_no_E[n]
	map_all[n,nn]
	bra_C[n]
	inp_E[n]
	map_C[n,nn]
;

$GDXIN %A1%
$onMulti
$load n
$load alias_map2
$load alias_set
$load out_T_inp
$load endo_PbT
$load bra_o_C
$load bra_T_inp
$load n_out
$load inp_T_inp
$load bra_no_C
$load bra_o_T_inp
$load bra_no_T_out
$load out_C
$load int
$load kno_no_T_inp
$load kno_T_inp
$load bra_o_E
$load inp_T_out
$load out_T_out
$load kno_C
$load out_E
$load wT
$load kno_inp
$load fg
$load bra_E
$load kno_T_out
$load kno_no_C
$load kno_E
$load bra_no_T_inp
$load bra_o_T_out
$load inp
$load kno_out
$load kno_no_E
$load bra_T_out
$load inp_C
$load out
$load bra_no_E
$load bra_C
$load inp_E
$load exo_mu
$load map_all
$load alias_
$load map_T_out
$load map_T_inp
$load map_E
$load map_C
$GDXIN
$offMulti
