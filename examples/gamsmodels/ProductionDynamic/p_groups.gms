$GROUP p_g_tech_endo
mu[s,n,nn]$((map_all[s,n,nn] and not exo_mu[s,n,nn])) ""
markup[s,n]$(out[s,n]) ""
;

$GROUP p_gvars_endo
PbT[t,s,n]$(endo_PbT[s,n]) ""
PwT[t,s,n]$(int[s,n]) ""
qD[t,s,n]$(((wT[s,n] and tx0[t]) or (int[s,n] and t0[t] and not dur[n]))) ""
Peq[t,n]$((n_out[n] and tx0E[t])) ""
;

$GROUP p_ict_endo
ic[t,s,n]$(out[s,n]) ""
os[t,s,n]$(out[s,n]) ""
;

$GROUP p_g_tech_exo
sigma[s,n]$(kno_inp[s,n]) ""
eta[s,n]$(kno_out[s,n]) ""
mu[s,n,nn]$(exo_mu[s,n,nn]) ""
;

$GROUP p_g_tech_exo_dyn
rDepr[t,s,n]$(dur[n]) ""
Rrate[t] ""
;

$GROUP p_gvars_exo
qS[t,s,n]$(out[s,n]) ""
PwT[t,s,n]$(inp[s,n]) ""
qD[t,s,n]$((dur[n] and t0[t])) ""
tauS[t,s,n]$(out[s,n]) ""
tauLump[t,s]$(s_prod[s]) ""
;

$GROUP p_g_calib_exo
qD[t,s,n]$((inp[s,n] and t0[t])) ""
PbT[t,s,n]$((t0[t] and out[s,n] and not endo_PbT[s,n])) ""
Peq[t,n]$((t0[t] and n_out[n])) ""
;

$GROUP p_g_vars_endo
p_gvars_endo
p_g_calib_exo
;

$GROUP p_g_tech
p_g_tech_exo
p_g_tech_exo_dyn
p_g_tech_endo
;

$GROUP p_g_vars_exo
p_gvars_exo
;

$GROUP p_ict_exo
ic_1[s,n]$(dur[n]) ""
ic_2[s,n]$(dur[n]) ""
ic_tvc[s,n]$(dur[n]) ""
;

@load_level(p_g_vars_endo,%qmark%%p_1%");
@load_level(p_ict_endo,%qmark%%p_1%");
@load_fixed(p_g_tech_endo,%qmark%%p_1%");
@load_fixed(p_gvars_endo,%qmark%%p_1%");
@load_fixed(p_g_tech_exo,%qmark%%p_1%");
@load_fixed(p_g_tech_exo_dyn,%qmark%%p_1%");
@load_fixed(p_gvars_exo,%qmark%%p_1%");
@load_fixed(p_g_calib_exo,%qmark%%p_1%");
@load_fixed(p_g_tech,%qmark%%p_1%");
@load_fixed(p_g_vars_exo,%qmark%%p_1%");
@load_fixed(p_ict_exo,%qmark%%p_1%");
