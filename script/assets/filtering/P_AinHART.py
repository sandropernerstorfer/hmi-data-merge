def P_AinHART_Filter(instrumentRows, filterTypes):
  from assets.filtering.__filterUtils import convertControllerToInput, createFullTag, getUnit, createLabel, findSafetyArea, createMinMaxRange, tryNumericTypeCoercion
  from assets.database import locationColumn, typeColumn, tagColumn, descColumn, rangeColumn, unitColumn, routeColumn, safetyColumn1, safetyColumn2, safetyColumn3
  
  entries = []
  for row in instrumentRows:
  
    type = convertControllerToInput(row[typeColumn])
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row[tagColumn])
    
    desc = row[descColumn]
    
    unit = getUnit(row[unitColumn])
    
    label = createLabel(fullTag, row[routeColumn], [row[safetyColumn1], row[safetyColumn2], row[safetyColumn3]])
    
    area = findSafetyArea(row[locationColumn])
    
    minRange, maxRange = createMinMaxRange(row[rangeColumn])
    minRange = tryNumericTypeCoercion(minRange)
    maxRange = tryNumericTypeCoercion(maxRange)
    
    entries.append([fullTag, label, desc, area, minRange, maxRange, unit])
  
  return [entries, 'P_AinHART']