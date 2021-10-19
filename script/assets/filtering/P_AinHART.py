def P_AinHART_Filter(instrumentRows, filterTypes):
  import re
  from assets.database import safetyAreas
  from assets.database import locationColumn, typeColumn, tagColumn, descColumn, rangeColumn, unitColumn, routeColumn, safetyColumn1, safetyColumn2, safetyColumn3
  
  
  entries = []
  for key, *values in instrumentRows:
    
    # Convert Controller definition into Input (FC -> FI)
    type = values[typeColumn - 3]
    try:
      type = type.strip()
    finally:
      if(len(type) == 2 and type[-1] == 'C'):
        t = list(type)
        t[-1] = 'I'
        type = ''.join(t)
      if type not in filterTypes:
        continue
    
    row = [None, None, None] + [v for v in values]     # 3 * None is just for easier index

    fullTag = type + str(row[tagColumn])
    desc = row[descColumn]
    
    unit = row[unitColumn]
    if row[unitColumn] == 'NA': unit = None
    
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
    fullRange = row[rangeColumn]
    
    if(fullRange == None or fullRange == '' or fullRange == '…'):
      rangeMin = None
      rangeMax = None
    elif(isinstance(fullRange, int) or isinstance(fullRange, float)):
      rangeMin = fullRange
      rangeMax = None
    elif(isinstance(fullRange, str)):
      fullRange = fullRange.strip()
      fullRange = fullRange.split('…')
      if(len(fullRange) == 1):
        fullRange = fullRange[0].split('-')   # exception with -
      if(len(fullRange) == 1):
        rangeMin = fullRange[0].strip()
        rangeMax = None
      elif(len(fullRange) == 2):
        rangeMin = fullRange[0].strip()
        rangeMax = fullRange[1].strip()
      else:
        rangeMin = None
        rangeMax = None
        
      try: rangeMin = int(rangeMin)
      except: 
        try: rangeMin = float(rangeMin)
        except: rangeMin = rangeMin
        
      try: rangeMax = int(rangeMax)
      except: 
        try: rangeMax = float(rangeMax)
        except: rangeMax = rangeMax
    
    entries.append([fullTag, label, desc, area, rangeMin, rangeMax, unit])
  
  return [entries, 'P_AinHART']