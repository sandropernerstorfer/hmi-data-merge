import tkinter, time, re
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
filePath = askopenfilename(
    filetypes = [( 'Excel File', '.xlsx .xls')]
  )
root.destroy()
clearConsole()
if(filePath == ''):
  exit()
print('[\033[92mx\033[0m] Select Master-File in dialog')
time.sleep(2)

# Load Master-Workbook & Target-Sheet
try:
  print(' | ')
  print(" *  Loading Excel Data from "+"\033[92m.../"+filePath.split('/')[-2]+'/'+filePath.split('/')[-1]+"\033[0m")
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

firstRow  = 8
pidCol    = 3
typeCol   = 6
tagCol    = 7
descCol   = 10
rangeCol  = 46
unitCol   = 47
routeCol  = 29
sCol1     = 34
sCol2     = 35
sCol3     = 36
locCol    = 5
header = ['full-tag', 'label', 'description', 'area', 'range-min', 'range-max', 'unit']

print('')
pid = int(pid)

# Loop through Sheet-Rows and save elements with PID in list
entries = [header]
for key, *values in master_ws.iter_rows(min_row = firstRow):
  
  if(key.value == None):  # Stop if row A has no value
    break
  
  if(values[pidCol-2].value == pid):  # Find row with defined PID
    row = [v.value for v in values]
    row.insert(0, None)   # None, None, is just for easier indexing
    row.insert(0, None)
    
    desc  = row[descCol]
    unit  = row[unitCol]
    
    if(len(row[typeCol]) == 2 and row[typeCol][-1] == 'C'):
      t = list(row[typeCol])
      t[-1] = 'I'
      row[typeCol] = ''.join(t)
    fullTag = row[typeCol] + str(row[tagCol])
    
    label = fullTag
    if(row[sCol1] != None or row[sCol2] != None or row[sCol3] != None):
      label += '_S'
    elif(row[routeCol] == 'D'):
      label += '_P'
      
    area = 'area01'
    if row[locCol] in safetyAreas:
      area = safetyAreas[row[locCol]]
        
    rangeMin = None
    rangeMax = None
    if(row[rangeCol] != None):
      fullRange = row[rangeCol].strip()
      if(fullRange == '' or fullRange == '...' or fullRange == '…'):
        rangeMin = None
        rangeMax = None
      else:
        splitRanges = [int(d) for d in re.findall(r'-?\d+', fullRange)]
        l = len(splitRanges)
        if l == 0:
          rangeMin = None
          rangeMax = None
        if l == 1:
          rangeMin = splitRanges[0]
          rangeMax = None
        else:
          rangeMin = splitRanges[0]
          rangeMax = splitRanges[1]

    entries.append([fullTag, label, desc, area, rangeMin, rangeMax, unit])

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
wb.save('./script/output/'+str(pid)+'-Processed.xlsx')
clearConsole()
printInfoBlock('File saved in "output" folder.', 'green')
print('')