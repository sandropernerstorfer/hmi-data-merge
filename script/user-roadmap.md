
* Get 'ProcessLibraryOnlineConfigTool.xls' File
  (with desired typicals sheet-data) from Remote Machine

* Start script -> index.py

  * Select Master-Excel in dialog and load entire Instrument Data
  * Enter target P&ID
  * Enter target Typicals. Possible to enter multiple, by seperating them with a semicolon - typical;typical;typical
  * Continue to Merging Process

  * Select ProcessLibraryOnlineConfigTool-File in dialog and load contents
  * For each entered typical, the filtered data with entered PID from the Master-Excel will be merged into the ProcessLib. Data contents and will be updated and stored into a list
  * This final updated list contains exactly the same row counts as ProcessLib. had before

  * For each entered typical, a sheet named after the typical, is stored into an excel-File. for example (2403-processed.xlsx)
  * This File can be found in the 'Outputs folder'


* Now overwrite the seperate sheets from the ProcessLib. file with the corresponding processed-output-file sheets

* Move file to remote machine and load into programm