from openpyxl import Workbook
from assets.utils import *

# --------------------------------- #

clearConsole()
filePath = getMasterPath()
master_ws = getMasterSheet(filePath)

while True:       # Creating Output Dataset
  while True:     # Processing User Input
    printInfoBlock('Set filter conditions:', 'yellow')
    print('')
    
    while True:   # Processing PID
      pid = askForPid().strip()
      if(pid != None and pid != ''): break
      else:
        eraseLastLine()
      
    while True:   # Processing Typical
      typical = askForTypical().strip()
      if(typical == None or typical == ''):
        eraseLastLine()
        continue
      
      typicalFilterFunction = getFilterFunction(typical)
      if(typicalFilterFunction != None):
        break
      else:
        clearConsole()
        print('\033[93m*\033[0m Couldn\'t find "'+typical+'" in the typicals list. Try searching again.\n')
        print('P&ID: '+pid)

    try: convertedPid = int(pid)
    except: convertedPid = pid
    entries = typicalFilterFunction(convertedPid, master_ws)
    if(entries == None):
      clearConsole()
      printInfoBlock('Found 0 entries.', 'red')
      print('\nOne of following could be the reason:')
      print('\033[93m*\033[0m No entries found with given PID: '+pid)
      print('\033[93m*\033[0m No entries found falling into the given typical: '+typical)
      print('\nYou can try again using different parameters.')
    else: break
  
  printFilterResults(entries)

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