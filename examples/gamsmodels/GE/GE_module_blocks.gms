$BLOCK M_GE_module_eqt0 
	E_equi_GE_module[t,n]$(n_equi[n] and t0[t])..	sum(s$(d_qS[s,n]), qS[t,s,n]) =E= sum(s$(d_qD[s,n]), qD[t,s,n]);
$ENDBLOCK
$BLOCK M_GE_module_eqtx0E 
	E_equi_tx0E_GE_module[t,n]$(n_equi[n] and tx0E[t])..	sum(s$(d_qS[s,n]), qS[t,s,n]) =E= sum(s$(d_qD[s,n]), qD[t,s,n]);
$ENDBLOCK
