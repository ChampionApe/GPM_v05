sets
	n
	s
	alias_map2
	alias_set
	t
;

alias(n,nn);

sets
	n_equi[n]
	tx0[t]
	tx0E[t]
	inv[n]
	s_itory[s]
	d_qS[s,n]
	d_vD[s,n]
	txE[t]
	d_PbT[s,n]
	d_tauLump[s]
	n_fg[n]
	d_qD[s,n]
	d_tauD[s,n]
	s_tax[s]
	dur[n]
	d_tauS[s,n]
	dur2inv[n,nn]
	n_tax[n]
	s_for[s]
	s_inv[s]
	alias_[alias_set,alias_map2]
	t0E[t]
	s_prod[s]
	tauDendo[s,n]
	n_for[n]
	t0[t]
	sfor_nfor[s,n]
	d_PwT[s,n]
	tE[t]
	d_Peq[n]
	s_HH[s]
	sfor_ndom[s,n]
	inp_HH[s,n]
	n_prod[n]
	itoryD[s,n]
	out_HH[s,n]
	d_vS[s,n]
;

$GDXIN %GE_data%
$onMulti
$load alias_map2
$load n
$load t
$load alias_set
$load s
$load n_equi
$load tx0
$load n_tax
$load s_for
$load tx0E
$load s_inv
$load inv
$load s_itory
$load t0E
$load s_prod
$load txE
$load n_for
$load t0
$load d_tauLump
$load n_fg
$load tE
$load d_Peq
$load s_HH
$load n_prod
$load s_tax
$load dur
$load d_tauS
$load dur2inv
$load alias_
$load d_qS
$load d_vD
$load tauDendo
$load sfor_nfor
$load d_PbT
$load d_PwT
$load d_qD
$load sfor_ndom
$load inp_HH
$load itoryD
$load d_tauD
$load out_HH
$load d_vS
$GDXIN
$offMulti
