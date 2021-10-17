from openpyxl import Workbook
# Modules
from assets.utils import printInfoBlock, clearConsole, getMasterPath, getMasterSheet
from assets.database import typicals

clearConsole()

filePath = getMasterPath()

master_ws = getMasterSheet(filePath)

# User Input: Filter parameters
processingUserInput = True
printInfoBlock('Set filter conditions:', 'yellow')
while processingUserInput:
  print('')
  # PID
  pid = input('P&ID: ')
  pid = int(pid)
  # TYPICAL
  typicalNotFound = True
  while typicalNotFound:
    typical = input('Typical: ')
    # Find the right Filtering Function
    if typical in typicals:
      typicalFilterFunction = typicals[typical]
      break
    else:
      clearConsole()
      print('\033[93m*\033[0m Couldn\'t find this typical in the typicals list. Try searching again:\n')
      print('P&ID: '+str(pid))
  print('')

  # Call filtering function and get processed list
  entries = typicalFilterFunction(pid, master_ws)

  # Info and restart user input if no entries returned
  if(entries == None):
    clearConsole()
    printInfoBlock('Found 0 entries.', 'red')
    print('\nOne of following could be the reason:')
    print('\033[93m*\033[0m No entries found with given PID: '+str(pid))
    print('\033[93m*\033[0m No entries found falling into the given typical: '+typical)
    printInfoBlock('You can try again:', 'yellow')
  else:
    break
  
# Print Result Infos
printInfoBlock('Found '+str(len(entries) - 1)+' entries.', 'cyan')
printInfoBlock('First: '+entries[1][0]+' ... Last: '+entries[-1][0], 'cyan')

# User Confirmation
confirmation = input('\n\nProcess and populate new Excel-File? [\033[92m y\033[0m | \033[91mn\033[0m ]: ')
if(confirmation != 'y' and confirmation != 'yes' and confirmation != ''):
  clearConsole()
  exit()

# Instanciate destination workbook & sheet
print('Creating new Excel-Workbook and importing Data ...')
wb = Workbook()
ws = wb.active
ws.title = str(pid)+'-Data'

# Populate new workbook/sheet
for row in entries:
  ws.append(row)

# Save new file in 'output' folder
try:
  wb.save('./script/output/'+str(pid)+'-processed.xlsx')
  clearConsole()
  printInfoBlock('File saved in "output" folder.', 'green')
  print('')
except:
  clearConsole()
  print('Something went wrong while saving the file. Make sure the file you are writing to \033[93mis closed\033[0m.\n')
  exit()