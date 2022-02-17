$BLOCK B_V1
	E_V1_OptimalTau[i]..	tau[i]	=E= 1/(1+exp((p[i]-lambda)/sigma));
	E_V1_Scale..			1		=E=	sum(i, theta[i]*tau[i]);
	E_V1_lambda..			lambda	=E= pe-sigma*sum(i, theta[i]*tau[i]*(log(tau[i])*(1-tau[i])+log(1-tau[i])*tau[i]));
$ENDBLOCK

$BlOCK B_V2
	E_V2_OptimalTau[i]..	tau[i]	=E= 1/(1+exp((p[i]-lambda)/sigma));
	E_V2_Scale..			1 		=E= sum(i, theta[i]*tau[i]);
	E_V2_pe..				pe 		=E= sum(i, theta[i]*tau[i]*(1+sigma*(log(tau[i])*(2-tau[i])-(1-tau[i])*log(1-tau[i]))));
$ENDBLOCK