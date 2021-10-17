import time, tkinter, sys
from os import system
from tkinter.filedialog import askopenfilename
from openpyxl import load_workbook
from assets.database import typicals

def eraseLastLine():
  CURSOR_UP_ONE = '\x1b[1A' 
  ERASE_LINE = '\x1b[2K'
  sys.stdout.write(CURSOR_UP_ONE) 
  sys.stdout.write(ERASE_LINE)

def clearConsole():
  system('cls||clear')

def printInfoBlock(text, color = '0'):
  l = len(text)
  if color == 'blue':     color = '94'
  elif color == 'red':      color = '91'
  elif color == 'yellow':   color = '93'
  elif color == 'green':    color = '92'
  elif color == 'cyan':     color = '96'
  
  print('-'+l*'-'+'-')
  print(' \033['+color+'m'+text+'\033[0m ')
  print('-'+l*'-'+'-')

def getMasterPath():
  root = tkinter.Tk()
  root.withdraw()
  print('[ ] Select master file in dialog')
  time.sleep(.8)
  filePath = askopenfilename(filetypes = [( 'Excel File', '.xlsx .xls')])
  root.destroy()
  clearConsole()
  if(filePath == ''):
    exit()
  print('[\033[92mx\033[0m] Select master file in dialog')
  time.sleep(2)
  return filePath

def getMasterSheet(filePath):
  try:
    print(" |\n[ ] Loading data from "+"\033[92m.../"+filePath.split('/')[-2]+'/'+filePath.split('/')[-1]+"\033[0m")
    master_wb = load_workbook(filePath)
    eraseLastLine()
    print("[\033[92mx\033[0m] Loading data from "+"\033[92m.../"+filePath.split('/')[-2]+'/'+filePath.split('/')[-1]+"\033[0m\n")
    return master_wb.active
  except:
    clearConsole()
    print('Something went wrong while loading the master file. Make sure you \033[93mclose the file\033[0m before running the script.\n')
    exit()
    
def askForPid():
  pid = input('P&ID: ')
  return pid

def askForTypical():
  typical = input('Typical: ')
  return typical

def getFilterFunction(typical):
  typicalFilterFunction = None
  if typical in typicals:
    typicalFilterFunction = typicals[typical]
  return typicalFilterFunction

def printFilterResults(entries):
  print('')
  printInfoBlock('Found '+str(len(entries) - 1)+' entries.', 'cyan')
  printInfoBlock('First: '+entries[1][0]+' ... Last: '+entries[-1][0], 'cyan')
  print('')

def getUserConfirmation(text):
  confirmation = input(text+' [\033[92m y\033[0m | \033[91mn\033[0m ]: ')
  if(confirmation != 'y' and confirmation != 'yes' and confirmation != ''):
    return False
  else:
    return True