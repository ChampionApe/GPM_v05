$FIX p_static_g_tech, p_static_g_exovars;
$UNFIX p_static_g_endovars, p_static_g_calib_exo;
$Model p_static_B M_upper_nest, M_p_static_pw, M_lower_nests;
scalars p_static_B_modelstat, p_static_B_solvestat;
solve p_static_B using CNS;
p_static_B_modelstat = p_static_B.modelstat; p_static_B_solvestat = p_static_B.solvestat;
