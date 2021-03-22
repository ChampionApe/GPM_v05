sets
	alias_set
	alias_map2
	t
	n
	s
;

alias(n,nn,nnn);

sets
	alias_[alias_set,alias_map2]
	t0[t]
	tE[t]
	tx0[t]
	txE[t]
	t0E[t]
	tx0E[t]
	n_for[n]
	s_for[s]
	n_prod[n]
	sfor_ndom[s,n]
	sfor_nfor[s,n]
	dom2for[n,nn]
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
$load n_for
$load s_for
$load n_prod
$load alias_
$load sfor_ndom
$load sfor_nfor
$load dom2for
$GDXIN
$offMulti
