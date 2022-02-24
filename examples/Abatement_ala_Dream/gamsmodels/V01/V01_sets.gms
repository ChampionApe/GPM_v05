sets
	alias_set
	alias_map2
	s
	n
;

alias(n,nn,nnn);

sets
	alias_[alias_set,alias_map2]
	V01_NT_map[s,n,nn]
	V01_NT_inp[s,n]
	V01_NT_out[s,n]
	V01_NT_int[s,n]
	V01_NT_bra_out[s,n]
	V01_NT_bra_nout[s,n]
	V01_inp[s,n]
	V01_NT_x[s,n]
	V01_x2inp[s,n,nn]
	V01_dur[s,n]
	V01_ES[s,n]
	V01_T[s,n]
	V01_inp2T[s,n,nn]
	V01_T2ES[s,n,nn]
	V01_T2ESNorm[s,n,nn]
	V01_map[s,n,nn]
;

$GDXIN %V01_DB%
$onMulti
$load alias_set
$load alias_map2
$load s
$load n
$load alias_
$load V01_NT_map
$load V01_NT_inp
$load V01_NT_out
$load V01_NT_int
$load V01_NT_bra_out
$load V01_NT_bra_nout
$load V01_inp
$load V01_NT_x
$load V01_x2inp
$load V01_dur
$load V01_ES
$load V01_T
$load V01_inp2T
$load V01_T2ES
$load V01_T2ESNorm
$load V01_map
$GDXIN
$offMulti
