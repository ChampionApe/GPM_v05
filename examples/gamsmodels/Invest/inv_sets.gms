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
	I_map_all[s,n,nn]
	I_inp[s,n]
	I_out[s,n]
	I_int[s,n]
	fg[n]
	I_wT[s,n]
	I_kno_out[s,n]
	I_kno_inp[s,n]
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
	I_out_nest[s,n]
	kno_no_nest[s,n]
	bra_o_nest[s,n]
	bra_no_nest[s,n]
	s_inv[s]
	I_n_out[n]
	I_endo_PbT[s,n]
	I_exo_mu[s,n,nn]
;

$GDXIN %inv_2%
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
$load I_n_out
$load alias_
$load I_map_all
$load I_inp
$load I_out
$load I_int
$load I_wT
$load I_kno_out
$load I_kno_inp
$load map_nest
$load kno_nest
$load bra_nest
$load inp_nest
$load out_nest
$load I_out_nest
$load kno_no_nest
$load bra_o_nest
$load bra_no_nest
$load I_endo_PbT
$load I_exo_mu
$GDXIN
$offMulti
