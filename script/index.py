from openpyxl import Workbook
from assets.typicals.__filterUtils import getAllWithPid
from assets.utils import *

# --------------------------------- #
#
# Initial Console Clearing
#
clearConsole()
#
# Get Master File Path and load Worksheet
#
filePath = getExcelPath('Master')
master_ws = getExcelSheet(filePath, 'Master', 'Index')
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
    # Typical-Input Circle Start | Ask for typicals, search and get filter function ------------------------------------------------------------------ TODO Ab hier - änderungen für auswahl mehrerer typicals
    #
    filterFunction = askAndReturnFilterFunction(pid)
    #
    # Get filtered list with Typical-Function
    #
    entries, typical = filterFunction(allElements)
    if(entries == None):
      clearConsole()
      printInfoBlock('Found 0 entries.', 'red')
      print('\nOne of following could be the reason:')
      printListItem('No entries found with given PID: '+pid, 'yellow')
      printListItem('None of the entries fall into the given typical category: '+typical, 'yellow')
      print('\nYou can try again using different parameters.')
    else: break
  #
  # Print filtered list result infos
  #
  printTypicalFilterResults(entries, typical)
  #
  # Get user confirmation for continuing with populating new sheet ----------------------------------------------------------------------------------- TODO Bis hier
  #
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

# filePath = getExcelPath('ProcessLibraryOnlineConfigTool')
# master_ws = getExcelSheet(filePath, 'ProcessLibraryOnlineConfigTool', typical)












# Instanciate destination workbook & sheet
print('Creating new Excel-Workbook and importing Data ...')
wb = Workbook()
ws = wb.active
ws.title = pid+'-Data'

# Populate new workbook/sheet
for row in entries:
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