$FIX p_g_tech, p_g_vars_exo, p_ict_exo, HH_g_tech, HH_g_exo_static, HH_g_calib_endo, inv_g_tech, inv_g_vars_exo, itory_g_exo, itory_itory_exo, trade_g_tech, trade_g_exo_vars, G_g_exo, G_g_calib_endo, G_g_exo_dyn;
$UNFIX p_g_vars_endo, p_ict_endo, HH_g_endo_static, HH_g_endo_dyn, HH_g_calib_exo, inv_g_vars_endo, itory_g_endo, trade_g_endo_vars, G_g_endo, GE_module_ge_t0, GE_module_ge_tx0E;
$Model ex1_B M_lower_nests, M_p_pw, M_p_cf, M_upper_nest, M_HH_dyn, M_bdgt_HH, M_HH_agg, M_inv_pw, M_nest, M_itory, M_trade, M_gov_G, M_GE_module_eqtx0E, M_GE_module_eqt0;
scalars ex1_B_modelstat, ex1_B_solvestat;
solve ex1_B using CNS;
ex1_B_modelstat = ex1_B.modelstat; ex1_B_solvestat = ex1_B.solvestat;
$FIX p_g_tech_exo, p_g_tech_exo_dyn, p_gvars_exo, p_g_calib_exo, p_ict_endo, HH_g_tech_exo, HH_g_exo_static, HH_g_calib_exo, inv_g_tech_exo, inv_gvars_exo, inv_g_calib_exo, itory_g_exo, itory_itory_exo, trade_g_tech_exo, trade_g_exovars, trade_g_calib_exo, G_g_exo, G_g_exo_dyn, GE_module_ge_t0;
$UNFIX p_g_tech_endo, p_gvars_endo, p_ict_endo, HH_g_endo_static, HH_g_endo_dyn, HH_g_tech_endo, HH_g_calib_endo, inv_g_tech_endo, inv_gvars_endo, itory_g_endo, trade_g_endovars, trade_g_tech_endo, G_g_endo, G_g_calib_endo, GE_module_ge_tx0E;
$Model ex1_DC M_lower_nests, M_p_pw, M_p_cf, M_upper_nest, M_HH_dyn, M_bdgt_HH, M_HH_agg, M_inv_pw, M_nest, M_itory, M_trade, M_gov_G, M_gcalib_G, M_GE_module_eqtx0E;
