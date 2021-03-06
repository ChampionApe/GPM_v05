parameters
	load_PwThat[n]
	load_PbT[n]
	load_pMhat[z]
	load_qD[n]
	load_os[n,nn]
	load_M0[z]
	load_s_uc[n,nn]
	load_qsumX[n,nn]
	load_currapp[n,nn]
	load_currapp_mod[n,nn]
	load_sigma[n]
	load_mu[n,nn]
	load_eta[n]
	load_phi[z,n]
	load_pM[z]
	load_PwT[n]
	load_qS[n]
	load_gamma_tau[n,nn]
	atest_ID_modelstat
	atest_ID_solvestat
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
$load load_qsumX
$load load_currapp
$load load_currapp_mod
$load load_sigma
$load load_mu
$load load_eta
$load load_phi
$load load_pM
$load load_PwT
$load load_qS
$load load_gamma_tau
$load atest_ID_modelstat
$load atest_ID_solvestat
$offMulti
