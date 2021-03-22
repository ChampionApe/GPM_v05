$GROUP itsector_g_endo
qD[t,s,n]$((tx0E[t] and itoryD[s,n])) "qD[t,s,n]"
;

$GROUP itsector_g_exo
qD[t,s,n]$((t0[t] and itoryD[s,n])) "qD[t,s,n]"
;

$GROUP itsector_itory_exo
ar1_itory "ar1_itory"
;

@load_level(itsector_g_endo,%qmark%%rname%");
@load_fixed(itsector_g_exo,%qmark%%rname%");
@load_fixed(itsector_itory_exo,%qmark%%rname%");
