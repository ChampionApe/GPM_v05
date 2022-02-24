# Non-Technology groups:
$GROUP G_V01_NT_endo_always
	pS[s,n]$(V01_NT_out[s,n])	"cost price index for outputs"
	pD[s,n]$(V01_NT_int[s,n])	"cost price index for intermediates"
	qD[s,n]$(V01_NT_x[s,n])		"demand for pure inputs outside Tech"
;

$GROUP G_V01_NT_endo_base
	qD[s,n]$(V01_NT_int[s,n])						"demand quantities"
	qD[s,n]$(V01_NT_inp[s,n] and not V01_NT_x[s,n])	"demand quantities"
;
$GROUP G_V01_NT_exo_always
	sigma[s,n]$(V01_NT_int[s,n])	"price elasticities"
	sigma[s,n]$(V01_NT_out[s,n])	"price elasticities"
	pD[s,n]$(V01_inp[s,n])			"price on inputs"
	qS[s,n]$(V01_NT_out[s,n])		"output"
;
$GROUP G_V01_NT_exo_base
	mu[s,n,nn]$(V01_NT_map[s,n,nn])	"share parameters"
;

# Technology groups
$GROUP G_V01_T_endo_always
	lambda[s,n]$(V01_ES[s,n])	"shadow cost of energy services"
	pD[s,n]$(V01_ES[s,n])		"price index of energy services"
;

$GROUP G_V01_T_endo_base
	qD[s,n]$(V01_T[s,n])		"technology shares"
	pD[s,n]$(V01_T[s,n])		"price index of technologies"
;

$GROUP G_V01_T_exo_always
	theta[s,n]$(V01_T[s,n])								"technology potential"
	mu[s,n,nn]$(V01_inp2T[s,n,nn] and not V01_dur[s,n]) "input intensities on non-durables"
	sigma[s,n]$(V01_ES[s,n])							"measure of heterogeneity in costs"
	mu[s,n,nn]$(V01_T2ESNorm[s,n,nn])					"Normalized element in shadow cost parameters."
;

$GROUP G_V01_T_exo_base
	mu[s,n,nn]$(V01_T2ES[s,n,nn] and not V01_T2ESNorm[s,n,nn])	"shadow cost parameters"
	mu[s,n,nn]$(V01_inp2T[s,n,nn] and V01_dur[s,n])				"input intensity of durables"
;


# Accounting groups:
$GROUP G_V01_ACC_endo_base
	qD[s,n]$(V01_inp[s,n])	
;