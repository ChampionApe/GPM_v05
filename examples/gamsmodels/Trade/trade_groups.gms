$GROUP trade_g_endovars
qD[t,s,n]$((sfor_ndom[s,n] and tx0E[t])) "qD[t,s,n]"
;

$GROUP trade_g_tech_endo
phi[s,n]$(sfor_ndom[s,n]) "phi[s,n]"
;

$GROUP trade_g_tech_exo
sigma[s,n]$(sfor_ndom[s,n]) "sigma[s,n]"
;

$GROUP trade_g_exovars
PwT[t,s,n]$(sfor_ndom[s,n]) "PwT[t,s,n]"
Peq[t,n]$(n_for[n]) "Peq[t,n]"
;

$GROUP trade_g_calib_exo
qD[t,s,n]$((sfor_ndom[s,n] and t0[t])) "qD[t,s,n]"
;

$GROUP trade_g_endo_vars
trade_g_endovars
trade_g_calib_exo
;

$GROUP trade_g_tech
trade_g_tech_exo
trade_g_tech_endo
;

$GROUP trade_g_exo_vars
trade_g_exovars
;

@load_level(trade_g_endo_vars,%qmark%%rname%");
@load_fixed(trade_g_calib_exo,%qmark%%rname%");
@load_fixed(trade_g_exovars,%qmark%%rname%");
@load_fixed(trade_g_tech_endo,%qmark%%rname%");
@load_fixed(trade_g_tech,%qmark%%rname%");
@load_fixed(trade_g_tech_exo,%qmark%%rname%");
@load_fixed(trade_g_exo_vars,%qmark%%rname%");
@load_fixed(trade_g_endovars,%qmark%%rname%");
