$GROUP atest_g_ID_alwaysendo
PwThat[n]$(ID_int[n]) ""
PbT[n]$(ID_out[n]) ""
qD[n]$((ID_int[n] or ID_inp[n])) ""
;

$GROUP atest_TEST
minobj ""
;

$GROUP atest_g_ID_alwaysexo
sigma[n]$(ID_kno_inp[n]) ""
mu[n,nn]$(ID_mu_exo[n,nn]) ""
eta[n]$(ID_kno_out[n]) ""
PwT[n]$(ID_inp[n]) ""
qS[n]$(ID_out[n]) ""
PwThat[n]$(ID_inp[n]) ""
;

$GROUP atest_g_ID_endoincalib
mu[n,nn]$(ID_mu_endoincalib[n,nn]) ""
;

$GROUP atest_g_minobj_endoincalib_exoinbaseline
gamma_tau[n,nn]$(ID_e2t[n,nn]) ""
;

@load_level(atest_g_ID_alwaysendo,%qmark%%ID_0%");
@load_level(atest_TEST,%qmark%%ID_0%");
@load_fixed(atest_g_ID_alwaysexo,%qmark%%ID_0%");
@load_fixed(atest_g_ID_endoincalib,%qmark%%ID_0%");
@load_fixed(atest_g_minobj_endoincalib_exoinbaseline,%qmark%%ID_0%");
