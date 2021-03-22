sets
	alias_set
	alias_map2
	s
	n
	t
;

alias(n,nn);

sets
	alias_[alias_set,alias_map2]
	s_prod[s]
	n_prod[n]
	n_fg[n]
	s_for[s]
	n_for[n]
	sfor_ndom[s,n]
	sfor_nfor[s,n]
	s_HH[s]
	inp_HH[s,n]
	out_HH[s,n]
	n_tax[n]
	s_tax[s]
	s_itory[s]
	s_inv[s]
	inv[n]
	dur2inv[n,nn]
	dur[n]
	itoryD[s,n]
	n_equi[n]
	d_Peq[n]
	d_vS[s,n]
	d_vD[s,n]
	d_PwT[s,n]
	d_PbT[s,n]
	d_qD[s,n]
	d_qS[s,n]
	d_tauS[s,n]
	d_tauD[s,n]
	d_tauLump[s]
	t0[t]
	tE[t]
	tx0[t]
	txE[t]
	t0E[t]
	tx0E[t]
;

$GDXIN %GE_data_3%
$onMulti
$load alias_set
$load alias_map2
$load s
$load n
$load t
$load s_prod
$load n_prod
$load n_fg
$load s_for
$load n_for
$load s_HH
$load n_tax
$load s_tax
$load s_itory
$load s_inv
$load inv
$load dur
$load n_equi
$load d_Peq
$load d_tauLump
$load t0
$load tE
$load tx0
$load txE
$load t0E
$load tx0E
$load alias_
$load sfor_ndom
$load sfor_nfor
$load inp_HH
$load out_HH
$load dur2inv
$load itoryD
$load d_vS
$load d_vD
$load d_PwT
$load d_PbT
$load d_qD
$load d_qS
$load d_tauS
$load d_tauD
$GDXIN
$offMulti
