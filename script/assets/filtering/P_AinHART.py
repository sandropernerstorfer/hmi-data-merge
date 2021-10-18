def P_AinHART_Filter(instrumentRows, filterTypes):
  import re
  from assets.database import safetyAreas
  from assets.database import locationColumn, typeColumn, tagColumn, descColumn, rangeColumn, unitColumn, routeColumn, safetyColumn1, safetyColumn2, safetyColumn3
  
  
  # Loop through Sheet-Rows and save elements with PID in list
  entries = []
  for key, *values in instrumentRows:
    
    row = [None, None, None] + [v for v in values]     # 3 * None is just for easier indexing

    desc = row[descColumn]
    
    unit = row[unitColumn]
    if row[unitColumn] == 'NA': unit = None
    
    if(len(row[typeColumn]) == 2 and row[typeColumn][-1] == 'C'):
      t = list(row[typeColumn])
      t[-1] = 'I'
      row[typeColumn] = ''.join(t)
    fullTag = row[typeColumn] + str(row[tagColumn])
    
    label = fullTag
    if(row[safetyColumn1] != None or row[safetyColumn2] != None or row[safetyColumn3] != None):
      label += '_S'
    elif(row[routeColumn] == 'D'):
      label += '_P'
      
    area = 'area01'
    if row[locationColumn] in safetyAreas:
      area = safetyAreas[row[locationColumn]]
        
    rangeMin = None
    rangeMax = None
    if(row[rangeColumn] != None):
      fullRange = row[rangeColumn].strip()
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