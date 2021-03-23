$GROUP itory_g_endo
qD[t,s,n]$((tx0E[t] and itoryD[s,n])) ""
;

$GROUP itory_g_exo
qD[t,s,n]$((t0[t] and itoryD[s,n])) ""
;

$GROUP itory_itory_exo
ar1_itory ""
;

@load_level(itory_g_endo,%qmark%%GE_data%");
@load_fixed(itory_g_exo,%qmark%%GE_data%");
@load_fixed(itory_itory_exo,%qmark%%GE_data%");
