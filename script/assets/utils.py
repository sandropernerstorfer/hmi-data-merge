import time, tkinter, sys
from os import system
from tkinter.filedialog import askopenfilename
from openpyxl import load_workbook
from assets.database import typicals

# --------------------------------- #
#
# Console Functions
#
def eraseLastLine():
  sys.stdout.write('\x1b[1A') 
  sys.stdout.write('\x1b[2K')
def clearConsole():
  system('cls||clear')
def printInfoBlock(text, color = '0'):
  l = len(text)
  if color   == 'blue':     color = '94'
  elif color == 'red':      color = '91'
  elif color == 'yellow':   color = '93'
  elif color == 'green':    color = '92'
  elif color == 'cyan':     color = '96'
  print('-'+l*'-'+'-')
  print(' \033['+color+'m'+text+'\033[0m ')
  print('-'+l*'-'+'-')
def printPidFilterResult(entries, pid, color):
  printInfoBlock('Found '+str(len(entries))+' entries with PID: '+pid, color)
  if(len(entries) > 0):
    printInfoBlock('First: '+entries[0][4]+str(entries[0][5])+' ... Last: '+entries[-1][4]+str(entries[-1][5]), color)
  print('')
def printTypicalFilterResults(entries, typical):
  print('')
  printInfoBlock('Found '+str(len(entries))+' entries with Typical: '+typical, 'cyan')
  print('')
def getUserConfirmation(text):
  confirmation = input(text+' [\033[92m y\033[0m | \033[91mn\033[0m ]: ')
  if(confirmation != 'y' and confirmation != 'yes' and confirmation != ''):
    return False
  else:
    return True

#
# Application Functions
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
    print(' \033[91m*\033[0m Something went wrong while loading the '+fileName+' File.\n\n Make sure\n \033[93m*\033[0m you \033[93mclose the file\033[0m before running the script.\n \033[93m*\033[0m there is an \033[93m"'+sheetName+'"\033[0m Sheet.\n')
    exit()
    
def askForPid():
  printInfoBlock('Set P&ID you want to filter', 'cyan')
  print('')
  while True:
    pid = input('P&ID: ')
    pid = pid.strip()
    if(pid != None and pid != ''): break
    else: eraseLastLine()
  return pid

def askAndReturnFilterFunction(pid):
  printInfoBlock('Set Typicals you want to filter', 'cyan')
  print('')
  while True:
    typical = input('Typicals: [seperate with ;] ')
    typical = typical.strip()
    if(typical == None or typical == ''):
      eraseLastLine()
      continue
    
    filterFunction = getFilterFunction(typical)
    if(filterFunction != None):
      break
    else:
      clearConsole()
      print('\033[93m*\033[0m Couldn\'t find "'+typical+'" in the typicals list. Try searching again.\n')
      print('P&ID: '+pid)
  return filterFunction

def getFilterFunction(typical):
  filterFunction = None
  if typical in typicals:
    filterFunction = typicals[typical][0]
  return filterFunction
