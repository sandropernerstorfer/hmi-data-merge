import os, tkinter, time
from tkinter.filedialog import askopenfilename
from openpyxl import Workbook, load_workbook
# Modules
from assets.utils import printInfoBlock
from assets.database import safetyAreas


# Clear tkinter frame
root = tkinter.Tk()
root.withdraw()

# Ask user for Master File-Path
print('Select Master-File in dialog ...')
time.sleep(.8)
filePath = askopenfilename(filetypes=[( 'Excel File', '.xlsx .xls')])
root.destroy()
if(filePath == ''): exit()
os.system('cls||clear')

# Hard-Coded Variables for Master File - can be dynamic later
firstRow = 8
pidRow = 3

# Load Master-Workbook & Target-Sheet
print("Loading Excel Data from "+"\033[92m.../"+filePath.split('/')[-2]+'/'+filePath.split('/')[-1]+"\033[0m")
master_wb = load_workbook(filePath)
master_ws = master_wb.active

# User Input - Filtering Parameters
os.system('cls||clear')
printInfoBlock('Fill out parameters to filter:', 'yellow')
pid = input("\nP&ID: ")
print('')
pid = int(pid)

# List for Output
entries = []

# Loop through Sheet-Rows
for key, *values in master_ws.iter_rows(min_row = firstRow):
  if(key.value == None):
    break
  if(values[pidRow-2].value == pid):
    entries.append([v.value for v in values])

# Print Result Infos
printInfoBlock('Found '+str(len(entries))+' entries.', 'cyan')
printInfoBlock('First: '+entries[0][4]+str(entries[0][5])+' ... Last: '+entries[-1][4]+str(entries[-1][5]), 'cyan')

# User Confirmation
confirmation = input('\nProcess and populate new Excel-File? [\033[92m y\033[0m | \033[91mn\033[0m ]: ')
if(confirmation != 'y' and confirmation != 'yes' and confirmation != ''): exit()

# Hardcoded Variables for Destination File - can be dynamic later
firstRow = 2

# Load Destination Workbook & Sheet
print('Creating new Excel-Workbook and importing Data ...')
wb = Workbook()
ws = wb.active
ws.title = str(pid)+'-Data'

# rows einschreiben
for row in entries:
  ws.append(row)

# saving
wb.save('./script/output/'+str(pid)+'-Processed.xlsx')

os.system('cls||clear')
printInfoBlock('File saved in "output" folder.', 'green')
print('')