from assets.filtering.__filterUtils import convertControllerToInput, createFullTag, getDescription, getUnit, createLabel, findSafetyArea, createMinMaxRange, tryNumericTypeCoercion

def P_AinHART_Filter(instrumentRows, filterTypes):
  entries = []
  for row in instrumentRows:
  
    type = convertControllerToInput(row)
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row)
    
    desc = getDescription(row)
    
    unit = getUnit(row)
    
    label = createLabel(fullTag, row)
    
    area = findSafetyArea(row)
    
    minRange, maxRange = createMinMaxRange(row)
    minRange = tryNumericTypeCoercion(minRange)
    maxRange = tryNumericTypeCoercion(maxRange)
    
    entries.append([fullTag, label, desc, area, minRange, maxRange, unit])
  
  return [entries, 'P_AinHART']