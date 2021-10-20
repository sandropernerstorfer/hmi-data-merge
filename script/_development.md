----------------------------------------------------------------------------------------------------------------

* Script was developed in such a way that variables can be changed in the 'database.py' file
  * if for example sheet formats or column positions change

* For each Typical a new file with fitting name, containing filter logic and merge logic, has to be created
  * located in script/assets/filtering/... (for example P_AInHART.py)

* Runtime and App Cycle is Dynamic and reacts to data change in database.py and new typical scripts

----------------------------------------------------------------------------------------------------------------

- index.py
  Main Program Cycle

- assets/database.py
  Holds manually changeable variables that control the proram flow
  Changing can of course shortcut the script if the variables are not corresponding to the real world situation

- assets/utils.py
  Holds Program Cycle Logic and Functions which are imported in the Main Cycle

- filtering/__filterUtils.py
  Holds helper functions and logic regarding typicals sorting and filtering
  Imported into filter functions that need them

- filtering/<typical_Name>.py
  Contains all the sorting and filtering procedure and returns the output list with typical name
  For each typical another sort & filter process has to be applied, but there may be similarities

- output/
  Output Excel files will be stores in this directory

----------------------------------------------------------------------------------------------------------------