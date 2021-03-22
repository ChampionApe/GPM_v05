sets
	alias_set
	alias_map2
	t
	n
	s
;


sets
	alias_[alias_set,alias_map2]
	t0[t]
	tE[t]
	tx0[t]
	txE[t]
	t0E[t]
	tx0E[t]
	n_equi[n]
	d_qD[s,n]
	d_qS[s,n]
	Peq_endo[n]
	qS_endo[s,n]
;

$GDXIN %rname%
$onMulti
$load alias_set
$load alias_map2
$load t
$load n
$load s
$load t0
$load tE
$load tx0
$load txE
$load t0E
$load tx0E
$load n_equi
$load Peq_endo
$load alias_
$load d_qD
$load d_qS
$load qS_endo
$GDXIN
$offMulti
