$GROUP G_GE_electricity_endo
	PwT[n]$(elec_set[n])
;

$GROUP G_GE_electricity_exo
	ge_scale
	ge_elast
;

$BLOCK B_GE_electricity 
	E_GE_electricity[n]$(elec_set[n])..	PwT[n] =E= ge_scale*(sum(nn$(ai2i[nn,n]), qD[nn]))**(ge_elast);
$ENDBLOCK