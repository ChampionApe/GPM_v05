$FIX G_V01_NT_exo_always, G_V01_NT_exo_base, G_V01_T_exo_always, G_V01_T_exo_base;
$UNFIX G_V01_NT_endo_always, G_V01_NT_endo_base, G_V01_T_endo_always, G_V01_T_endo_base, G_V01_ACC_endo_base;
$Model V01_B M_V01_NT, M_V01_T_always, M_V01_T_base, M_V01_ACC;
scalars V01_B_modelstat, V01_B_solvestat;
solve V01_B using CNS;
V01_B_modelstat = V01_B.modelstat; V01_B_solvestat = V01_B.solvestat;
