$FIX G_V01_NT_endo_base, G_V01_NT_exo_always, G_V01_T_endo_base, G_V01_T_exo_always, G_V01_ACC_endo_base;
$UNFIX G_V01_NT_endo_always, G_V01_NT_exo_base, G_V01_T_endo_always, G_V01_T_exo_base;
$Model V01_CalibAll M_V01_NT, M_V01_T_always, M_V01_ACC;
scalars V01_CalibAll_modelstat, V01_CalibAll_solvestat;
solve V01_CalibAll using CNS;
V01_CalibAll_modelstat = V01_CalibAll.modelstat; V01_CalibAll_solvestat = V01_CalibAll.solvestat;
