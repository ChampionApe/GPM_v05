$FIX A1_g_tech, A1_g_exovars;
$UNFIX A1_g_endovars, A1_g_calib_exo;
$Model A1_B M_E, M_T_inp, M_T_out, M_A1_pw, M_C;
scalars A1_B_modelstat, A1_B_solvestat;
solve A1_B using CNS;
A1_B_modelstat = A1_B.modelstat; A1_B_solvestat = A1_B.solvestat;
