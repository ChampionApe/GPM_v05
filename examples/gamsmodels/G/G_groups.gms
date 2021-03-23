$GROUP G_g_endo
TotTaxRev[t] ""
PwT[t,s,n]$(d_tauD[s,n]) ""
vD[t,s,n]$((gsvngs[n] and s_G[s] and tx0[t])) ""
g_tvc[s,n]$((gsvngs[n] and s_G[s])) ""
;

$GROUP G_g_calib_endo
tauD[t,s,n]$((tauDendo[s,n] and t0[t])) ""
;

$GROUP G_g_exo
qD[t,s,n]$(d_tauD[s,n]) ""
qS[t,s,n]$(d_tauS[s,n]) ""
vD[t,s,n]$((s_tax[s] and n_tax[n])) ""
tauS[t,s,n]$(d_tauS[s,n]) ""
tauLump[t,s]$(d_tauLump[s]) ""
PbT[t,s,n]$(d_tauS[s,n]) ""
Peq[t,n]$(d_Peq[n]) ""
tauD[t,s,n]$((d_tauD[s,n] and (tx0E[t] or (t0[t] and not tauDendo[s,n])))) ""
;

$GROUP G_g_exo_dyn
irate[t] ""
vD[t,s,n]$((gsvngs[n] and s_G[s] and t0[t])) ""
;

@load_level(G_g_endo,%qmark%%GE_data_0%");
@load_fixed(G_g_calib_endo,%qmark%%GE_data_0%");
@load_fixed(G_g_exo,%qmark%%GE_data_0%");
@load_fixed(G_g_exo_dyn,%qmark%%GE_data_0%");
