$BLOCK M_nested_CES
	E_s[n,nn]$(map[n,nn])..	share[n,nn] =E= mu[n,nn] * (P[nn]/P[n])**(sigma[nn]);
	E_p[n]$(kno[n])..	P[n] =E= sum(nn$(map[nn,n]), share[nn,n]*P[nn]);
	E_q[n]$(bra[n])..	q[n] =E= sum(nn$(map[n,nn]), share[n,nn]*(q[nn]-epsi))+epsi;
$ENDBLOCK
