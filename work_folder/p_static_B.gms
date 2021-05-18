sets
	alias_set
	alias_map2
	l1
	s
	n
;


sets
	alias_[alias_set,alias_map2]
	PwT_l1_subset[s,n]
	qS_l1_subset[s,n]
	tauS_l1_subset[s,n]
	tauLump_l1_subset[s]
;

$GDXIN %shock%
$onMulti
$load alias_set
$load alias_map2
$load l1
$load s
$load n
$load tauLump_l1_subset
$load alias_
$load PwT_l1_subset
$load qS_l1_subset
$load tauS_l1_subset
$GDXIN
$offMulti
 parameters
	PwT_l1[s,n,l1]
	qS_l1[s,n,l1]
	tauS_l1[s,n,l1]
	tauLump_l1[s,l1]
;

$GDXIN %shock%
$onMulti
$load PwT_l1
$load qS_l1
$load tauS_l1
$load tauLump_l1
$offMulti
 loop( (l1), 	PwT.fx[s,n]$(PwT_l1_subset[s,n]) = PwT_l1[s,n,l1];
	qS.fx[s,n]$(qS_l1_subset[s,n]) = qS_l1[s,n,l1];
	tauS.fx[s,n]$(tauS_l1_subset[s,n]) = tauS_l1[s,n,l1];
	tauLump.fx[s]$(tauLump_l1_subset[s]) = tauLump_l1[s,l1];


solve p_static_B using CNS;

)
		