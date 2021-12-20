# GPM_v05
GamsPythonModels, version 0.5. 

A group of Python classes that is especially equipped to work with GAMS in. This includes
- **DataBase classes:** Sets up Python version of GAMS databases (gdx) using Pandas. Includes facilities to subset, write GAMS code from symbols, and aggregate entire databases according to settings.
- **DB2Gams classes:** Classes used for interaction between database and Gams. Includes
  - _gams_settings:_ Defines the basic model structure of a GAMS model (blocks of equations, endogenous variable groups, exogenous groups, solve statements, files with relevant inputs etc.). 
  - _gams_model_py:_ A class that writes .gms files based on the gams_settings file.
  - _gams_model:_ An executable class that is used to interact with GAMS. Includes prespecified ways to solve particularly difficult problems with the 'sneaky_solve' method. 
- **gmspython classes:** Classes that builds on top of the DB2Gams and DataBase classes. This can be used to write and solve entire gams models based on a database and settings. The gmspython classes includes an integration class (gmspython_i) that can be used to combine and integrate various gmspython classes. 
  - Under the folder examples, "Example1.ipynb" shows how these classes are used to build a dynamic general equilibrium model with an arbitrarily nested production structure and an arbitrary number of goods. The model includes methods for calibration to national accounts (input-output data).
