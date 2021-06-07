$GROUP Abatement_g_prices_alwaysendo
PwThat[n]$(int[n]) ""
PbT[n]$(endo_PbT[n]) ""
;

$GROUP Abatement_g_quants_alwaysendo
qD[n] ""
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

$GROUP Abatement_g_emissions_alwaysendo
M0[n]$(M_subset[n]) ""
M[n]$(M_subset[n]) ""
;

$GROUP Abatement_g_EOP_endogenousC
qS[n]$(EOP_C_subset[n]) ""
;

$GROUP Abatement_g_EOP_alwaysendo
pMhat[n]$(M_subset[n]) ""
PwThat[n]$(inp[n]) ""
;

$GROUP Abatement_g_params_alwaysexo
sigma[n] ""
mu[n,nn]$(params_alwaysexo_mu[n,nn]) ""
eta[n]$(kno_out[n]) ""
;

$GROUP Abatement_g_prices_alwaysexo
tauS[n]$(out[n]) ""
tauLump ""
;

$GROUP Abatement_g_quants_alwaysexo
qS[n] ""
;

$GROUP Abatement_g_params_endoincalib
sigma[n]$(tech_endoincalib_sigma[n]) ""
mu[n,nn]$(tech_endoincalib_mu[n,nn]) ""
markup[n]$(out[n]) ""
;

$GROUP Abatement_g_emissions_alwaysexo
phi[n,nn]$(map_M2X[n,nn]) ""
;

$GROUP Abatement_g_EOP_alwaysexo
pM[n]$(M_subset[n]) ""
PwT[n]$(inp[n]) ""
;

$GROUP Abatement_g_EOP_endoincalib
theta[n]$(EOP_C_subset[n]) ""
muG[n]$(EOP_C_subset[n]) ""
sigmaG[n]$(EOP_C_subset[n]) ""
;

@load_level(Abatement_g_prices_alwaysendo,%qmark%%Abatement_0%");
@load_level(Abatement_g_quants_alwaysendo,%qmark%%Abatement_0%");
@load_level(Abatement_g_prices_exoincalib,%qmark%%Abatement_0%");
@load_level(Abatement_g_quants_exoincalib,%qmark%%Abatement_0%");
@load_level(Abatement_g_emissions_alwaysendo,%qmark%%Abatement_0%");
@load_level(Abatement_g_EOP_endogenousC,%qmark%%Abatement_0%");
@load_level(Abatement_g_EOP_alwaysendo,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_params_alwaysexo,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_prices_alwaysexo,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_quants_alwaysexo,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_params_endoincalib,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_emissions_alwaysexo,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_EOP_alwaysexo,%qmark%%Abatement_0%");
@load_fixed(Abatement_g_EOP_endoincalib,%qmark%%Abatement_0%");
