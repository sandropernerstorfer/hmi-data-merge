## Pimetals - Excel Filter/Process/Merge Script
***
This Script will take the <span style='color: #65c1c2; font-weight: 600'>Master Instrument File</span>, and filter the data based on the user input: <span style='color: #65c1c2; font-weight: 600'>P&ID</span> and <span style='color: #65c1c2; font-weight: 600'>Typicals</span>.
For each given Typical the data will be processed and saved controlled by the corresponding Typical Filter Logic.
Output will then be stored on the desktop as new Excel File with one new Sheet for each filtered typical.

This data can then replace the rows in the ProcessLibraryConfigTool.xls File, sheet by sheet.
<ul>
  <li>For now, this last step (the ProcessLib. replacement) has to be done manually via copy-paste</li>
  because the excel format of this file is too old for the used tools.
  <li>Update will be provided when a solution is found.</li>
</ul>
<br>

<span style='color: #492; font-weight: 600'>Filter Logic finished for following Typicals:</span>

* *P_AInHART*

<span style='color: #492; font-weight: 600'>Added Locations for Safety Area (default is 'area01'):</span>

* *+H00*
* *+H01*
* *+H04*
* *+H05*
* *+H06*
* *+H07*
* *+H08*
* *+H09*
* *+H10*
* *+H11*
* *+H12*
* *+H14*
* *+H16*
* *+H17*
* *+H19*
* *+H20*
* *+H21*
* *+H22*
* *+H23*
* *+H24*
* *+H25*
* *+H26*


***
#### Development Info

* Script was developed in such a way that variables can be changed in the <span style='color: #79c2c2; font-weight: 600;'>database.py</span> file
  * if for example sheet formats or column positions change
<br>

* For each Typical a new file with fitting name, containing filter logic and merge logic, has to be created
  * located in <span style='color: #79c2c2; font-weight: 600;'>script/assets/filtering/<Typical_Name>.py</span>
<br>

* Runtime and App Cycle is Dynamic and works depending on data in <span style='color: #79c2c2; font-weight: 600;'>database.py</span> and <span style='color: #79c2c2; font-weight: 600;'>new typical scripts</span>

***
#### File & Directory Info

##### application.zip:
- <span style='color: #79c2c2; font-weight: 600;'>index.exe</span>
  - Executable Application to run the script

##### src:
- <span style='color: #79c2c2; font-weight: 600;'>index.py</span>
  - Main Program Cycle
<br>

- <span style='color: #79c2c2; font-weight: 600;'>assets/database.py</span>
  - Holds manually changeable variables that control the proram flow
  - Changing can of course shortcut the script if the variables are not corresponding to the real world situation
<br>

- <span style='color: #79c2c2; font-weight: 600;'>assets/utils.py</span>
  - Holds Program Cycle Logic and Functions which are imported in the Main Cycle
<br>

- <span style='color: #79c2c2; font-weight: 600;'>filtering/__filterUtils.py</span>
  - Holds helper functions and logic regarding typicals sorting and filtering
  - Imported into filter functions that need them
<br>

- <span style='color: #79c2c2; font-weight: 600;'>filtering/<Typical_Name>.py</span>
  - Contains all the sorting and filtering procedure and returns the output list with typical name
  - For each typical another sort & filter process has to be applied, but there may be similarities

***
#### Usage Info

* Get <span style='color: #79c2c2; font-weight: 600;'>'ProcessLibraryOnlineConfigTool.xls' File</span> (with desired typicals sheet-data) from Remote Machine
<br>

* Start script <span style='color: #79c2c2; font-weight: 600;'>index.py</span> or the index.exe in the v*.* folder
  * Select Master-Excel in dialog and load entire Instrument Data
  * Enter target P&ID
  * Enter target Typicals. Possible to enter multiple, by seperating them with a semicolon - typical;typical;typical
  * Continue to Merging Process

  * Select ProcessLibraryOnlineConfigTool-File in dialog and load contents
  * For each entered typical, the filtered data with entered PID from the Master-Excel will be merged into the ProcessLib. Data contents and will be updated and stored into a list
  * This final updated list contains exactly the same row counts as ProcessLib. had before

  * For each entered typical, a sheet named after the typical, is stored into an excel-File. for example (2403-processed.xlsx)
  * This File can be found on the desktop

<br>

* Now <span style='color: #79c2c2; font-weight: 600;'>overwrite the seperate sheets from the ProcessLib</span>. file with the <span style='color: #79c2c2; font-weight: 600;'>corresponding processed-output-file sheets</span>
<br>

* Move <span style='color: #79c2c2; font-weight: 600;'>file back to remote machine</span> and <span style='color: #79c2c2; font-weight: 600;'>load into programm</span>

***