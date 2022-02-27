from sys import stdout
from os import system


consoleColorCodes = {
  '0':      '0',
  'blue':   '94',
  'red':    '91',
  'yellow': '93',
  'green':  '92',
  'cyan':   '96'
}
def eraseLastLine():
  stdout.write('\x1b[1A') 
  stdout.write('\x1b[2K')
  
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
  print('')
  printInfoBlock('Found '+str(len(entries))+' entries with P&ID: '+pid, color)
  print('')
  
def printTypicalFilterResults(entries, typical):
  if(len(entries) == 0):
    color = 'red'
  else: color = 'green'
  
  spaceForNumber = 5
  numberAsText = str(len(entries))
  textLength = len(numberAsText)
  spaceForNumber -= textLength
  if spaceForNumber < 0: spaceForNumber = 0
  entriesText = numberAsText+spaceForNumber*' '
  
  printListItem('Found \033[92m'+entriesText+'\033[0m candidates for \033[92m'+typical+'\033[0m', color)
  
def getUserConfirmation(text):
  confirmation = input(text+' [\033[92m y\033[0m | \033[91mn\033[0m ]: ')
  if(confirmation != 'y' and confirmation != 'yes' and confirmation != ''):
    return False
  else:
    return True

def printAllFilterWarnings(allWarnings: list):
  warningsPrinted = 0
  for warnings in allWarnings:
    if len(warnings) == 1: continue
    print('')
    warningsPrinted += 1
    for msg in warnings:
      printListItem(msg, 'yellow')
  
  if warningsPrinted > 0: return True
  return False