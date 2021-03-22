$GROUP g_dynamic_g_endo
TotTaxRev[t] "TotTaxRev[t]"
tauS[t,s,n]$(d_tauS[s,n]) "tauS[t,s,n]"
PwT[t,s,n]$(d_tauD[s,n]) "PwT[t,s,n]"
vD[t,s,n]$((gsvngs[n] and s_G[s] and tx0[t])) "vD[t,s,n]"
;

$GROUP g_dynamic_g_calib_endo
tauD[t,s,n]$((tauDendo[s,n] and t0[t])) "tauD[t,s,n]"
;

$GROUP g_dynamic_g_exo
qD[t,s,n]$(d_tauD[s,n]) "qD[t,s,n]"
qS[t,s,n]$(d_tauS[s,n]) "qS[t,s,n]"
vD[t,s,n]$((s_tax[s] and n_tax[n])) "vD[t,s,n]"
tauSflat[t,s,n]$(d_tauS[s,n]) "tauSflat[t,s,n]"
tauLump[t,s]$(d_tauLump[s]) "tauLump[t,s]"
PbT[t,s,n]$(d_tauS[s,n]) "PbT[t,s,n]"
Peq[t,n]$(d_Peq[n]) "Peq[t,n]"
tauD[t,s,n]$((d_tauD[s,n] and (tx0E[t] or (t0[t] and not tauDendo[s,n])))) "tauD[t,s,n]"
;

$GROUP g_dynamic_g_exo_dyn
irate[t] "irate[t]"
g_tvc[s,n]$((gsvngs[n] and s_G[s])) "g_tvc[s,n]"
;

@load_level(g_dynamic_g_endo,%qmark%%GE_data%");
@load_fixed(g_dynamic_g_exo_dyn,%qmark%%GE_data%");
@load_fixed(g_dynamic_g_exo,%qmark%%GE_data%");
@load_fixed(g_dynamic_g_calib_endo,%qmark%%GE_data%");
