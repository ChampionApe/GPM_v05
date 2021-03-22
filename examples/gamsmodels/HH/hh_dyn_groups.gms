$GROUP hh_dyn_g_endo_static
PwT[t,s,n]$(int_HH_agg[s,n]) "PwT[t,s,n]"
PbT[t,s,n]$(out_HH_agg[s,n]) "PbT[t,s,n]"
qD[t,s,n]$((int_HH_agg[s,n] or (inp_HH_agg[s,n] and not exo_HH_agg[s,n] and tx0E[t]))) "qD[t,s,n]"
qS[t,s,n]$((out_HH_agg[s,n] and not exo_HH_agg[s,n] and tx0E[t])) "qS[t,s,n]"
;

$GROUP hh_dyn_g_endo_dyn
PwT[t,s,n]$((top_HH_agg[s,n] and tx0E[t])) "PwT[t,s,n]"
vD[t,s,n]$((svngs[n] and s_HH[s] and tx0[t])) "vD[t,s,n]"
sp[t,s]$(s_HH[s]) "sp[t,s]"
;

$GROUP hh_dyn_g_tech_endo
mu[s,n,nn]$(endo_mu[s,n]) "mu[s,n,nn]"
;

$GROUP hh_dyn_g_calib_endo
vD[t,s,n]$((svngs[n] and s_HH[s] and t0[t])) "vD[t,s,n]"
;

$GROUP hh_dyn_g_tech_exo
sigma[s,n]$(kno_HH_agg[s,n]) "sigma[s,n]"
mu[s,n,nn]$((map_all_HH_agg[s,n,nn] and not endo_mu[s,n])) "mu[s,n,nn]"
irate[t] "irate[t]"
disc[s]$(s_HH[s]) "disc[s]"
crra[s,n]$(int_temp_HH_agg[s,n]) "crra[s,n]"
hh_tvc[s,n]$((svngs[n] and s_HH[s])) "hh_tvc[s,n]"
;

$GROUP hh_dyn_g_exo_static
PwT[t,s,n]$(inp_HH_agg[s,n]) "PwT[t,s,n]"
Peq[t,n]$(fg_HH[n]) "Peq[t,n]"
qD[t,s,n]$((inp_HH_agg[s,n] and exo_HH_agg[s,n])) "qD[t,s,n]"
qS[t,s,n]$((out_HH_agg[s,n] and exo_HH_agg[s,n])) "qS[t,s,n]"
tauLump[t,s]$(s_HH[s]) "tauLump[t,s]"
tauS[t,s,n]$(out_HH_agg[s,n]) "tauS[t,s,n]"
;

$GROUP hh_dyn_g_calib_exo
qD[t,s,n]$((inp_HH_agg[s,n] and t0[t] and not exo_HH_agg[s,n])) "qD[t,s,n]"
qS[t,s,n]$((out_HH_agg[s,n] and t0[t] and not exo_HH_agg[s,n])) "qS[t,s,n]"
;

$GROUP hh_dyn_g_tech
hh_dyn_g_tech_exo
hh_dyn_g_tech_endo
;

@load_level(hh_dyn_g_endo_static,%qmark%%HH_agg_1%");
@load_level(hh_dyn_g_calib_exo,%qmark%%HH_agg_1%");
@load_level(hh_dyn_g_endo_dyn,%qmark%%HH_agg_1%");
@load_fixed(hh_dyn_g_exo_static,%qmark%%HH_agg_1%");
@load_fixed(hh_dyn_g_tech_endo,%qmark%%HH_agg_1%");
@load_fixed(hh_dyn_g_calib_endo,%qmark%%HH_agg_1%");
@load_fixed(hh_dyn_g_tech,%qmark%%HH_agg_1%");
@load_fixed(hh_dyn_g_tech_exo,%qmark%%HH_agg_1%");
