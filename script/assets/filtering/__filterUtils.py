from assets.database import (
  firstRow, pidColumn, locationColumn,
  typeColumn, tagColumn, descColumn,
  rangeColumn, unitColumn, routeColumn,
  safetyColumn1, safetyColumn2, safetyColumn3
)

def getAllWithPid(pid, master_ws):
  
  try: pid = int(pid)
  except: pid = pid
  
  elements = []
  for key, *values in master_ws.iter_rows(min_row = firstRow):
    if(key.value == None):
      break

    if(values[pidColumn-2].value == pid):
      row = [None,None] + [v.value for v in values]     # [None, None] is just added for easier indexing when filtering
      elements.append(row)
  
  return elements

def convertControllerToInput(row):
  type = row[typeColumn]
  try:
    type = type.strip()
  finally:
    if(len(type) == 2 and type[-1] == 'C'):
      t = list(type)
      t[-1] = 'I'
      type = ''.join(t)
  return type

def createFullTag(type, row):
  tag = row[tagColumn]
  return type + str(tag)

def getDescription(row):
  return row[descColumn]

def getUnit(row):
  unit = row[unitColumn]
  if(unit == 'NA'):   # Sheet exception
    return None
  else: return unit

def createLabel(fullTag, row):
  safetyColumns = [row[safetyColumn1], row[safetyColumn2], row[safetyColumn3]]
  route = row[routeColumn]
  if any(safetyColumns):
    return fullTag + '_S'
  elif route == 'D':
    return fullTag + '_P'
  else: return fullTag

def findSafetyArea(row):
  location = row[locationColumn]
  from assets.database import safetyAreas
  if location in safetyAreas:
    return safetyAreas[location]
  else: return 'area01'
  
def createMinMaxRange(row):
  fullRange = row[rangeColumn]
  if(fullRange == None or fullRange == '' or fullRange == '…'):
    return [None, None]
  
  if(isinstance(fullRange, int) or isinstance(fullRange, float)):
    return [fullRange, None]
  
  if(isinstance(fullRange, str)):
    fullRange = fullRange.strip()
    fullRange = fullRange.split('…')
    if(len(fullRange) == 1):
      fullRange = fullRange[0].split('-')
    if(len(fullRange) == 1):
      return [fullRange[0].strip(), None]
    elif(len(fullRange) == 2):
      return [fullRange[0].strip(), fullRange[1].strip()]
      
  return [None, None]

def tryNumericTypeCoercion(value):
  try: return int(value)
  except:
    try: return float(value)
    except :return value