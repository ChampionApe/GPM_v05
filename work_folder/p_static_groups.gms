$GROUP p_static_g_tech_endo
mu[s,n,nn]$((map_all[s,n,nn] and not exo_mu[s,n,nn])) ""
markup[s,n]$(out[s,n]) ""
;

$GROUP p_static_g_tech_exo
sigma[s,n]$(kno_inp[s,n]) ""
eta[s,n]$(kno_out[s,n]) ""
mu[s,n,nn]$(exo_mu[s,n,nn]) ""
;

$GROUP p_static_g_endovars
PwT[s,n]$(int[s,n]) ""
qD[s,n]$(int[s,n]) ""
PbT[s,n]$(endo_PbT[s,n]) ""
;

$GROUP p_static_g_calib_exo
qD[s,n]$(inp[s,n]) ""
PbT[s,n]$((out[s,n] and not endo_PbT[s,n])) ""
Peq[n]$(n_out[n]) ""
;

$GROUP p_static_g_tech
p_static_g_tech_endo
p_static_g_tech_exo
;

$GROUP p_static_g_exovars
PwT[s,n]$(inp[s,n]) ""
qS[s,n]$(out[s,n]) ""
tauS[s,n]$(out[s,n]) ""
tauLump[s]$(s_prod[s]) ""
;

@load_level(p_static_g_endovars,%qmark%%p_0%");
@load_level(p_static_g_calib_exo,%qmark%%p_0%");
@load_fixed(p_static_g_tech_endo,%qmark%%p_0%");
@load_fixed(p_static_g_tech_exo,%qmark%%p_0%");
@load_fixed(p_static_g_tech,%qmark%%p_0%");
@load_fixed(p_static_g_exovars,%qmark%%p_0%");
