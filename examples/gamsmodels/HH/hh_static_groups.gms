$GROUP hh_static_g_tech_endo
mu[s,n,nn]$(endo_mu[s,n]) "mu[s,n,nn]"
;

$GROUP hh_static_g_tech_exo
sigma[s,n]$(kno_HH_agg[s,n]) "sigma[s,n]"
mu[s,n,nn]$((map_all_HH_agg[s,n,nn] and not endo_mu[s,n])) "mu[s,n,nn]"
;

$GROUP hh_static_g_endovars
PwT[s,n]$((int_HH_agg[s,n] and not top_HH_agg[s,n])) "PwT[s,n]"
PbT[s,n]$(out_HH_agg[s,n]) "PbT[s,n]"
qD[s,n]$(int_HH_agg[s,n]) "qD[s,n]"
;

$GROUP hh_static_g_savings
sp[s]$(s_HH[s]) "sp[s]"
;

$GROUP hh_static_g_exovars
PwT[s,n]$(inp_HH_agg[s,n]) "PwT[s,n]"
Peq[n]$(fg_HH[n]) "Peq[n]"
qD[s,n]$((inp_HH_agg[s,n] and exo_HH_agg[s,n])) "qD[s,n]"
qS[s,n]$((out_HH_agg[s,n] and exo_HH_agg[s,n])) "qS[s,n]"
tauS[s,n]$(out_HH_agg[s,n]) "tauS[s,n]"
tauLump[s]$(s_HH[s]) "tauLump[s]"
;

$GROUP hh_static_g_calib_exo
qD[s,n]$((inp_HH_agg[s,n] and not exo_HH_agg[s,n])) "qD[s,n]"
qS[s,n]$((out_HH_agg[s,n] and not exo_HH_agg[s,n])) "qS[s,n]"
PwT[s,n]$(top_HH_agg[s,n]) "PwT[s,n]"
;

$GROUP hh_static_g_tech
hh_static_g_tech_exo
hh_static_g_tech_endo
;

@load_level(hh_static_g_endovars,%qmark%%HH_agg_0%");
@load_level(hh_static_g_calib_exo,%qmark%%HH_agg_0%");
@load_fixed(hh_static_g_tech_exo,%qmark%%HH_agg_0%");
@load_fixed(hh_static_g_tech_endo,%qmark%%HH_agg_0%");
@load_fixed(hh_static_g_exovars,%qmark%%HH_agg_0%");
@load_fixed(hh_static_g_tech,%qmark%%HH_agg_0%");
@load_fixed(hh_static_g_savings,%qmark%%HH_agg_0%");
