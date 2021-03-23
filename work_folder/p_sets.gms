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
	map_all[s,n,nn]
	inp[s,n]
	out[s,n]
	int[s,n]
	fg[n]
	wT[s,n]
	kno_out[s,n]
	kno_inp[s,n]
	t0[t]
	tE[t]
	tx0[t]
	txE[t]
	t0E[t]
	tx0E[t]
	map_lower_nests[s,n,nn]
	kno_lower_nests[s,n]
	bra_lower_nests[s,n]
	inp_lower_nests[s,n]
	out_lower_nests[s,n]
	kno_no_lower_nests[s,n]
	bra_o_lower_nests[s,n]
	bra_no_lower_nests[s,n]
	map_upper_nest[s,n,nn]
	kno_upper_nest[s,n]
	bra_upper_nest[s,n]
	inp_upper_nest[s,n]
	out_upper_nest[s,n]
	kno_no_upper_nest[s,n]
	bra_o_upper_nest[s,n]
	bra_no_upper_nest[s,n]
	s_prod[s]
	n_out[n]
	dur[n]
	dur2inv[n,nn]
	inv[n]
	ndur[n]
	endo_PbT[s,n]
	exo_mu[s,n,nn]
;

$GDXIN %p_1%
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
$load s_prod
$load n_out
$load dur
$load inv
$load ndur
$load alias_
$load map_all
$load inp
$load out
$load int
$load wT
$load kno_out
$load kno_inp
$load map_lower_nests
$load kno_lower_nests
$load bra_lower_nests
$load inp_lower_nests
$load out_lower_nests
$load kno_no_lower_nests
$load bra_o_lower_nests
$load bra_no_lower_nests
$load map_upper_nest
$load kno_upper_nest
$load bra_upper_nest
$load inp_upper_nest
$load out_upper_nest
$load kno_no_upper_nest
$load bra_o_upper_nest
$load bra_no_upper_nest
$load dur2inv
$load endo_PbT
$load exo_mu
$GDXIN
$offMulti
