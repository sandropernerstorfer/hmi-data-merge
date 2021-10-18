def P_AinHART_Filter(instrumentRows, filterTypes):
  import re
  from assets.database import safetyAreas

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
  
  # Loop through Sheet-Rows and save elements with PID in list
  entries = []
  for key, *values in instrumentRows:
    
    row = [None, None, None] + [v for v in values]     # 3 * None is just for easier indexing

    desc = row[descCol]
    
    unit = row[unitCol]
    if row[unitCol] == 'NA': unit = None
    
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
  
  return [entries, 'P_AinHART']

def P_AinHART_Merge():
  return 'merge function'