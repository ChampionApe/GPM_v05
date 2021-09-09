$GROUP A1_test_g_ID_alwaysendo
PwThat[n]$((ID_int[n] or ID_inp[n])) ""
PbT[n]$(ID_out[n]) ""
pMhat[z] ""
qD[n]$(((ID_int[n] or ID_inp[n]) and not (kno_ID_EC[n] or kno_ID_CU[n]))) ""
os[n,nn]$(ID_e2t[n,nn]) ""
M0[z] ""
s_uc[n,nn]$((map_ID_CU[n,nn] and bra_ID_TU[n])) ""
;

@load_fixed(A1_test_g_ID_alwaysendo,%qmark%%ID_0%");
