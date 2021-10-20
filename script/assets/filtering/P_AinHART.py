from assets.filtering.__filterUtils import convertControllerToInput, createFullTag, getDescription, getUnit, createLabel, findSafetyArea, createMinMaxRange, tryNumericTypeCoercion, compressAndSortFinalData

def P_AInHART_Filter(instrumentRows, filterTypes):
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
  
  return [entries, 'P_AInHART']

def P_AInHART_Merge(masterData, processLibData):
  output = []
  for xrow in processLibData:
    for row in masterData:
      if(xrow[2] == row[0]):
        xrow[4] = row[2]
        xrow[5] = row[1]
        xrow[6] = row[0]
        xrow[7] = row[3]
        xrow[8] = row[6]
        xrow[10] = row[4]
        xrow[11] = row[5]
        break
    output.append(xrow)
  
  return compressAndSortFinalData(output)