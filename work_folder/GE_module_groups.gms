$GROUP GE_module_ge_t0
qS[t,s,n]$((qS_endo[s,n] and t0[t])) ""
Peq[t,n]$((Peq_endo[n] and t0[t])) ""
;

$GROUP GE_module_ge_tx0E
qS[t,s,n]$((qS_endo[s,n] and tx0E[t])) ""
Peq[t,n]$((Peq_endo[n] and tx0E[t])) ""
;

@load_level(GE_module_ge_t0,%qmark%%rname%");
@load_level(GE_module_ge_tx0E,%qmark%%rname%");
