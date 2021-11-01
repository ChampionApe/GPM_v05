$GROUP A3_g_ID_alwaysendo
PwThat[n]$((ID_int[n] or ID_inp[n])) ""
PbT[n]$(ID_out[n]) ""
pMhat[z] ""
qD[n]$(((ID_int[n] or ID_inp[n]) and not (kno_ID_EC[n] or ID_nonbaseC[n]))) ""
os[n,nn]$((ID_e2t[n,nn] and kno_ID_TU[nn])) ""
M0[z] ""
s_uc[n,nn]$((map_ID_CU[n,nn] and bra_ID_TU[n])) ""
share[n,nn]$(ID_map_all[n,nn]) ""
;

$GROUP A3_g_ID_exoincalib
qD[n]$((ai[n] or kno_ID_EC[n] or ID_nonbaseC[n])) ""
qsumX[n,nn]$(ID_e2ai[n,nn]) ""
;

$GROUP A3_g_ID_currapp
currapp[n,nn]$((ID_e2t[n,nn] and kno_ID_TU[nn])) ""
currapp_mod[n,nn]$((ID_e2t[n,nn] and kno_ID_TU[nn])) ""
;

$GROUP A3_g_EOP_alwaysendo
PwThat[n]$((EOP_int[n] or EOP_inp[n])) ""
PbT[n]$(EOP_out[n]) ""
qD[n]$((EOP_int[n] or EOP_inp[n])) ""
qS[n]$(EOP_out[n]) ""
M[z] ""
share[n,nn]$(EOP_map_all[n,nn]) ""
;

$GROUP A3_g_EOP_currapp
currapp_EOP[z,n]$(m2t[z,n]) ""
;

$GROUP A3_g_ID_alwaysexo
sigma[n]$(ID_kno_inp[n]) ""
eta[n]$(ID_kno_out[n]) ""
phi[z,n]$(ai[n]) ""
pM[z] ""
PwT[n]$((ID_inp[n] and not ID_electricity_set[n])) ""
qS[n]$(ID_out[n]) ""
epsi ""
;

$GROUP A3_g_ID_gamma_tau
gamma_tau[n,nn]$((ID_e2t[n,nn] and kno_ID_TU[nn])) ""
;

$GROUP A3_g_ID_mu_exo
mu[n,nn]$(ID_mu_exo[n,nn]) ""
;

$GROUP A3_g_ID_mu_endoincalib
mu[n,nn]$(ID_mu_endoincalib[n,nn]) ""
;

$GROUP A3_g_electricity_endo_ID
PwT[n]$(ID_electricity_set[n]) ""
;

$GROUP A3_g_EOP_alwaysexo
sigma[n]$(EOP_kno_inp[n]) ""
mu[n,nn]$(EOP_map_all[n,nn]) ""
eta[n]$(EOP_kno_out[n]) ""
theta[z,n]$(m2c[z,n]) ""
PwT[n]$((EOP_inp[n] and not EOP_electricity_set[n])) ""
;

$GROUP A3_g_EOP_endoincalib
muG[n]$(kno_EOP_CU[n]) ""
sigmaG[n]$(kno_EOP_CU[n]) ""
;

$GROUP A3_g_electricity_endo_EOP
PwT[n]$(EOP_electricity_set[n]) ""
;

@load_level(A3_g_ID_alwaysendo,%qmark%%ID_0%");
@load_level(A3_g_ID_exoincalib,%qmark%%ID_0%");
@load_level(A3_g_ID_currapp,%qmark%%ID_0%");
@load_level(A3_g_EOP_alwaysendo,%qmark%%ID_0%");
@load_level(A3_g_EOP_currapp,%qmark%%ID_0%");
@load_fixed(A3_g_ID_alwaysexo,%qmark%%ID_0%");
@load_fixed(A3_g_ID_gamma_tau,%qmark%%ID_0%");
@load_fixed(A3_g_ID_mu_exo,%qmark%%ID_0%");
@load_fixed(A3_g_ID_mu_endoincalib,%qmark%%ID_0%");
@load_fixed(A3_g_electricity_endo_ID,%qmark%%ID_0%");
@load_fixed(A3_g_EOP_alwaysexo,%qmark%%ID_0%");
@load_fixed(A3_g_EOP_endoincalib,%qmark%%ID_0%");
@load_fixed(A3_g_electricity_endo_EOP,%qmark%%ID_0%");
