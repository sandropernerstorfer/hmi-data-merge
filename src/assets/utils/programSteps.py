import os
import re
from assets.utils.console import *
from assets.utils.configFile import *
from assets.utils.appUtils import *
from assets.utils.excel import *



def initialActions():
  clearConsole()
  dp = path.expanduser("~/Desktop")
  return dp

def getConfigSheet():
  path = getExcelPath('PyToolConfig')
  ws = getExcelSheet(path, 'PyToolConfig', 'PyToolConfig', True)
  if ws == None:
    confirmation = getUserConfirmation('Load Config File again ?')
    clearConsole()
    if confirmation == True: return getConfigSheet()
    else: sys.exit()
  else:
    time.sleep(1.5)
    return ws

def getConfigData(sheet):
  json = sheet['A1'].value
  data = parseConfigJSON(json)
  if data == None:
    printListItem('Config Data could not be parsed.','red')
    printListItem('Make sure the correct Formatting Rules are applied inside the Config Excel (JSON Formatting).','yellow')
    confirmation = getUserConfirmation('Load Config File again ?')
    clearConsole()
    if confirmation == True: return 'load again'
    else: sys.exit()
  else: return data

def getConfigErrors(data):
  errors = checkConfigData(data)
  clearConsole()
  return errors

def handleConfigWarnings(warnings):
  warnings.pop(0)
  for warning in warnings:
    printListItem(warning, 'yellow')

  print('')
  confirmation = getUserConfirmation('Want to continue with warnings ?')
  clearConsole()

  if confirmation == False:
    printListItem('You can adjust the config file to remove the warnings before you load again.', 'cyan')
    print('')
    confirmation = getUserConfirmation('Load Config File again ?')
    clearConsole()
    if confirmation == True: return 'load again'
    else: sys.exit()
  else: return True

def handleConfigErrors(errors):
  print('Make sure you fix the following errors before loading the file again:')
  for error in errors:
    printListItem(error, 'red')
  print('')
  confirmation = getUserConfirmation('Load Config File again ?')
  clearConsole()
  if confirmation == True: return 'load again'
  else: sys.exit()

def getInstrumentIndexSheet():
  path = getExcelPath('Instrument Index')
  ws = getExcelSheet(path, 'Instrument Index', 'Index')
  if ws == None:
    confirmation = getUserConfirmation('Load Instrument Index again ?')
    clearConsole()
    if confirmation == True: return getInstrumentIndexSheet()
    else: sys.exit()
  else: return ws

def getPidAndIndexElements(sheet, indexParameters):
  pid = askForPid() # str
  allElements = getAllWithPid(pid, sheet, indexParameters['firstRow'], indexParameters['pidColumn']) # list
  clearConsole()
  if len(allElements) == 0:
    printPidFilterResult(allElements, pid, 'red')
    printListItem('No Elements with given P&ID found. Try searching again.', 'red')
    print('')
    return 'load again', None
  else: return pid, allElements

def getFinalLists(allElements, typicalParams, areaParams, indexParams):
  filterToolsList = askAndReturnFilterTools() # list[[Filter,Merge,TypicalName],...]
  finalLists = [] # this stores all final filtered lists + typical name
  allFilterWarnings = [] # this stores all warnings that occured in the filter (e.g. unsure range)
  for filterTools in filterToolsList:
    filterResults, warnings = filterTools[0](allElements, typicalParams[filterTools[2]], areaParams, indexParams) # returns entries, warnings
    printTypicalFilterResults(filterResults, filterTools[2])
    if(len(filterResults) > 0):
      finalLists.append([filterResults, filterTools[1], filterTools[2]])
      if len(warnings) > 1:
        allFilterWarnings.append(warnings)
  if len(finalLists) == 0: # check if there is at least 1 entry to continue with
        print('')
        printInfoBlock('Found no matching entries', 'red')
        print('')
        printListItem('None of the entries in given P&ID are possible candidates for the given typicals.', 'red')
        printListItem('You can try again using different parameters.', 'cyan')
        print('')
        return 'try again', None
  else: return finalLists, allFilterWarnings

def getMergeContinuationConfirmation():
  print('')
  confirmation = getUserConfirmation('Continue to \033[92mMaster | ProcessLibrary\033[0m merging stage?')
  clearConsole()
  if confirmation == False:
    confirmation = getUserConfirmation('Start again?')
    clearConsole()
    if confirmation == False: sys.exit()

def getProcessLibWorkbook():
    path = getExcelPath('ProcessLibraryOnlineConfigTool')
    wb = getProcessFileData(path, 'ProcessLibraryOnlineConfigTool')
    if wb == None:
      confirmation = getUserConfirmation('Want to search for the ProcessLibraryOnlineConfigTool File again ?')
      clearConsole()
      if confirmation == True: return getProcessLibWorkbook()
      else: sys.exit()
    else: return wb

def getProcessLibTypicalSheet(wb, typicalName):
  sheet = wb.sheet_by_name(typicalName)
  return sheet, sheet.nrows

def getProcessLibSheetData(sheet, rowCount):
  x = []
  for row in range(rowCount):
    x.append(sheet.row_values(rowx=row))
  return x

def callMergeFunction(mergeFunc, indexData, procLibData, procLibParams, typicalName):
  mergedOutput, controlOutput = mergeFunc(indexData, procLibData, procLibParams)
  if len(mergedOutput) > 0 and mergedOutput[0] == 'sortError':
      mergedOutput.pop(0)
      printListItem('-------- '+typicalName+' Sheet may be unsorted due to missing Origin-Instance Values in ProcessLib File.', 'yellow')
  return mergedOutput, controlOutput

def mergeCollectedWarnings(warnings_1: list, warnings_2: list, typicalName):
  if len(warnings_1) == 0:
    warnings_2.insert(0, '# '+typicalName+' Warnings:')
    warnings_1.append(warnings_2)
  else:
    found = False
    for warnings in warnings_1:
      if found: break
      if re.search(r'\b'+typicalName+r'\b', warnings[0]):
        for warning in warnings_2:
          warnings.append(warning)
        found = True
        break
    if found == False and len(warnings_2) > 0:
      warnings_2.insert(0, '# '+typicalName+' Warnings:')
      warnings_1.append(warnings_2)
  return warnings_1

def removeDefaultSheet(wb):
  try:
    wb.remove(wb['Sheet'])
  finally:
    return wb

def saveOutputFile(wb, path, pid):
  try:
    savePath = os.path.join(path, pid+'-processed.xlsx')
    wb.save(savePath)
    print('')
    printInfoBlock('File for P&ID: '+pid+' saved to \''+path+'\'.', 'green')
  except:
    clearConsole()
    print('Something went wrong while saving the file. Make sure the file you are writing to \033[93mis closed\033[0m.\n')
    sys.exit()

def handleFilterWarnings(warnings):
  if len(warnings) > 0:
    print('')
    printListItem('The following list contains problems that occured with filters being unsure about Instrument Index Data.', 'cyan')
    printListItem('Can be manually adjusted in the saved file, and ideally also in the Instrument Index.', 'cyan')
    minOneWarning = printAllFilterWarnings(warnings)
    if minOneWarning == False: 
      print('')
      printListItem('No warnings', 'green')
    print('\n')
  printListItem('If you want to start again make sure you now manually merge the sheets before you start a new run...', 'cyan')
  printListItem('...so you work with the updated ProcessedLibraryConfigTool Data.', 'cyan')
  print('')
  