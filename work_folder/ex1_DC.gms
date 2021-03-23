sets
	alias_set
	alias_map2
	l1
	t
	s
	n
;


sets
	alias_[alias_set,alias_map2]
	qD_l1_subset[t,s,n]
	Peq_l1_subset[t,n]
	qS_l1_subset[t,s,n]
	vD_l1_subset[t,s,n]
	tauD_l1_subset[t,s,n]
;

$GDXIN %shock%
$onMulti
$load alias_set
$load alias_map2
$load l1
$load t
$load s
$load n
$load alias_
$load qD_l1_subset
$load Peq_l1_subset
$load qS_l1_subset
$load vD_l1_subset
$load tauD_l1_subset
$GDXIN
$offMulti
 parameters
	qD_l1[t,s,n,l1]
	Peq_l1[t,n,l1]
	qS_l1[t,s,n,l1]
	vD_l1[t,s,n,l1]
	tauD_l1[t,s,n,l1]
;

$GDXIN %shock%
$onMulti
$load qD_l1
$load Peq_l1
$load qS_l1
$load vD_l1
$load tauD_l1
$offMulti
 loop( (l1), 	qD.fx[t,s,n]$(qD_l1_subset[t,s,n]) = qD_l1[t,s,n,l1];
	Peq.fx[t,n]$(Peq_l1_subset[t,n]) = Peq_l1[t,n,l1];
	qS.fx[t,s,n]$(qS_l1_subset[t,s,n]) = qS_l1[t,s,n,l1];
	vD.fx[t,s,n]$(vD_l1_subset[t,s,n]) = vD_l1[t,s,n,l1];
	tauD.fx[t,s,n]$(tauD_l1_subset[t,s,n]) = tauD_l1[t,s,n,l1];


solve ex1_DC using CNS;

)
		