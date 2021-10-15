import tkinter, time
from tkinter.filedialog import askopenfilename
from openpyxl import Workbook, load_workbook
# Modules
from assets.utils import printInfoBlock, clearConsole
from assets.database import safetyAreas


# Clear tkinter frame & clear Console
root = tkinter.Tk()
root.withdraw()
clearConsole()

# Ask user for Master File-Path
print('[ ] Select Master-File in dialog')
time.sleep(.8)
filePath = askopenfilename(filetypes=[( 'Excel File', '.xlsx .xls')])
root.destroy()
if(filePath == ''): exit()
clearConsole()
print('[\033[92mx\033[0m] Select Master-File in dialog')
time.sleep(2)

# Load Master-Workbook & Target-Sheet
try:
  print("--- Loading Excel Data from "+"\033[92m.../"+filePath.split('/')[-2]+'/'+filePath.split('/')[-1]+"\033[0m")
  master_wb = load_workbook(filePath)
except:
  clearConsole()
  print('Something went wrong while loading the Master-File. Make sure you \033[93mclose the file\033[0m before running the script.\n')
  exit()
master_ws = master_wb.active

# User Input: Filtering and Row Parameters
clearConsole()
printInfoBlock('Set filter conditions:', 'green')
pid = input("\nP&ID: ")
firstRow = 8    # hardcoded
pidRow = 3      # hardcoded
print('')
pid = int(pid)

# Loop through Sheet-Rows and save in list
entries = []
for key, *values in master_ws.iter_rows(min_row = firstRow):
  if(key.value == None):
    break
  if(values[pidRow-2].value == pid):
    entries.append([v.value for v in values])

# Print Result Infos
printInfoBlock('Found '+str(len(entries))+' entries.', 'cyan')
printInfoBlock('First: '+entries[0][4]+str(entries[0][5])+' ... Last: '+entries[-1][4]+str(entries[-1][5]), 'cyan')

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
wb.save('./script/output/'+str(pid)+'-Processed.xlsx')
clearConsole()
printInfoBlock('File saved in "output" folder.', 'green')
print('')