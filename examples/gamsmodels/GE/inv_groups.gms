$GROUP inv_g_tech_exo
sigma[s,n]$(GE_kno_inp[s,n]) "sigma[s,n]"
eta[s,n]$(GE_kno_out[s,n]) "eta[s,n]"
mu[s,n,nn]$(GE_exo_mu[s,n,nn]) "mu[s,n,nn]"
;

$GROUP inv_g_tech_endo
mu[s,n,nn]$((GE_map_all[s,n,nn] and not GE_exo_mu[s,n,nn])) "mu[s,n,nn]"
markup[s,n]$(GE_out[s,n]) "markup[s,n]"
;

$GROUP inv_gvars_exo
qS[t,s,n]$(GE_out[s,n]) "qS[t,s,n]"
PwT[t,s,n]$(GE_inp[s,n]) "PwT[t,s,n]"
tauS[t,s,n]$(GE_out[s,n]) "tauS[t,s,n]"
tauLump[t,s]$(s_inv[s]) "tauLump[t,s]"
;

$GROUP inv_gvars_endo
PbT[t,s,n]$(GE_endo_PbT[s,n]) "PbT[t,s,n]"
PwT[t,s,n]$(GE_int[s,n]) "PwT[t,s,n]"
qD[t,s,n]$((GE_wT[s,n] and tx0[t])) "qD[t,s,n]"
Peq[t,n]$((GE_n_out[n] and tx0E[t])) "Peq[t,n]"
;

$GROUP inv_g_calib_exo
qD[t,s,n]$((GE_inp[s,n] and t0[t])) "qD[t,s,n]"
PbT[t,s,n]$((t0[t] and GE_out[s,n] and not GE_endo_PbT[s,n])) "PbT[t,s,n]"
Peq[t,n]$((t0[t] and GE_n_out[n])) "Peq[t,n]"
;

$GROUP inv_g_vars_endo
inv_gvars_endo
inv_g_calib_exo
;

$GROUP inv_g_tech
inv_g_tech_exo
inv_g_tech_endo
;

$GROUP inv_g_vars_exo
inv_gvars_exo
;

@load_level(inv_g_vars_endo,%qmark%%inv_1%");
@load_fixed(inv_g_tech_exo,%qmark%%inv_1%");
@load_fixed(inv_g_tech_endo,%qmark%%inv_1%");
@load_fixed(inv_gvars_exo,%qmark%%inv_1%");
@load_fixed(inv_gvars_endo,%qmark%%inv_1%");
@load_fixed(inv_g_calib_exo,%qmark%%inv_1%");
@load_fixed(inv_g_tech,%qmark%%inv_1%");
@load_fixed(inv_g_vars_exo,%qmark%%inv_1%");
