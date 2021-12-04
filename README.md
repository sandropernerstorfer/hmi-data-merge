## Primetals - Excel Filter/Process/Merge Script
***
This Script will take the <span style='color: #65c1c2; font-weight: 600'>Master Instrument Index File</span>, and filter the data based on the user input: <span style='color: #65c1c2; font-weight: 600'>P&ID</span> and <span style='color: #65c1c2; font-weight: 600'>Typicals</span>.
For each given Typical the data will be processed and saved controlled by the corresponding Typical Filter Logic.
Output will then be stored on the desktop as new Excel File with two Sheets for each filtered typical (Control- & Full Sheet).

The rows in the Full-Sheets can then replace the rows in the ProcessLibraryConfigTool.xls File.
<br>

<span style='color: #492; font-weight: 600'>Filter Logic finished for following Typicals:</span>

* *PT_Intlk*
* *PT_CfgModeChg*
* *PT_CondSel*
* *PT_ForkEH*
* *PT_Perm*
* *PT_Valve_Diag*
* *P_AIChan*
* *P_AIn*
* *P_AInHART*
* *P_DIn*
* *P_E300Ovld*
* *P_Motor*
* *P_PF52x*
* *P_PF755*
* *P_PIDE*
* *P_ResInh*
* *P_RunTime*
* *P_ValveC*
* *P_ValveSO*
* *P_ValveStats*
* *P_VSD*

***
#### File & Directory Info

##### app.zip:
- <span style='color: #79c2c2; font-weight: 600;'>index.exe</span>
  - Executable Application File to run the script

##### config:
- <span style='color: #79c2c2; font-weight: 600;'>PyToolConfig.xlsx</span>
  - Configuration Interface - holds important indexing and filtering parameters
  - Edit with caution. Must be JSON Formatted

##### src/:
- <span style='color: #79c2c2; font-weight: 600;'>main.py</span>
  - Main Program Cycle
<br>

- <span style='color: #79c2c2; font-weight: 600;'>./assets/utils/..</span>
  - Holds Program Cycle Logic and Functions which control the Main Cycle
<br>

- <span style='color: #79c2c2; font-weight: 600;'>./assets/filtering/..</span>
  - Holds Typical Filter-, Merge-, and Helper-Functions

***
#### Usage Info

* Get <span style='color: #79c2c2; font-weight: 600;'>'ProcessLibraryOnlineConfigTool.xls' File</span> (with desired typicals sheet-data) from Remote Machine
<br>

* Start script <span style='color: #79c2c2; font-weight: 600;'>main.py</span> or the <span style='color: #79c2c2; font-weight: 600;'>./app.zip/.exe</span>
  * Select PyToolConfig File in dialog to load config parameters
  * Select Master-Excel in dialog and load entire Instrument Index Data
  * Enter target P&ID - Single P&ID or all(*)
  * Enter target Typicals. Possible to enter multiple:
  by seperating them with a semicolon (typical;typical;typical)
  or selecting all(*)
  * Continue to Merging Process
  * Select ProcessLibraryOnlineConfigTool-File in dialog and load contents
  * For each entered typical, the filtered data with entered P&ID from the Master-Excel will be merged into the ProcessLib. Data contents will be updated and stored into a list
  * This final updated list contains exactly the same row counts as ProcessLib. had before
  * For each entered typical 2 sheets are created in a new excel file that in the end will be saved on your desktop.

<br>

* Now <span style='color: #79c2c2; font-weight: 600;'>overwrite the seperate sheets from the ProcessLib</span> file with the <span style='color: #79c2c2; font-weight: 600;'>corresponding processed-output-file sheets</span>
<br>

* Move <span style='color: #79c2c2; font-weight: 600;'>file back to remote machine</span> and <span style='color: #79c2c2; font-weight: 600;'>load into programm</span>

***