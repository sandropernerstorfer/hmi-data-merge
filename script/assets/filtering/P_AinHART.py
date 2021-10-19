def P_AinHART_Filter(instrumentRows, filterTypes):
  from assets.filtering.__filterUtils import convertControllerToInput, createFullTag, getUnit, createLabel, createSafetyArea
  from assets.database import locationColumn, typeColumn, tagColumn, descColumn, rangeColumn, unitColumn, routeColumn, safetyColumn1, safetyColumn2, safetyColumn3
  
  entries = []
  for row in instrumentRows:
  
    # Instrument Type checking
    type = convertControllerToInput(row[typeColumn])
    if type not in filterTypes: continue

    # Generate Full Tag
    fullTag = createFullTag(type, row[tagColumn])
    
    # Get Description
    desc = row[descColumn]
    
    # Get Unit
    unit = getUnit(row[unitColumn])
    
    # Generate Label
    label = createLabel(fullTag, [row[safetyColumn1], row[safetyColumn2], row[safetyColumn3]])
    
    # Generate Safety Area
    area = createSafetyArea(row[locationColumn])
        
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