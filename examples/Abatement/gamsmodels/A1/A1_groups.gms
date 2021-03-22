$GROUP A1_g_tech_endo
mu[n,nn]$((map_all[n,nn] and not exo_mu[n,nn])) "mu[n,nn]"
markup[n]$(out[n]) "markup[n]"
;

$GROUP A1_g_tech_exo
sigma[n]$(kno_inp[n]) "sigma[n]"
eta[n]$(kno_out[n]) "eta[n]"
mu[n,nn]$(exo_mu[n,nn]) "mu[n,nn]"
;

$GROUP A1_g_endovars
PwT[n]$(int[n]) "PwT[n]"
qD[n]$(int[n]) "qD[n]"
PbT[n]$(endo_PbT[n]) "PbT[n]"
;

$GROUP A1_g_calib_exo
qD[n]$(inp[n]) "qD[n]"
PbT[n]$((out[n] and not endo_PbT[n])) "PbT[n]"
Peq[n]$(n_out[n]) "Peq[n]"
;

$GROUP A1_g_tech
A1_g_tech_endo
A1_g_tech_exo
;

$GROUP A1_g_exovars
PwT[n]$(inp[n]) "PwT[n]"
tauS[n]$(out[n]) "tauS[n]"
qS[n]$(out[n]) "qS[n]"
;

@load_level(A1_g_calib_exo,%qmark%%A1%");
@load_level(A1_g_endovars,%qmark%%A1%");
@load_fixed(A1_g_tech_exo,%qmark%%A1%");
@load_fixed(A1_g_tech,%qmark%%A1%");
@load_fixed(A1_g_exovars,%qmark%%A1%");
@load_fixed(A1_g_tech_endo,%qmark%%A1%");
