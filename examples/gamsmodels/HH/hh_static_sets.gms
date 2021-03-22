sets
	n
	s
	alias_map2
	alias_set
;

alias(n,nn,nnn);

sets
	kno_HH_agg[s,n]
	map_HH[s,n,nn]
	qs_qd_HH[s,n]
	exo_HH_agg[s,n]
	alias_[alias_set,alias_map2]
	int_HH_agg[s,n]
	top_HH_agg[s,n]
	out_HH_agg[s,n]
	map_all_HH_agg[s,n,nn]
	s_HH[s]
	qd_qs_HH[s,n]
	endo_mu[s,n]
	int_temp_HH[s,n]
	qs_qs_HH[s,n]
	out_HH[s,n]
	qd_qd_HH[s,n]
	inp_HH[s,n]
	inp_HH_agg[s,n]
	int_temp_HH_agg[s,n]
	kno_HH[s,n]
	fg_HH[n]
;

$GDXIN %HH_agg_0%
$onMulti
$load n
$load s
$load alias_map2
$load alias_set
$load fg_HH
$load s_HH
$load kno_HH_agg
$load map_HH
$load qs_qd_HH
$load exo_HH_agg
$load alias_
$load int_HH_agg
$load top_HH_agg
$load kno_HH
$load out_HH_agg
$load map_all_HH_agg
$load qd_qs_HH
$load endo_mu
$load int_temp_HH
$load out_HH
$load qd_qd_HH
$load inp_HH
$load inp_HH_agg
$load int_temp_HH_agg
$load qs_qs_HH
$GDXIN
$offMulti
