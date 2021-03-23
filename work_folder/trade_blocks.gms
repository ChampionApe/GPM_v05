$BLOCK M_trade 
	E_fdemand_trade[t,s,n]$(sfor_ndom[s,n] and txE[t])..	qD[t,s,n] =E= sum(nn$(dom2for[n,nn]), phi[s,n] * (Peq[t,nn]/PwT[t,s,n])**(sigma[s,n]));
$ENDBLOCK
