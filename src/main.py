import os
import re
from openpyxl import Workbook
from assets.utils.console import *
from assets.utils.configFile import *
from assets.utils.appUtils import *
from assets.utils.excel import *

# --------------------------------- #
def main():
  
  desktopPath, directoryName = getDesktopPathAndDirname()

  clearConsole()
  
  # Config Data Circle Start | Get Config Data, Parse JSON, Handle Sheet Response
  while True:
    excelPath = getExcelPath('PyToolConfig')
    ws = getExcelSheet(excelPath, 'PyToolConfig', 'PyToolConfig', True)
    if ws == None:
      confirmation = getUserConfirmation('Load Config File again ?')
      clearConsole()
      if confirmation == True: continue
      else: sys.exit()
    
    time.sleep(1.5)

    jsonData = ws['A1'].value
    configData = parseConfigJSON(jsonData)

    if(configData == None):
      printListItem('Config Data could not be parsed.','red')
      printListItem('Make sure the correct Formatting Rules are applied inside the Config Excel (JSON Formatting).','yellow')
      confirmation = getUserConfirmation('Load Config File again ?')
      clearConsole()
      if(confirmation == False):
        sys.exit()
      else:
        continue
    else:
      errors = checkConfigData(configData)
      clearConsole()
      if len(errors) > 0:
        if(errors[0] == 'warnings'):
          errors.pop(0)
          for warning in errors:
            printListItem(warning, 'yellow')

          print('')
          confirmation = getUserConfirmation('Want to continue with warnings ?')
          clearConsole()

          if confirmation == False:
            printListItem('You can adjust the config file to remove the warnings before you load again.', 'cyan')
            print('')
            confirmation = getUserConfirmation('Load Config File again ?')
            clearConsole()
            if confirmation == True: continue
            else: sys.exit()
          else: break
        else:
          print('Make sure you fix the following errors before loading the file again:')
          for error in errors:
            printListItem(error, 'red')

          print('')
          confirmation = getUserConfirmation('Load Config File again ?')
          clearConsole()
          if confirmation == True: continue
          else: sys.exit()
      else: break
  
  areaParameters    = configData['areaParameters']        # Final Config Data
  typicalParameters = configData['typicalParameters']
  indexParameters = configData['indexParameters']
  processLibParameters = configData['processLibParameters']

  # Instrument Index Circle Start | Get Instrument File & Sheet
  while True:
    # Get Instrument Index File Path and load Worksheet
    excelPath = getExcelPath('Instrument Index')
    ws = getExcelSheet(excelPath, 'Instrument Index', 'Index')
    if ws == None:
      confirmation = getUserConfirmation('Load Instrument Index again ?')
      clearConsole()
      if confirmation == True: continue
      else: sys.exit()
    else: break
  
  # Logic Circle Start  |  Take Input-Values, Filter Data, Save Sheet
  while True:
    
    # Input Circle Start
    while True:
      
      # PID-Input Circle Start
      pid = askForPid()

      # Get elements with given PID
      allElements = getAllWithPid(pid, ws, indexParameters['firstRow'], indexParameters['pidColumn'])
      clearConsole()
      if(len(allElements) == 0):
        printPidFilterResult(allElements, pid, 'red')
        printListItem('No Elements with given P&ID found. Try searching again.', 'red')
        continue
      else: printPidFilterResult(allElements, pid, 'green')
      
      # Typical-Input Circle Start | Ask for typicals, search and get filter functions
      filterToolsList = askAndReturnFilterTools() # ----------------------------------------------------------------------------------------------[[Filter,Merge,TypicalName]]

      # Get filtered lists with Typical-Functions and print results
      finalLists = [] # this stores all final filtered lists + typical name
      allFilterWarnings = [] # this stores all warnings that occured in the filter (e.g. unsure range)
      for filterTools in filterToolsList:
        filterResults, warnings = filterTools[0](allElements, typicalParameters[filterTools[2]], areaParameters, indexParameters)     # returns entries, warnings
        printTypicalFilterResults(filterResults, filterTools[2])
        if(len(filterResults) > 0):
          finalLists.append([filterResults, filterTools[1], filterTools[2]])
          if len(warnings) > 1:
            allFilterWarnings.append(warnings)

      # Check if there is at least 1 entry to continue with
      if(len(finalLists) == 0):
        print('')
        printInfoBlock('Found no matching entries', 'red')
        printListItem('None of the entries in P&ID "'+pid+'" are possible candidates for the given typicals.', 'red')
        print('\nYou can try again using different parameters.')
      else: break
    
    # Get user confirmation for continuing with populating new sheet
    print('')
    confirmation = getUserConfirmation('Continue to \033[92mMaster | ProcessLibrary\033[0m merging stage?')
    clearConsole()
    if(confirmation == False):
      confirmation = getUserConfirmation('Start again?')
      clearConsole()
      if(confirmation == True):
        continue
      else:
        exit()

    # Instanciate Output File Object
    wb = Workbook()
    
    # File Input Circle for ProcessLib File
    while True:

      # Get Path of ProcessLib File
      filePath = getExcelPath('ProcessLibraryOnlineConfigTool')

      # Get Excel Data from ProcessLib File
      book = getProcessFileData(filePath, 'ProcessLibraryOnlineConfigTool')
      if(book == None):
        confirmation = getUserConfirmation('Want to search for the ProcessLibraryOnlineConfigTool File again ?')
        if(confirmation == True): continue
        else: exit()
      else: break

    # Loop through all saved typicals with their items
    # list = [[listItems], mergeFunction, typicalName]
    for list in finalLists:
      
      # get xls sheet by typical name
      sheet = book.sheet_by_name(list[2])
      rowCount = sheet.nrows
      # get XLS data
      xlsData = []
      for row in range(rowCount):
        xlsData.append(sheet.row_values(rowx=row))
      
      # Call Merge function for current typical and get final dataset
      mergedOutput, controlOutput = list[1](list[0], xlsData, processLibParameters[list[2]])
      
      if pid == 'all':
        differenceWarnings = returnMergeDifferences(mergedOutput, controlOutput, processLibParameters[list[2]]['key'], 0)     # 0 is index of Full Tag in control sheet - filters normally return full tag at index 0
        
        if len(allFilterWarnings) == 0:
          differenceWarnings.insert(0, '# '+list[2]+' Warnings:')
          allFilterWarnings.append(differenceWarnings)
        else:
          found = False
          for warnings in allFilterWarnings:
            if found: break
            # if list[2] in warnings[0]:
            if re.search(r'\b'+list[2]+r'\b', warnings[0]):
              for warning in differenceWarnings:
                warnings.append(warning)
              found = True
              break
          if found == False and len(differenceWarnings) > 0:
            differenceWarnings.insert(0, '# '+list[2]+' Warnings:')
            allFilterWarnings.append(differenceWarnings)
      
      # Create Sheet on instanciated workbook object with Typical Name
      # Also create sheet with only the imported for checking
      printListItem('Creating '+list[2]+' Sheet and importing Data ...', 'cyan')
      controlSheet = wb.create_sheet(list[2]+'-Imported')
      outputSheet = wb.create_sheet(list[2]+'-Full')

      # Populate Imported checking sheet
      controlSheet.append([' '])
      controlSheet.append(['This is just the control sheet, if you want to check the master imports for '+list[2]+' again.'])
      controlSheet.merge_cells('A1:J1')
      controlSheet.append(['The '+list[2]+'-Full Sheet has to be manually imported into the ProcessLib-File '+list[2]+' Sheet.'])
      controlSheet.merge_cells('A2:J2')
      controlSheet.append([' '])
      
      for row in controlOutput:
        controlSheet.append(row)
        
      # Populate final and full output sheet
      for row in mergedOutput:
        outputSheet.append(row)

    # Save new file in 'output' folder
    try:
      defaultSheet = wb['Sheet']
      wb.remove(defaultSheet)
    except: pass

    try:
      savePath = os.path.join(desktopPath, pid+'-processed.xlsx')
      wb.save(savePath)
      print('')
      printInfoBlock('File for P&ID: '+pid+' saved to \''+directoryName+'\'.', 'green')
      if len(allFilterWarnings) > 0:
        print('')
        printListItem('The following list contains problems that occured with filters being unsure about Instrument Index Data.', 'cyan')
        printListItem('Can be manually adjusted in the saved file, and ideally also in the Instrument Index.', 'cyan')
        printAllFilterWarnings(allFilterWarnings)
        print('\n')
      printListItem('If you want to start again make sure you now manually merge the sheets before you start a new run...', 'cyan')
      printListItem('...so you work with the updated ProcessedLibraryConfigTool Data.', 'cyan')
      print('')
      confirmation = getUserConfirmation('Want to start again ?')
      clearConsole()
      if(confirmation == True): continue
      else: break
    except:
      clearConsole()
      print('Something went wrong while saving the file. Make sure the file you are writing to \033[93mis closed\033[0m.\n')
      exit()

# SP - NS Init   
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    clearConsole()
    sys.exit()