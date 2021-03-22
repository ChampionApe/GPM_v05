$GROUP g_static_g_endo
TotTaxRev "TotTaxRev"
PwT[s,n]$(d_tauD[s,n]) "PwT[s,n]"
;

$GROUP g_static_g_exo
qD[s,n]$(d_tauD[s,n]) "qD[s,n]"
qS[s,n]$(d_tauS[s,n]) "qS[s,n]"
vD[s,n]$((s_tax[s] and n_tax[n])) "vD[s,n]"
tauD[s,n]$((d_tauD[s,n] and not tauDendo[s,n])) "tauD[s,n]"
tauS[s,n]$(d_tauS[s,n]) "tauS[s,n]"
tauLump[s]$(d_tauLump[s]) "tauLump[s]"
PbT[s,n]$(d_tauS[s,n]) "PbT[s,n]"
Peq[n]$(d_Peq[n]) "Peq[n]"
;

$GROUP g_static_g_calib_endo
tauD[s,n]$(tauDendo[s,n]) "tauD[s,n]"
;

@load_level(g_static_g_endo,%qmark%%GE_data_5%");
@load_level(g_static_g_calib_endo,%qmark%%GE_data_5%");
@load_fixed(g_static_g_exo,%qmark%%GE_data_5%");
