$GROUP inv_g_tech_endo
mu[s,n,nn]$((I_map_all[s,n,nn] and not I_exo_mu[s,n,nn])) ""
markup[s,n]$(I_out[s,n]) ""
;

$GROUP inv_gvars_endo
PbT[t,s,n]$(I_endo_PbT[s,n]) ""
PwT[t,s,n]$(I_int[s,n]) ""
qD[t,s,n]$((I_wT[s,n] and tx0[t])) ""
Peq[t,n]$((I_n_out[n] and tx0E[t])) ""
;

$GROUP inv_g_tech_exo
sigma[s,n]$(I_kno_inp[s,n]) ""
eta[s,n]$(I_kno_out[s,n]) ""
mu[s,n,nn]$(I_exo_mu[s,n,nn]) ""
;

$GROUP inv_gvars_exo
qS[t,s,n]$(I_out[s,n]) ""
PwT[t,s,n]$(I_inp[s,n]) ""
tauS[t,s,n]$(I_out[s,n]) ""
tauLump[t,s]$(s_inv[s]) ""
;

$GROUP inv_g_calib_exo
qD[t,s,n]$((I_inp[s,n] and t0[t])) ""
PbT[t,s,n]$((t0[t] and I_out[s,n] and not I_endo_PbT[s,n])) ""
Peq[t,n]$((t0[t] and I_n_out[n])) ""
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

@load_level(inv_g_vars_endo,%qmark%%inv_2%");
@load_fixed(inv_g_tech_endo,%qmark%%inv_2%");
@load_fixed(inv_gvars_endo,%qmark%%inv_2%");
@load_fixed(inv_g_tech_exo,%qmark%%inv_2%");
@load_fixed(inv_gvars_exo,%qmark%%inv_2%");
@load_fixed(inv_g_calib_exo,%qmark%%inv_2%");
@load_fixed(inv_g_tech,%qmark%%inv_2%");
@load_fixed(inv_g_vars_exo,%qmark%%inv_2%");
