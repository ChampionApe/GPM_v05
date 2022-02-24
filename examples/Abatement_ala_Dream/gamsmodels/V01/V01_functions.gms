$FUNCTION load_level({group}, {gdx}):
  $offlisting
  $GROUP __load_group {group};
  $LOOP __load_group:
    parameter load_{name}{sets} "";
    load_{name}{sets}$({conditions}) = 0;
  $ENDLOOP
  execute_load {gdx} $LOOP __load_group: load_{name}={name}.l $ENDLOOP;
  $LOOP __load_group:
    {name}.l{sets}$({conditions}) = load_{name}{sets};
  $ENDLOOP
  $onlisting
$ENDFUNCTION

$FUNCTION load_fixed({group}, {gdx}):
  $offlisting
  $GROUP __load_group {group};
  $LOOP __load_group:
    parameter load_{name}{sets} "";
    load_{name}{sets}$({conditions}) = 0;
  $ENDLOOP
  execute_load {gdx} $LOOP __load_group: load_{name}={name}.l $ENDLOOP;
  $LOOP __load_group:
    {name}.fx{sets}$({conditions}) = load_{name}{sets};
  $ENDLOOP
  $onlisting
$ENDFUNCTION

$FUNCTION TechLogit({p},{lambda},{sigma},{mu},{map}): sum(nn$({map}), (1/(1+exp(({p}-{mu}-{lambda})/{sigma})))) $ENDFUNCTION
$FUNCTION TechNormal({p},{lambda},{sigma},{mu},{map}): sum(nn$({map}),errorf(({lambda}-{p}+{mu})/{sigma})) $ENDFUNCTION
$FUNCTION TechLognormal({p},{lambda},{sigma},{mu},{map}): sum(nn$({map}), errorf((log({lambda})-log({p})+Sqr({sigma})/2+{mu})/{sigma})) $ENDFUNCTION

$FUNCTION SolveEmptyNLP({name})
variable randomnameobj;  
randomnameobj.L = 0;

EQUATION E_EmptyNLPObj;
E_EmptyNLPObj..    randomnameobj  =E=  0;

Model M_SolveEmptyNLP /
E_EmptyNLPObj, {name}
/;
solve M_SolveEmptyNLP using NLP min randomnameobj;
$ENDFUNCTION