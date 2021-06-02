parameters
	load_PwT[n]
	load_PbT[n]
	load_qD[n]
	load_Peq[n]
	load_qsumU[n]
	load_qsumX[n]
	load_sigma[n]
	load_mu[n,nn]
	load_eta[n]
	load_tauS[n]
	load_tauLump
	load_qS[n]
	load_markup[n]
	Abatement_B_modelstat
	Abatement_B_solvestat
	sigma_l1[n,l1]
	eta_l1[n,l1]
;

$GDXIN %Abatement_0%
$onMulti
$load load_PwT
$load load_PbT
$load load_qD
$load load_Peq
$load load_qsumU
$load load_qsumX
$load load_sigma
$load load_mu
$load load_eta
$load load_tauS
$load load_tauLump
$load load_qS
$load load_markup
$load Abatement_B_modelstat
$load Abatement_B_solvestat
$load sigma_l1
$load eta_l1
$offMulti
