parameters
	load_PwThat[n]
	load_PbT[n]
	load_pMhat[z]
	load_qD[n]
	load_os[n,nn]
	load_M0[z]
	load_s_uc[n,nn]
	load_share[n,nn]
	load_qsumX[n,nn]
	load_currapp[n,nn]
	load_currapp_mod[n,nn]
	load_qS[n]
	load_M[z]
	load_currapp_EOP[z,n]
	load_sigma[n]
	load_mu[n,nn]
	load_eta[n]
	load_phi[z,n]
	load_pM[z]
	load_PwT[n]
	load_epsi
	load_gamma_tau[n,nn]
	load_theta[z,n]
	load_muG[n]
	load_sigmaG[n]
	A3_EOP_modelstat
	A3_EOP_solvestat
	sigmaG_l1[n,l1]
	sigma_l1[n,l1]
	mu_l1[n,nn,l1]
	eta_l1[n,l1]
;

$GDXIN %ID_0%
$onMulti
$load load_PwThat
$load load_PbT
$load load_pMhat
$load load_qD
$load load_os
$load load_M0
$load load_s_uc
$load load_share
$load load_qsumX
$load load_currapp
$load load_currapp_mod
$load load_qS
$load load_M
$load load_currapp_EOP
$load load_sigma
$load load_mu
$load load_eta
$load load_phi
$load load_pM
$load load_PwT
$load load_epsi
$load load_gamma_tau
$load load_theta
$load load_muG
$load load_sigmaG
$load A3_EOP_modelstat
$load A3_EOP_solvestat
$load sigmaG_l1
$load sigma_l1
$load mu_l1
$load eta_l1
$offMulti
