$GROUP HH_g_endo_static
PwT[t,s,n]$(int_HH[s,n]) ""
PbT[t,s,n]$(out_HH[s,n]) ""
qD[t,s,n]$((int_HH[s,n] or (inp_HH[s,n] and not exo_HH[s,n] and tx0E[t]))) ""
qS[t,s,n]$((out_HH[s,n] and not exo_HH[s,n] and tx0E[t])) ""
;

$GROUP HH_g_endo_dyn
PwT[t,s,n]$((top_HH[s,n] and tx0E[t])) ""
vD[t,s,n]$((svngs[n] and s_HH[s] and tx0[t])) ""
sp[t,s]$(s_HH[s]) ""
;

$GROUP HH_g_tech_endo
mu[s,n,nn]$(endo_mu[s,n]) ""
;

$GROUP HH_g_calib_endo
vD[t,s,n]$((svngs[n] and s_HH[s] and t0[t])) ""
;

$GROUP HH_g_tech_exo
sigma[s,n]$(kno_HH[s,n]) ""
mu[s,n,nn]$((map_all_HH[s,n,nn] and not endo_mu[s,n])) ""
irate[t] ""
disc[s]$(s_HH[s]) ""
crra[s,n]$(int_temp_HH[s,n]) ""
hh_tvc[s,n]$((svngs[n] and s_HH[s])) ""
;

$GROUP HH_g_exo_static
PwT[t,s,n]$(inp_HH[s,n]) ""
Peq[t,n]$(fg_HH[n]) ""
qD[t,s,n]$((inp_HH[s,n] and exo_HH[s,n])) ""
qS[t,s,n]$((out_HH[s,n] and exo_HH[s,n])) ""
tauLump[t,s]$(s_HH[s]) ""
tauS[t,s,n]$(out_HH[s,n]) ""
;

$GROUP HH_g_calib_exo
qD[t,s,n]$((inp_HH[s,n] and t0[t] and not exo_HH[s,n])) ""
qS[t,s,n]$((out_HH[s,n] and t0[t] and not exo_HH[s,n])) ""
;

$GROUP HH_g_tech
HH_g_tech_exo
HH_g_tech_endo
;

@load_level(HH_g_endo_static,%qmark%%HH_1%");
@load_level(HH_g_endo_dyn,%qmark%%HH_1%");
@load_level(HH_g_calib_exo,%qmark%%HH_1%");
@load_fixed(HH_g_tech_endo,%qmark%%HH_1%");
@load_fixed(HH_g_calib_endo,%qmark%%HH_1%");
@load_fixed(HH_g_tech_exo,%qmark%%HH_1%");
@load_fixed(HH_g_exo_static,%qmark%%HH_1%");
@load_fixed(HH_g_tech,%qmark%%HH_1%");
