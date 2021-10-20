from openpyxl import Workbook
from assets.filtering.__filterUtils import getAllWithPid
from assets.utils import *
from assets.database import sheetName

# --------------------------------- #
#
# Initial Console Clearing
#
clearConsole()
#
# Get Master File Path and load Worksheet
#
filePath = getExcelPath('Master')
master_ws = getExcelSheet(filePath, 'Master', sheetName)
#
# Logic Circle Start  |  Take Input-Values, Filter Data, Save Sheet
#
while True:
  #
  # Input Circle Start
  #
  while True:
    #
    # PID-Input Circle Start
    #
    pid = askForPid()
    #
    # Get elements with given PID
    #
    allElements = getAllWithPid(pid, master_ws)
    clearConsole()
    if(len(allElements) == 0):
      printPidFilterResult(allElements, pid, 'red')
      printListItem('No Elements with given PID found. Try searching again.', 'red')
      continue
    else: printPidFilterResult(allElements, pid, 'green')
    #
    # Typical-Input Circle Start | Ask for typicals, search and get filter functions
    #
    filterToolsList = askAndReturnFilterTools()
    #
    # Get filtered lists with Typical-Functions and print results
    #
    finalLists = [] # this stores all final filtered lists + typical name
    for filterTools in filterToolsList:
      filterResults = filterTools[0](allElements, filterTools[1])     # returns [entries, typical name]
      printTypicalFilterResults(filterResults[0], filterResults[1])
      if(len(filterResults) > 0):
        finalLists.append(filterResults)
    #
    # Check if there is at least 1 entry to continue with
    #
    if(len(finalLists) == 0):
      printInfoBlock('Found no entries.', 'red')
      print('\nOne of following could be the reason:')
      printListItem('No entries found with given PID: '+pid, 'yellow')
      printListItem('None of the entries fall into the given typicals categories.', 'yellow')
      print('\nYou can try again using different parameters.')
    else: break
  
  #
  # Get user confirmation for continuing with populating new sheet
  #
  print('')
  confirmation = getUserConfirmation('Continue to \033[92mMaster | ProcessLibrary\033[0m merging stage?')
  clearConsole()
  if(confirmation == True): break
  else:
    confirmation = getUserConfirmation('Start again?')
    clearConsole()
    if(confirmation == True):
      continue
    else:
      exit()


# ------------------------------------------------------------------------------------------- TODO Merge and Save Logic #
# print(finalLists[0][0])   # List
# print(finalLists[0][1])   # Typical

#
# Instanciate Output File Object
#
wb = Workbook()
#
# File Input Circle for ProcessLib File
#
while True:
  #
  # Get Path of ProcessLib File
  #
  filePath = getProcessPath('ProcessLibraryOnlineConfigTool')
  if(filePath == False): continue
  #
  # Get Excel Data from ProcessLib File
  #
  book = getProcessFileData(filePath, 'ProcessLibraryOnlineConfigTool')
  if(book == None):
    confirmation = getUserConfirmation('Want to search for the ProcessLibraryOnlineConfigTool File again ?')
    if(confirmation == True): continue
    else: exit()
  else: break


for list in finalLists: #--------- list = [listItems, TypicalName]
  
  #---------------- get xls sheet by typical name
  sheet = book.sheet_by_name(list[1])
  rowCount = sheet.nrows
  #------------------------------------------------
  #----------------- get XLS data
  xlsData = []
  for row in range(sheet.nrows):
    xlsData.append(sheet.row_values(rowx=row))
  #------------------------------------------------
  
  # Loop through filtered rows
  # on each iteration compare fullTags
  # if match -> populate field
  # -- row = filtered excel row
  # INDEX ist hardcoded für P_AInHART atm
  # ([fullTag, label, desc, area, minRange, maxRange, unit])
  doneList = []
  for xrow in xlsData:
    for row in list[0]:
      if(row[0] == xrow[2]):
        xrow[4] = row[2]
        xrow[5] = row[1]
        xrow[6] = row[0]
        xrow[7] = row[3]
        xrow[8] = row[6]
        xrow[10] = row[4]
        xrow[11] = row[5]
        break
    doneList.append(xrow)

  for i in range (8):
    doneList.pop(0)
  doneList = sorted(doneList, key=lambda x: x[3])
  # Instanciate destination workbook & sheet
  print('Creating '+list[1]+'-Sheet and importing Data ...')
  # wb = Workbook()
  ws = wb.create_sheet(list[1])

  # Populate new workbook/sheet
  for row in doneList:
    ws.append(row)

# Save new file in 'output' folder
try:
  wb.save('./script/output/'+pid+'-processed.xlsx')
  clearConsole()
  printInfoBlock('File saved in "output" folder.', 'green')
  print('')
except:
  clearConsole()
  print('Something went wrong while saving the file. Make sure the file you are writing to \033[93mis closed\033[0m.\n')
  exit()