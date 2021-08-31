parameters
	load_PwThat[n]
	load_PbT[n]
	load_M0[n]
	load_qD[n]
	load_qsumU[n]
	load_pMhat[n]
	load_qS[n]
	load_M[n]
	load_currapp_ID[n]
	load_qsumX[n]
	load_currapp_EOP[n]
	load_currapp_ID_modified[n]
	load_sigma[n]
	load_mu[n,nn]
	load_eta[n]
	load_PwT[n]
	load_pM[n]
	load_phi[n,nn]
	load_theta[n]
	load_muG[n]
	load_sigmaG[n]
	load_gamma_tau[n,nn]
	Abatement_EOP_modelstat
	Abatement_EOP_solvestat
	sigma_l1[n,l1]
	eta_l1[n,l1]
;

$GDXIN %ID_0%
$onMulti
$load load_PwThat
$load load_PbT
$load load_M0
$load load_qD
$load load_qsumU
$load load_pMhat
$load load_qS
$load load_M
$load load_currapp_ID
$load load_qsumX
$load load_currapp_EOP
$load load_currapp_ID_modified
$load load_sigma
$load load_mu
$load load_eta
$load load_PwT
$load load_pM
$load load_phi
$load load_theta
$load load_muG
$load load_sigmaG
$load load_gamma_tau
$load Abatement_EOP_modelstat
$load Abatement_EOP_solvestat
$load sigma_l1
$load eta_l1
$offMulti
