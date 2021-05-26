$GROUP A1_g_tech_endo
mu[n,nn]$((map_all[n,nn] and not exo_mu[n,nn])) ""
markup[n]$(out[n]) ""
;

$GROUP A1_g_tech_exo
sigma[n]$(kno_inp[n]) ""
eta[n]$(kno_out[n]) ""
mu[n,nn]$(exo_mu[n,nn]) ""
;

$GROUP A1_g_endovars
PwT[n]$(int[n]) ""
qD[n]$(int[n]) ""
PbT[n]$(endo_PbT[n]) ""
;

$GROUP A1_g_calib_exo
qD[n]$(inp[n]) ""
PbT[n]$((out[n] and not endo_PbT[n])) ""
Peq[n]$(n_out[n]) ""
;

$GROUP A1_g_tech
A1_g_tech_endo
A1_g_tech_exo
;

$GROUP A1_g_exovars
PwT[n]$(inp[n]) ""
qS[n]$(out[n]) ""
tauS[n]$(out[n]) ""
tauLump ""
;

@load_level(A1_g_endovars,%qmark%%A1_0%");
@load_level(A1_g_calib_exo,%qmark%%A1_0%");
@load_fixed(A1_g_tech_endo,%qmark%%A1_0%");
@load_fixed(A1_g_tech_exo,%qmark%%A1_0%");
@load_fixed(A1_g_tech,%qmark%%A1_0%");
@load_fixed(A1_g_exovars,%qmark%%A1_0%");
