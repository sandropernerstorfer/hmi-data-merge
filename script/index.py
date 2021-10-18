from openpyxl import Workbook
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
    printInfoBlock('Set filter conditions:', 'yellow')
    print('')
    #
    # PID-Input Circle Start
    #
    pid = askForPid()
    #
    # Typical-Input Circle Start | Search and get filter function
    #
    typicalFilterFunction, typical = askAndGetTypicalFunction(pid)
    #
    # Get filtered list with Typical-Function
    #
    entries = getFilteredData(typicalFilterFunction, pid, master_ws)
    if(entries == None):
      clearConsole()
      printInfoBlock('Found 0 entries.', 'red')
      print('\nOne of following could be the reason:')
      print('\033[93m*\033[0m No entries found with given PID: '+pid)
      print('\033[93m*\033[0m None of the entries fall into the given typical category: '+typical)
      print('\nYou can try again using different parameters.')
    else: break
  #
  # Print filtered list result-infos
  #
  printFilterResults(entries)
  #
  # Get user confirmation for continuing with populating new sheet
  #
  confirmation = getUserConfirmation('Process and populate new Excel-File?')
  clearConsole()
  if(confirmation == True): break
  else:
    confirmation = getUserConfirmation('Start again?')
    clearConsole()
    if(confirmation == True):
      continue
    else:
      exit()


# ------------------------------------------------------------------------------------------- TODO Saving Logic #

# filePath = getExcelPath('ProcessLibraryOnlineConfigTool')
# master_ws = getExcelSheet(filePath, 'ProcessLibraryOnlineConfigTool', typical)











exit()
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