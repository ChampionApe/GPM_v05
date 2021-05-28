$GROUP Abatement_g_prices_alwaysendo
PwT[n]$(int[n]) ""
PbT[n]$(endo_PbT[n]) ""
;

$GROUP Abatement_g_quants_alwaysendo
qD[n] ""
;

$GROUP Abatement_g_params_endoincalib
sigma[n]$(tech_endoincalib_sigma[n]) ""
mu[n,nn]$(tech_endoincalib_mu[n,nn]) ""
markup[n]$(out[n]) ""
;

$GROUP Abatement_g_minobj_endoincalib
minobj ""
;

$GROUP Abatement_g_params_alwaysexo
sigma[n] ""
mu[n,nn]$(params_alwaysexo_mu[n,nn]) ""
eta[n]$(kno_out[n]) ""
;

$GROUP Abatement_g_prices_alwaysexo
PwT[n]$(inp[n]) ""
tauS[n]$(out[n]) ""
tauLump ""
;

$GROUP Abatement_g_quants_alwaysexo
qS[n]$(out[n]) ""
;

$GROUP Abatement_g_prices_exoincalib
PbT[n]$((out[n] and not endo_PbT[n])) ""
Peq[n]$(n_out[n]) ""
;

$GROUP Abatement_g_quants_exoincalib
qD[n]$(endovars_exoincalib_C[n]) ""
qsumU[n]$(sumUaggs[n]) ""
qsumX[n]$(sumXaggs[n]) ""
;

$GROUP Abatement_g_minobj_exoincalib
weight_mu ""
weight_sigma ""
minobj_sigma[n]$(minobj_sigma_subset[n]) ""
minobj_mu[n,nn]$(minobj_mu_subset[n,nn]) ""
;

@load_level(Abatement_g_prices_alwaysendo,%qmark%%Abatement_0%");
@load_level(Abatement_g_quants_alwaysendo,%qmark%%Abatement_0%");
@load_level(Abatement_g_params_endoincalib,%qmark%%Abatement_0%");
@load_level(Abatement_g_minobj_endoincalib,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_params_alwaysexo,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_prices_alwaysexo,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_quants_alwaysexo,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_prices_exoincalib,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_quants_exoincalib,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_minobj_exoincalib,%qmark%%Abatement_0%");
