sets
	alias_set
	alias_map2
	n
	s
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
	n_out[n]
	s_prod[s]
	endo_PbT[s,n]
	exo_mu[s,n,nn]
;

$GDXIN %p_0%
$onMulti
$load alias_set
$load alias_map2
$load n
$load s
$load fg
$load n_out
$load s_prod
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
$load endo_PbT
$load exo_mu
$GDXIN
$offMulti
