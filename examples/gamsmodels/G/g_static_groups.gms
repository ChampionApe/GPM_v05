$GROUP g_static_g_endo
TotTaxRev ""
PwT[s,n]$(d_tauD[s,n]) ""
;

$GROUP g_static_g_exo
qD[s,n]$(d_tauD[s,n]) ""
qS[s,n]$(d_tauS[s,n]) ""
vD[s,n]$((s_tax[s] and n_tax[n])) ""
tauD[s,n]$((d_tauD[s,n] and not tauDendo[s,n])) ""
tauS[s,n]$(d_tauS[s,n]) ""
tauLump[s]$(d_tauLump[s]) ""
PbT[s,n]$(d_tauS[s,n]) ""
Peq[n]$(d_Peq[n]) ""
;

$GROUP g_static_g_calib_endo
tauD[s,n]$(tauDendo[s,n]) ""
;

@load_level(g_static_g_endo,%qmark%%GE_data%");
@load_level(g_static_g_calib_endo,%qmark%%GE_data%");
@load_fixed(g_static_g_exo,%qmark%%GE_data%");
