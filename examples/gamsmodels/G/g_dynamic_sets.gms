sets
	alias_map2
	s
	alias_set
	n
	t
;

alias(n,nn);

sets
	tE[t]
	d_tauS[s,n]
	d_PbT[s,n]
	t0[t]
	d_tauD[s,n]
	s_prod[s]
	tx0E[t]
	n_tax[n]
	d_tauLump[s]
	dur[n]
	n_fg[n]
	inv[n]
	n_prod[n]
	d_qD[s,n]
	dur2inv[n,nn]
	d_qS[s,n]
	d_vS[s,n]
	n_equi[n]
	d_vD[s,n]
	tauDendo[s,n]
	sfor_nfor[s,n]
	alias_[alias_set,alias_map2]
	s_itory[s]
	s_HH[s]
	inp_HH[s,n]
	s_G[s]
	t0E[t]
	sfor_ndom[s,n]
	tx0[t]
	gsvngs[n]
	txE[t]
	s_tax[s]
	s_for[s]
	n_for[n]
	itoryD[s,n]
	s_inv[s]
	d_PwT[s,n]
	out_HH[s,n]
	d_Peq[n]
;

$GDXIN %GE_data%
$onMulti
$load s
$load n
$load t
$load alias_map2
$load alias_set
$load s_itory
$load s_HH
$load tE
$load t0
$load s_G
$load s_prod
$load t0E
$load tx0E
$load n_tax
$load d_tauLump
$load dur
$load n_fg
$load inv
$load n_prod
$load tx0
$load gsvngs
$load txE
$load s_tax
$load s_for
$load n_equi
$load n_for
$load s_inv
$load d_Peq
$load alias_
$load inp_HH
$load d_tauS
$load d_PbT
$load d_tauD
$load d_qD
$load d_qS
$load dur2inv
$load sfor_ndom
$load d_vS
$load itoryD
$load d_vD
$load tauDendo
$load d_PwT
$load sfor_nfor
$load out_HH
$GDXIN
$offMulti
