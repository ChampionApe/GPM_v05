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
	inp_HH[s,n]
	out_HH[s,n]
	int_HH[s,n]
	kno_HH[s,n]
	map_all_HH[s,n,nn]
	int_temp_HH[s,n]
	exo_HH[s,n]
	top_HH[s,n]
	inp_HH_agg[s,n]
	out_HH_agg[s,n]
	kno_HH_agg[s,n]
	map_HH_agg[s,n,nn]
	qs_qs_HH_agg[s,n]
	qs_qd_HH_agg[s,n]
	qd_qd_HH_agg[s,n]
	qd_qs_HH_agg[s,n]
	int_temp_HH_agg[s,n]
	t0[t]
	tE[t]
	tx0[t]
	txE[t]
	t0E[t]
	tx0E[t]
	endo_mu[s,n]
	s_HH[s]
	fg_HH[n]
	svngs[n]
;

$GDXIN %HH_1%
$onMulti
$load alias_set
$load alias_map2
$load n
$load s
$load t
$load t0
$load tE
$load tx0
$load txE
$load t0E
$load tx0E
$load s_HH
$load fg_HH
$load svngs
$load alias_
$load inp_HH
$load out_HH
$load int_HH
$load kno_HH
$load map_all_HH
$load int_temp_HH
$load exo_HH
$load top_HH
$load inp_HH_agg
$load out_HH_agg
$load kno_HH_agg
$load map_HH_agg
$load qs_qs_HH_agg
$load qs_qd_HH_agg
$load qd_qd_HH_agg
$load qd_qs_HH_agg
$load int_temp_HH_agg
$load endo_mu
$GDXIN
$offMulti
