$FIX G_V01_NT_endo_always, G_V01_NT_endo_base, G_V01_NT_exo_always, G_V01_NT_exo_base, G_V01_T_endo_base, G_V01_T_exo_always, G_V01_ACC_endo_base;
$UNFIX G_V01_T_endo_always, G_V01_T_exo_base;
$Model V01_CalibTech M_V01_T_always;
scalars V01_CalibTech_modelstat, V01_CalibTech_solvestat;
solve V01_CalibTech using CNS;
V01_CalibTech_modelstat = V01_CalibTech.modelstat; V01_CalibTech_solvestat = V01_CalibTech.solvestat;