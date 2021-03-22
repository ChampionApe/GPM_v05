sets
	alias_set
	alias_map2
	n
	s
	t
;

alias(n,nn,nnn);

sets
	alias_[alias_set,alias_map2]
	GE_map_all[s,n,nn]
	GE_inp[s,n]
	GE_out[s,n]
	GE_int[s,n]
	fg[n]
	GE_wT[s,n]
	GE_kno_out[s,n]
	GE_kno_inp[s,n]
	t0[t]
	tE[t]
	tx0[t]
	txE[t]
	t0E[t]
	tx0E[t]
	map_nest[s,n,nn]
	kno_nest[s,n]
	bra_nest[s,n]
	inp_nest[s,n]
	out_nest[s,n]
	GE_out_nest[s,n]
	kno_no_nest[s,n]
	bra_o_nest[s,n]
	bra_no_nest[s,n]
	s_inv[s]
	GE_n_out[n]
	GE_endo_PbT[s,n]
	GE_exo_mu[s,n,nn]
;

$GDXIN %inv_1%
$onMulti
$load alias_set
$load alias_map2
$load n
$load s
$load t
$load fg
$load t0
$load tE
$load tx0
$load txE
$load t0E
$load tx0E
$load s_inv
$load GE_n_out
$load alias_
$load GE_map_all
$load GE_inp
$load GE_out
$load GE_int
$load GE_wT
$load GE_kno_out
$load GE_kno_inp
$load map_nest
$load kno_nest
$load bra_nest
$load inp_nest
$load out_nest
$load GE_out_nest
$load kno_no_nest
$load bra_o_nest
$load bra_no_nest
$load GE_endo_PbT
$load GE_exo_mu
$GDXIN
$offMulti
