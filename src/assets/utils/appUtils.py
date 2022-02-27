from os import path
import re
from assets.utils.console import *
from assets.filtering.filterLogic import typicals


def askForPid():
  printInfoBlock('Set P&ID you want to filter', 'cyan')
  printListItem("Use * to select all instruments.",'cyan')
  print('')
  while True:
    pid = input('P&ID: ')
    pid = pid.strip()
    if(pid != None and pid != ''): break
    else: eraseLastLine()
  if(pid == '*'):
    pid = 'all'
  return pid

def getAllWithPid(pid, master_ws, firstRow, pidColumn):
  
  try: pid = int(pid)
  except: pid = pid
  
  elements = []
  
  if(pid == 'all'):
    for key, *values in master_ws.iter_rows(min_row = firstRow):
      if(key.value == None):
        break
      row = [None,None] + [v.value for v in values]     # [None, None] is just added for easier indexing when filtering
      elements.append(row)
  else:  
    for key, *values in master_ws.iter_rows(min_row = firstRow):
      if(key.value == None):
        break
      if(values[pidColumn-2].value == pid):
        row = [None,None] + [v.value for v in values]
        elements.append(row)
  
  return elements

def askAndReturnFilterTools():
  # Ask for Typical Input
  # Search if Typicals exists and return all typical tools from database
  # @return -> list[] of lists[filterFunction, typicalName, mergeFunction]
  printInfoBlock('Set Typicals you want to filter', 'cyan')
  print('Available Typicals are:')
  for key in typicals:
    printListItem(key, 'green')
  print('')
  
  printListItem('Typical names have to be exact. Mind lower and uppercase.', 'cyan')
  printListItem('Seperate multiple typicals with semicolons: ;', 'cyan')
  printListItem("Use * to select all Typicals.",'cyan')
  print('')
  
  while True:
    _typicals = input('Typicals: ')
    
    _typicals = _typicals.strip()
    if(_typicals == None or _typicals == ''):
      eraseLastLine()
      continue
    
    if(_typicals == '*'):
      _typicals = 'all'
    
    print('')
    
    _typicals = _typicals.split(';')
    
    if(_typicals[-1] == ''):
      _typicals.pop(-1)
    
    filterToolsList = []
    notFoundMessages = []
    for typical in _typicals:
      filterTools = getFilterTools(typical.strip())   # [FilterFunction, MergeFunction, TypicalName]
      if(filterTools == None):
        notFoundMessages.append('Couldn\'t find Typical: \''+typical+'\' in the database.')
      else:
        if(typical == 'all'):
          filterToolsList = filterTools
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
  if(typical == 'all'):
    allFilterTools = []
    for key in typicals:
      allFilterTools.append(typicals[key])
      allFilterTools[-1].append(key)
    return allFilterTools
  
  if typical in typicals:
    x = typicals[typical]
    x.append(typical)
    return x

def returnMergeDifferences(mergedList, controlList, mergedKey, controlKey):
  mergedTags = []
  for list in mergedList:
    mergedTags.append(str(list[mergedKey]).split('_', 1))
    
  controlTags = []
  for list in controlList:
    controlTags.append(list[controlKey])
  
  if len(mergedTags) == len(controlTags): return []
  
  tagDiffs = []
  for tag in mergedTags:
    if tag[0] not in controlTags:
      if len(tag) == 2:
        if 'old' in tag[1] or 'Old' in tag[1] or 'not_used' in tag[1] or 'Delete' in tag[1]:    # conditionally appends tag addition
          tagDiffs.append('_'.join(tag))
        else: tagDiffs.append(tag[0])
      else: tagDiffs.append(tag[0])
  
  messages = []
  for tag in tagDiffs:
    messages.append('--'+str(tag))
  
  if len(messages) > 0:
    messages.insert(0, 'The following signals were found in the ProcessLib Sheet but not in the Instrument Index. Therefore not updated:')  
  return messages

def removeNotUsedRangeWarnings(warnings, mergedOutput, typicalName, mergedKey):
  targetIndex = 0
  targetList = []
  for warningList in warnings:
    if re.search(r'\b'+typicalName+r'\b', warningList[0]):
      targetList = warningList
      break
    targetIndex = targetIndex + 1
  
  if len(targetList) == 0: return warnings
  
  warningHeader = targetList.pop(0)
  
  newWarningList = []
  for warning in targetList:
    w_signal = warning.split('|', 1)[0].strip()
    
    matchFound = False
    for row in mergedOutput:
      if w_signal in row[mergedKey]:
        matchFound = True
        break
    
    if matchFound:
      newWarningList.append(warning)
    
  newWarningList.insert(0, warningHeader)
  warnings[targetIndex] = newWarningList
  
  return warnings