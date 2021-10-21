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
  from assets.database import xls_key, xls_desc, xls_label, xls_tag, xls_area, xls_unit, xls_min, xls_max
  output = []
  for xrow in processLibData:
    for row in masterData:      # row[index] is corresponding to output order from above filter function
      if(xrow[xls_key-1] == row[0]):
        xrow[xls_desc-1]  = row[2]
        xrow[xls_label-1] = row[1]
        xrow[xls_tag-1]   = row[0]
        xrow[xls_area-1]  = row[3]
        xrow[xls_unit-1]  = row[6]
        xrow[xls_min-1]   = row[4]
        xrow[xls_max-1]   = row[5]
        break
    output.append(xrow)
  
  return compressAndSortFinalData(output)