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
	load_sigma[n]
	load_eta[n]
	load_phi[z,n]
	load_pM[z]
	load_PwT[n]
	load_qS[n]
	load_epsi
	load_gamma_tau[n,nn]
	load_mu[n,nn]
	A3_ID_modelstat
	A3_ID_solvestat
	load_minobj
	load_weight_mu
	load_mubar[n,nn]
	A3_ID_calibrate_modelstat
	A3_ID_calibrate_solvestat
	sol_qD[l1,n]
	sol_PwThat[l1,n]
	sol_mu[l1,n,nn]
	sol_gamma_tau[l1,n,nn]
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
$load load_sigma
$load load_eta
$load load_phi
$load load_pM
$load load_PwT
$load load_qS
$load load_epsi
$load load_gamma_tau
$load load_mu
$load A3_ID_modelstat
$load A3_ID_solvestat
$load load_minobj
$load load_weight_mu
$load load_mubar
$load A3_ID_calibrate_modelstat
$load A3_ID_calibrate_solvestat
$load sol_qD
$load sol_PwThat
$load sol_mu
$load sol_gamma_tau
$offMulti
