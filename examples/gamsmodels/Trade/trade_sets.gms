sets
	alias_map2
	s
	alias_set
	n
	t
;

alias(n,nn,nnn);

sets
	alias_[alias_set,alias_map2]
	tE[t]
	tx0[t]
	txE[t]
	t0[t]
	dom2for[n,nn]
	t0E[t]
	n_for[n]
	tx0E[t]
	s_for[s]
	sfor_nfor[s,n]
	n_prod[n]
	sfor_ndom[s,n]
;

$GDXIN %rname%
$onMulti
$load s
$load n
$load t
$load alias_map2
$load alias_set
$load tE
$load tx0
$load txE
$load t0
$load t0E
$load n_for
$load tx0E
$load s_for
$load n_prod
$load dom2for
$load alias_
$load sfor_ndom
$load sfor_nfor
$GDXIN
$offMulti
