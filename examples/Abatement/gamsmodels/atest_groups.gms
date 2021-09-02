$GROUP atest_g_ID_alwaysendo
PwThat[n]$((ID_int[n] or ID_inp[n])) ""
PbT[n]$(ID_out[n]) ""
pMhat[z] ""
qD[n]$(((ID_int[n] or ID_inp[n]) and not (kno_ID_EC[n] or kno_ID_CU[n]))) ""
qsumU[n,nn]$(ID_e2t[n,nn]) ""
os[n,nn]$(ID_e2t[n,nn]) ""
M0[z] ""
;

$GROUP atest_g_ID_exoincalib
qD[n]$((ai[n] or kno_ID_EC[n] or kno_ID_CU[n])) ""
qsumX[n,nn]$(ID_e2ai[n,nn]) ""
;

$GROUP atest_g_ID_alwaysexo
sigma[n]$(ID_kno_inp[n]) ""
mu[n,nn]$(ID_mu_exo[n,nn]) ""
eta[n]$(ID_kno_out[n]) ""
phi[z,n]$(ai[n]) ""
pM[z] ""
PwT[n]$(ID_inp[n]) ""
qS[n]$(ID_out[n]) ""
;

$GROUP atest_g_ID_endoincalib
mu[n,nn]$(ID_mu_endoincalib[n,nn]) ""
;

$GROUP atest_g_minobj_endoincalib_exoinbaseline
gamma_tau[n,nn]$(ID_e2t[n,nn]) ""
;

@load_level(atest_g_ID_alwaysendo,%qmark%%ID_0%");
@load_level(atest_g_ID_exoincalib,%qmark%%ID_0%");
@load_fixed(atest_g_ID_alwaysexo,%qmark%%ID_0%");
@load_fixed(atest_g_ID_endoincalib,%qmark%%ID_0%");
@load_fixed(atest_g_minobj_endoincalib_exoinbaseline,%qmark%%ID_0%");
