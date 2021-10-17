import tkinter, time, sys
from tkinter.filedialog import askopenfilename
from openpyxl import Workbook, load_workbook
# Modules
from assets.utils import printInfoBlock, clearConsole, CURSOR_UP_ONE, ERASE_LINE
from assets.database import typicals

# Clear tkinter frame & clear Console
root = tkinter.Tk()
root.withdraw()
clearConsole()

# Ask user for Master File-Path
print('[ ] Select master file in dialog')
time.sleep(.8)
filePath = askopenfilename(filetypes = [( 'Excel File', '.xlsx .xls')])
root.destroy()
clearConsole()
if(filePath == ''):
  exit()
print('[\033[92mx\033[0m] Select master file in dialog')
time.sleep(2)

# Load Master-Workbook & Target-Sheet
try:
  print(" |\n[ ] Loading data from "+"\033[92m.../"+filePath.split('/')[-2]+'/'+filePath.split('/')[-1]+"\033[0m")
  master_wb = load_workbook(filePath)
  sys.stdout.write(CURSOR_UP_ONE) 
  sys.stdout.write(ERASE_LINE) 
  print("[\033[92mx\033[0m] Loading data from "+"\033[92m.../"+filePath.split('/')[-2]+'/'+filePath.split('/')[-1]+"\033[0m\n")
except:
  clearConsole()
  print('Something went wrong while loading the master file. Make sure you \033[93mclose the file\033[0m before running the script.\n')
  exit()
master_ws = master_wb.active

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