import time, tkinter, sys
from os import system
from tkinter.filedialog import askopenfilename
from openpyxl import load_workbook
from assets.database import typicals, typeColumn, tagColumn

# --------------------------------- #
#
# Console Functions
#
consoleColorCodes = {
  '0':      '0',
  'blue':   '94',
  'red':    '91',
  'yellow': '93',
  'green':  '92',
  'cyan':   '96'
}
def eraseLastLine():
  sys.stdout.write('\x1b[1A') 
  sys.stdout.write('\x1b[2K')
  
def clearConsole():
  system('cls||clear')
  
def printListItem(text,color = '0'):
  color = consoleColorCodes[color]
  print('\033['+color+'m*\033[0m '+text)
  
def printInfoBlock(text, color = '0'):
  l = len(text)
  color = consoleColorCodes[color]
  print('-'+l*'-'+'-')
  print(' \033['+color+'m'+text+'\033[0m ')
  print('-'+l*'-'+'-')
  
def printPidFilterResult(entries, pid, color):
  printInfoBlock('Found '+str(len(entries))+' entries with PID: '+pid, color)
  if(len(entries) > 0):
    printListItem('First -> '+entries[0][typeColumn]+str(entries[0][tagColumn]), 'green')
    printListItem('Last  -> '+entries[-1][typeColumn]+str(entries[-1][tagColumn]), 'green')
  print('')
  
def printTypicalFilterResults(entries, typical):
  if(len(entries) == 0):
    color = 'red'
  else: color = 'green'
  printListItem('Found \033[92m'+str(len(entries))+'\033[0m with Typical: \033[92m'+typical+'\033[0m', color)
  
def getUserConfirmation(text):
  confirmation = input(text+' [\033[92m y\033[0m | \033[91mn\033[0m ]: ')
  if(confirmation != 'y' and confirmation != 'yes' and confirmation != ''):
    return False
  else:
    return True

# --------------------------------- #
#
# Application Circle Functions
#
# Get Excel Workbook, Sheet, and Data
#
def getExcelPath(fileName):
  root = tkinter.Tk()
  root.withdraw()
  print('[ ] Select '+fileName+'-File in dialog')
  time.sleep(.8)
  filePath = askopenfilename(filetypes = [( 'Excel File', '.xlsx .xls')])
  root.destroy()
  clearConsole()
  if(filePath == ''):
    exit()
  print('[\033[92mx\033[0m] Select '+fileName+'-File in dialog')
  time.sleep(2)
  return filePath

def getExcelSheet(filePath, fileName, sheetName):
  try:
    print(" |\n[ ] Loading data from "+"\033[92m.../"+filePath.split('/')[-2]+'/'+filePath.split('/')[-1]+"\033[0m")
    wb = load_workbook(filePath)
    eraseLastLine()
    print("[\033[92mx\033[0m] Loading data from "+"\033[92m.../"+filePath.split('/')[-2]+'/'+filePath.split('/')[-1]+"\033[0m\n")
    return wb[sheetName]
  except:
    clearConsole()
    # print(' \033[91m*\033[0m Something went wrong while loading the '+fileName+' File.\n\n Make sure\n \033[93m*\033[0m you \033[93mclose the file\033[0m before running the script.\n \033[93m*\033[0m there is an \033[93m"'+sheetName+'"\033[0m Sheet.\n')
    printListItem('Something went wrong while loading the '+fileName+' File.', 'red')
    print('\nMake sure ...')
    printListItem('you \033[93mclose the file\033[0m before running the script.', 'yellow')
    printListItem('there is an \033[93m"'+sheetName+'"\033[0m Sheet.','yellow')
    print('')
    exit()

#
# Ask for PID Input
#
def askForPid():
  printInfoBlock('Set P&ID you want to filter', 'cyan')
  print('')
  while True:
    pid = input('P&ID: ')
    pid = pid.strip()
    if(pid != None and pid != ''): break
    else: eraseLastLine()
  return pid

#
# Ask for Typical Input
# Search if Typicals exists and return all typical tools from database
# @return -> list[] of lists[filterFunction, typicalName]
#
def askAndReturnFilterTools():
  printInfoBlock('Set Typicals you want to filter', 'cyan')
  printListItem('Typical names have to be exact. Mind lower and uppercase.', 'cyan')
  printListItem('Seperate multiple typicals with semicolons: ;', 'cyan')
  print('')
  while True:
    typicals = input('Typicals: ')
    
    typicals = typicals.strip()
    if(typicals == None or typicals == ''):
      eraseLastLine()
      continue
    
    print('')
    
    typicals = typicals.split(';')
    
    if(typicals[-1] == ''):
      typicals.pop(-1)
    
    filterToolsList = []
    notFoundMessages = []
    for typical in typicals:
      filterTools = getFilterTools(typical.strip())
      if(filterTools == None):
        notFoundMessages.append('Couldn\'t find Typical: \''+typical+'\' in the database.')
      else:
        filterToolsList.append(filterTools)
    
    if(len(filterToolsList) == 0):
      printListItem('None of the Typicals were found in the database.', 'red')
      print('')
      confirmation = getUserConfirmation('Want to enter the typicals again ?')
      print('')
      if(confirmation == True): continue
      else: exit()
    
    if(len(notFoundMessages) > 0):
      for msg in notFoundMessages:
        printListItem(msg, 'yellow')
      print('')
      confirmation = getUserConfirmation('Want to enter the typicals again ?')
      print('')
      if(confirmation == True):
        continue
    
    break
  return filterToolsList

def getFilterTools(typical):
  filterTools = None
  if typical in typicals:
    filterTools = typicals[typical]
  return filterTools
