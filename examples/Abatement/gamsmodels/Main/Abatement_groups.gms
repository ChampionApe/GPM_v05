$GROUP Abatement_g_ID_prices_alwaysendo
PwThat[n]$((ID_int[n] or ID_inp[n])) ""
PbT[n]$(ID_out[n]) ""
;

$GROUP Abatement_g_ID_quants_alwaysendo
qD[n]$(((ID_int[n] or ID_inp[n]) and not ID_endovars_exoincalib_C[n])) ""
;

$GROUP Abatement_g_emissions_alwaysendo
M0[n]$(M_subset[n]) ""
;

$GROUP Abatement_g_EOP_prices_alwaysendo
PwThat[n]$((EOP_int[n] or EOP_inp[n])) ""
PbT[n]$(EOP_out[n]) ""
;

$GROUP Abatement_g_prices_endogenouswithEOP
pMhat[n]$(M_subset[n]) ""
;

$GROUP Abatement_g_EOP_quants_alwaysendo
qD[n]$(((EOP_int[n] or EOP_inp[n]))) ""
qS[n]$(EOP_out[n]) ""
;

$GROUP Abatement_g_EOP_quants_exoincalib
qsumU[n]$(EOP_sumUaggs[n]) ""
;

$GROUP Abatement_g_emissions_endoinEOP
M[n]$(M_subset[n]) ""
;

$GROUP Abatement_g_ID_quants_exoincalib
qD[n]$(ID_endovars_exoincalib_C[n]) ""
qsumU[n]$(ID_sumUaggs[n]) ""
qsumX[n]$(sumXaggs[n]) ""
;

$GROUP Abatement_g_ID_params_alwaysexo
sigma[n]$((ID_kno_inp[n] and not ID_tech_endoincalib_sigma[n])) ""
mu[n,nn]$(ID_params_alwaysexo_mu[n,nn]) ""
eta[n]$(ID_kno_out[n]) ""
;

$GROUP Abatement_g_ID_prices_alwaysexo
PwT[n]$(ID_inp[n]) ""
;

$GROUP Abatement_g_prices_alwaysexo
pM[n]$(M_subset[n]) ""
;

$GROUP Abatement_g_ID_quants_alwaysexo
qS[n]$((ID_out[n])) ""
;

$GROUP Abatement_g_emissions_alwaysexo
phi[n,nn]$(map_M2X[n,nn]) ""
;

$GROUP Abatement_g_EOP_params_alwaysexo
sigma[n]$(EOP_kno_inp[n]) ""
mu[n,nn]$(EOP_params_alwaysexo_mu[n,nn]) ""
eta[n]$(EOP_kno_out[n]) ""
;

$GROUP Abatement_g_EOP_params_endoincalib
theta[n]$(EOP_out[n]) ""
muG[n]$(EOP_out[n]) ""
sigmaG[n]$(EOP_out[n]) ""
;

$GROUP Abatement_g_EOP_prices_alwaysexo
PwT[n]$(EOP_inp[n]) ""
;

$GROUP Abatement_g_ID_params_endoincalib
sigma[n]$(ID_tech_endoincalib_sigma[n]) ""
mu[n,nn]$(ID_tech_endoincalib_mu[n,nn]) ""
;

@load_level(Abatement_g_ID_prices_alwaysendo,%qmark%%ID_0%");
@load_level(Abatement_g_ID_quants_alwaysendo,%qmark%%ID_0%");
@load_level(Abatement_g_emissions_alwaysendo,%qmark%%ID_0%");
@load_level(Abatement_g_EOP_prices_alwaysendo,%qmark%%ID_0%");
@load_level(Abatement_g_prices_endogenouswithEOP,%qmark%%ID_0%");
@load_level(Abatement_g_EOP_quants_alwaysendo,%qmark%%ID_0%");
@load_level(Abatement_g_EOP_quants_exoincalib,%qmark%%ID_0%");
@load_level(Abatement_g_emissions_endoinEOP,%qmark%%ID_0%");
@load_level(Abatement_g_ID_quants_exoincalib,%qmark%%ID_0%");
@load_fixed(Abatement_g_ID_params_alwaysexo,%qmark%%ID_0%");
@load_fixed(Abatement_g_ID_prices_alwaysexo,%qmark%%ID_0%");
@load_fixed(Abatement_g_prices_alwaysexo,%qmark%%ID_0%");
@load_fixed(Abatement_g_ID_quants_alwaysexo,%qmark%%ID_0%");
@load_fixed(Abatement_g_emissions_alwaysexo,%qmark%%ID_0%");
@load_fixed(Abatement_g_EOP_params_alwaysexo,%qmark%%ID_0%");
@load_fixed(Abatement_g_EOP_params_endoincalib,%qmark%%ID_0%");
@load_fixed(Abatement_g_EOP_prices_alwaysexo,%qmark%%ID_0%");
@load_fixed(Abatement_g_ID_params_endoincalib,%qmark%%ID_0%");
