from assets.utils.console import printListItem


def checkIfRowUsable(row, typeColumn, tagColumn):
  if row[typeColumn] == None or row[tagColumn] == None: return False
  if row[typeColumn] == '-' or row[tagColumn] == '-': return False
  return True

def getType(row, typeColumn):
  return str(row[typeColumn]).strip()

def convertControllerToInput(type):
  try:
    type = str(type).strip()
  except: return ''
  finally:
    if len(type) == 2 and type[-1] == 'C':
      t = list(type)
      t[-1] = 'I'
      type = ''.join(t)
  return type

def convertInputToController(type):
  try:
    type = str(type).strip()
  except: return ''
  finally:
    if len(type) == 2 and type[-1] == 'I':
      t = list(type)
      t[-1] = 'C'
      type = ''.join(t)
  return type

def convertFullTagFromTo(fullTag:str, convFrom:str, convTo:str):
  return fullTag.replace(convFrom, convTo, 1)

def createFullTag(type, row, tagColumn):
  tag = row[tagColumn]
  return str(type) + str(tag)

def getDescription(row, descColumn):
  return row[descColumn]

def getUnit(row, unitColumn):
  unit = row[unitColumn]
  if unit == None: return None
  try: unit = unit.strip()
  except: pass
  if unit == 'NA' or unit == '-': return None
  else: return unit

def createLabel(fullTag, row, safetyColumns, routeColumn):
  route = row[routeColumn]
  allSafetyCols = []
  for col in safetyColumns: allSafetyCols.append(row[col])
  if any(allSafetyCols):
    return fullTag + '_S'
  elif route is not None and 'D' in route:
    return fullTag + '_P'
  else: return fullTag

def findSafetyArea(row, safetyAreas, locationColumn):
  location = row[locationColumn]
  if location in safetyAreas:
    return safetyAreas[location]
  else: return 'area01'

def createMinMaxRange(row, rangeColumn):
  
  fullRange = row[rangeColumn]
  
  # NONE Value Guard
  if fullRange is None: return None, None
  
  # Check if already SINGLE NUMBER
  if(isinstance(fullRange, int) or isinstance(fullRange, float)):
    return 0, fullRange
  
  # Remove unnecessary chars
  removers = [' ', '%']
  fullRange = removeFromString(fullRange, removers)
  
  # Check if contains at least one digit
  if any(char.isdigit() for char in fullRange) == False: return [None, None]

  # Check if only single value by trying to convert into FLOAT or INT
  try: 
    x = float(fullRange)
    return False, False
  except: pass
  try:
    x = int(fullRange)
    return False, False
  except: pass
  
  # Try to split at specific symbols and return 2 values
  splitters = ['…', '/', '...', '–', '+', '-']
  min, max = tryStringSplitting(fullRange, splitters)
  
  # Check if no usable values returned
  if min is False or max is False:
    return False, False
  
  # Return Min & Max Values if both contain digits
  if any(char.isdigit() for char in min) and any(char.isdigit() for char in max):
    return min, max
  
  # Else Return warnings
  return False, False

def removeFromString(value:str, removers: list):
  for remover in removers:
    x = value.replace(remover, '')
  return x

def tryStringSplitting(value: str, splitters: list):
  for splitter in splitters:
    x = value.split(splitter)
    if len(x) == 2: return x[0], x[1]
    else: continue
  return False, False

def returnUnsureRange(range, fullTag):
  spaceForTag = 9
  tagAsText = str(fullTag)
  textLength = len(tagAsText)
  spaceForTag -= textLength
  if spaceForTag < 0: spaceForTag = 0
  tagText = fullTag+spaceForTag*' '
  
  warningMessage = tagText+' | filter unsure about Range: '+str(range)
  return warningMessage

def rangeTypeCoercion(value):
  if value == None: return value
  value = str(value)
  value = value.replace(',', '.')
  value = value.replace(' ', '')
  try: return int(value)
  except: return value

def splitTagNameString(value, splitter:str, maxsplit = -1):
  string = str(value)
  split = string.split(splitter, maxsplit)
  if len(split) == 2: return split[1]
  else: return None

def compressAndSortFinalData(dataSet, firstRow, sortKey):
  for i in range(firstRow):
    dataSet.pop(0)
  try:
    dataSet = sorted(dataSet, key=lambda x: x[sortKey])
  except:
    dataSet.insert(0, 'sortError')
  return dataSet