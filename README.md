## HMI Data Merge

More in depth technical guide and infos can be found in the config.xlsx "info" sheet.

***

This Script will take the <span style='color: #65c1c2; font-weight: 600'>Master Instrument Index File</span>, and filter the data based on the user input: <span style='color: #65c1c2; font-weight: 600'>P&ID</span> and <span style='color: #65c1c2; font-weight: 600'>Typicals</span>.
For each given Typical the data will be processed and saved controlled by the corresponding Typical Filter Logic.
Output will then be stored on the desktop as new Excel File with two Sheets for each filtered typical (Control- & Full Sheet).
The rows in the Full-Sheets can then replace the rows in the ProcessLibraryConfigTool.xls File.

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