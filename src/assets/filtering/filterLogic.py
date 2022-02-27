from assets.filtering.filterUtils import *


# ----------------------------------------------------------------------------------------------------------------------- #

''' Filter Functions ''' 
# Takes the Pre-Filtered Instrument Index Data ( all instruments or specific P&ID )
# Filters and Processes this Data depending on Typical Characteristics & Config File Typical Parameters
# Returns one LIST[] -> of LISTS[] -> with each list containing processed data of one Instrument, and warnings[]
# Returns all possible candidats for that typical. Merge Function will handle that filtering part

''' Merge Functions '''
# Compare the final processed output rows from the Filter Function against the corresponding ProcessLib Sheet
# Loops through the fitting ProcessLib Sheet and merges & updates everything it can with the final data
# row[index] is corresponding to the return order of the filter function of that typical

# ----------------------------------------------------------------------------------------------------------------------- #

def Faceplates_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  descCol     = i['descColumn']
  locationCol = i['locationColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# Faceplates Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    desc = getDescription(row, descCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])
  
  return entries, warnings

def Faceplates_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def PT_AInGas_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  rangeCol    = i['rangeColumn']
  unitCol     = i['unitColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# PT_AInGas Warnings:']
  for row in instrumentRows:
    
    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row, tagCol)
    
    desc = getDescription(row, descCol)
    
    unit = getUnit(row, unitCol)
    
    label = createLabel(fullTag, row, safetyCols, routeCol)
    
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    minRange, maxRange = createMinMaxRange(row, rangeCol)
    if minRange is False or maxRange is False:
      warnings.append(returnUnsureRange(row[rangeCol], fullTag))
      minRange = None
      maxRange = None
    else:
      minRange = rangeTypeCoercion(minRange)
      maxRange = rangeTypeCoercion(maxRange)
    
    entries.append([fullTag, label, desc, area, minRange, maxRange, unit])

  return entries, warnings

def PT_AInGas_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        xrow[i['rangeMin']]   = row[4]
        xrow[i['rangeMax']]   = row[5]
        xrow[i['unit']]       = row[6]
        break
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def PT_ElectricalRef_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  descCol     = i['descColumn']
  locationCol = i['locationColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# PT_ElectricalRef Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type == 'MC': pass
    else: type = convertControllerToInput(type)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    desc = getDescription(row, descCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])
  
  return entries, warnings

def PT_ElectricalRef_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    moreString  = splitTagNameString(xrow[i['key']], '_')
    if moreString == None:
      mergedOutput.append(xrow)
      continue
    for row in masterData:
      joinedKey = row[0]+'_'+moreString
      if xrow[i['key']] == joinedKey:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def PT_AInGasPART_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  descCol     = i['descColumn']
  locationCol = i['locationColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# PT_AInGasPART Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    desc = getDescription(row, descCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])
  
  return entries, warnings

def PT_AInGasPART_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def PT_Intlk_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# PT_Intlk Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, area])
  
  return entries, warnings

def PT_Intlk_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    intlkString  = splitTagNameString(xrow[i['key']], '_')
    if intlkString == None:
      mergedOutput.append(xrow)
      continue
    for row in masterData:
      joinedKey = row[0]+'_'+intlkString
      if xrow[i['key']] == joinedKey:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['area']]       = row[2]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def PT_CfgModeChg_Filter(instrumentRows, filterTypes, safetyAreas, i):
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# PT_CfgModeChg Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    desc = getDescription(row, descCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])
  
  return entries, warnings

def PT_CfgModeChg_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    moreString  = splitTagNameString(xrow[i['key']], '_')
    if moreString == None:
      mergedOutput.append(xrow)
      continue
    for row in masterData:
      joinedKey = row[0]+'_'+moreString
      if xrow[i['key']] == joinedKey:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def PT_CondSel_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# PT_CondSel Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, area])
  
  return entries, warnings

def PT_CondSel_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['desc']] = i['descStatic']
    intlkMoreString  = splitTagNameString(xrow[i['key']], '_', 1)
    if intlkMoreString == None:
      mergedOutput.append(xrow)
      continue
    for row in masterData:
      joinedKey = row[0]+'_'+intlkMoreString
      if xrow[i['key']] == joinedKey:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['area']]       = row[2]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def PT_ForkEH_Filter(instrumentRows, filterTypes, safetyAreas, i):
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# PT_ForkEH Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    desc = getDescription(row, descCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])
  
  return entries, warnings

def PT_ForkEH_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['0stText']] = i['0stTextStatic']
    xrow[i['1stText']] = i['1stTextStatic']
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def PT_Perm_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# PT_Perm Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    desc = getDescription(row, descCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])
  
  return entries, warnings

def PT_Perm_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    permString  = splitTagNameString(xrow[i['key']], '_', 1)
    if permString == None:
      mergedOutput.append(xrow)
      continue
    for row in masterData:
      joinedKey = row[0]+'_'+permString
      if xrow[i['key']] == joinedKey:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def PT_Valve_Diag_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# PT_Valve_Diag Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    desc = getDescription(row, descCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])
  
  return entries, warnings

def PT_Valve_Diag_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    moreString  = splitTagNameString(xrow[i['key']], '_', 1)
    if moreString == None:
      mergedOutput.append(xrow)
      continue
    for row in masterData:
      joinedKey = row[0]+'_'+moreString
      if xrow[i['key']] == joinedKey:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_AInHART_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  rangeCol    = i['rangeColumn']
  unitCol     = i['unitColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_AInHART Warnings:']
  for row in instrumentRows:
    
    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    type = convertControllerToInput(type)
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row, tagCol)
    
    desc = getDescription(row, descCol)
    
    unit = getUnit(row, unitCol)
    
    label = createLabel(fullTag, row, safetyCols, routeCol)
    
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    minRange, maxRange = createMinMaxRange(row, rangeCol)
    if minRange is False or maxRange is False:
      warnings.append(returnUnsureRange(row[rangeCol], fullTag))
      minRange = None
      maxRange = None
    else:
      minRange = rangeTypeCoercion(minRange)
      maxRange = rangeTypeCoercion(maxRange)
    
    entries.append([fullTag, label, desc, area, minRange, maxRange, unit])

  return entries, warnings

def P_AInHART_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        xrow[i['rangeMin']]   = row[4]
        xrow[i['rangeMax']]   = row[5]
        xrow[i['unit']]       = row[6]
        break
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_AIChan_Filter(instrumentRows, filterTypes, safetyAreas, i):
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  unitCol     = i['unitColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_AIChan Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    type = convertControllerToInput(type)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    desc = getDescription(row, descCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    unit = getUnit(row, unitCol)
    
    entries.append([fullTag, label, desc, area, unit])
  
  return entries, warnings

def P_AIChan_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['PVEUMin']] = int(i['PVEUMinStatic'])
    xrow[i['PVEUMax']] = int(i['PVEUMaxStatic'])
    chanString  = splitTagNameString(xrow[i['key']], '_', 1)
    if chanString == None:
      mergedOutput.append(xrow)
      continue
    for row in masterData:
      joinedKey = row[0]+'_'+chanString
      if xrow[i['key']] == joinedKey:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        xrow[i['unit']]       = row[4]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_AIn_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  rangeCol    = i['rangeColumn']
  unitCol     = i['unitColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_AIn Warnings:']
  for row in instrumentRows:
    
    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    type = convertControllerToInput(type)
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row, tagCol)
    
    desc = getDescription(row, descCol)
    
    unit = getUnit(row, unitCol)
    
    label = createLabel(fullTag, row, safetyCols, routeCol)
    
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    minRange, maxRange = createMinMaxRange(row, rangeCol)
    if minRange is False or maxRange is False:
      warnings.append(returnUnsureRange(row[rangeCol], fullTag))
      minRange = None
      maxRange = None
    else:
      minRange = rangeTypeCoercion(minRange)
      maxRange = rangeTypeCoercion(maxRange)
    
    entries.append([fullTag, label, desc, area, minRange, maxRange, unit])

  return entries, warnings

def P_AIn_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['InpRawMin']] = int(i['InpRawMinStatic'])
    xrow[i['InpRawMax']] = int(i['InpRawMaxStatic'])
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        xrow[i['rangeMin']]   = row[4]
        xrow[i['rangeMax']]   = row[5]
        xrow[i['unit']]       = row[6]
        break
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_DIn_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_DIn Warnings:']
  for row in instrumentRows:
    
    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row, tagCol)
    desc = getDescription(row, descCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])

  return entries, warnings

def P_DIn_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['0stText']] = i['0stTextStatic']
    xrow[i['1stText']] = i['1stTextStatic']
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_E300Ovld_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_E300Ovld Warnings:']
  for row in instrumentRows:
    
    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row, tagCol)
    desc = getDescription(row, descCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])

  return entries, warnings

def P_E300Ovld_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    ovldString  = splitTagNameString(xrow[i['key']], '_', 1)
    if ovldString == None:
      mergedOutput.append(xrow)
      continue
    for row in masterData:
      joinedKey = row[0]+'_'+ovldString
      if xrow[i['key']] == joinedKey:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_Motor_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_Motor Warnings:']
  for row in instrumentRows:
    
    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row, tagCol)
    desc = getDescription(row, descCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])

  return entries, warnings

def P_Motor_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['PCmdLock']] = int(i['PCmdLockStatic'])
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_PF52x_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_PF52x Warnings:']
  for row in instrumentRows:
    
    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row, tagCol)
    desc = getDescription(row, descCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])

  return entries, warnings

def P_PF52x_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['PCmdLock']] = int(i['PCmdLockStatic'])
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_PF755_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_PF755 Warnings:']
  for row in instrumentRows:
    
    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row, tagCol)
    desc = getDescription(row, descCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])

  return entries, warnings

def P_PF755_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['PCmdLock']] = int(i['PCmdLockStatic'])
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_PIDE_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  rangeCol    = i['rangeColumn']
  unitCol     = i['unitColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_PIDE Warnings:']
  for row in instrumentRows:
    
    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    type = convertInputToController(type)
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row, tagCol)
    
    desc = getDescription(row, descCol)
    
    unit = getUnit(row, unitCol)
    
    label = createLabel(fullTag, row, safetyCols, routeCol)
    
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    minRange, maxRange = createMinMaxRange(row, rangeCol)
    if minRange is False or maxRange is False:
      warnings.append(returnUnsureRange(row[rangeCol], fullTag))
      minRange = None
      maxRange = None
    else:
      minRange = rangeTypeCoercion(minRange)
      maxRange = rangeTypeCoercion(maxRange)
    
    pvNavTag = convertFullTagFromTo(fullTag, 'C', 'I')
    cvNavTag = convertFullTagFromTo(fullTag, 'C', 'V')
    
    entries.append([fullTag, label, desc, area, minRange, maxRange, unit, pvNavTag, cvNavTag])

  return entries, warnings

def P_PIDE_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['HasPVNav']] = int(i['HasPVNavStatic'])
    xrow[i['HasCVNav']] = int(i['HasCVNavStatic'])
    xrow[i['PCmdLock']] = int(i['PCmdLockStatic'])
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        xrow[i['rangeMin']]   = row[4]
        xrow[i['rangeMax']]   = row[5]
        xrow[i['unit']]       = row[6]
        xrow[i['PVNavTag']]   = row[7]
        xrow[i['CVNavTag']]   = row[8]
        break
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_ResInh_Filter(instrumentRows, filterTypes, safetyAreas, i):
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_ResInh Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, area])
  
  return entries, warnings

def P_ResInh_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    resihnString  = splitTagNameString(xrow[i['key']], '_', 1)
    if resihnString == None:
      mergedOutput.append(xrow)
      continue
    for row in masterData:
      joinedKey = row[0]+'_'+resihnString
      if xrow[i['key']] == joinedKey:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['area']]       = row[2]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_RunTime_Filter(instrumentRows, filterTypes, safetyAreas, i):
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_RunTime Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, area])
  
  return entries, warnings

def P_RunTime_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['desc']] = i['descStatic']
    runtimeString  = splitTagNameString(xrow[i['key']], '_', 1)
    if runtimeString == None:
      mergedOutput.append(xrow)
      continue
    for row in masterData:
      joinedKey = row[0]+'_'+runtimeString
      if xrow[i['key']] == joinedKey:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['area']]       = row[2]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_ValveC_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_ValveC Warnings:']
  for row in instrumentRows:
    
    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue
    
    fullTag = createFullTag(type, row, tagCol)
    desc = getDescription(row, descCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    cvNavTag = convertFullTagFromTo(fullTag, 'V', 'C')
    
    entries.append([fullTag, label, desc, area, cvNavTag])

  return entries, warnings

def P_ValveC_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['PCmdLock']] = int(i['PCmdLockStatic'])
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        xrow[i['CVNavTag']]   = row[4]
        break
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_ValveSO_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_ValveSO Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    desc = getDescription(row, descCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])
  
  return entries, warnings

def P_ValveSO_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['PCmdLock']] = int(i['PCmdLockStatic'])
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_ValveStats_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_ValveStats Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    desc = getDescription(row, descCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])
  
  return entries, warnings

def P_ValveStats_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    valvestatsString  = splitTagNameString(xrow[i['key']], '_', 1)
    if valvestatsString == None:
      mergedOutput.append(xrow)
      continue
    for row in masterData:
      joinedKey = row[0]+'_'+valvestatsString
      if xrow[i['key']] == joinedKey:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


def P_VSD_Filter(instrumentRows, filterTypes, safetyAreas, i):
  
  typeCol     = i['typeColumn']
  tagCol      = i['tagColumn']
  locationCol = i['locationColumn']
  descCol     = i['descColumn']
  routeCol    = i['routeColumn']
  safetyCols  = [i['safetyColumn1'], i['safetyColumn2'], i['safetyColumn3']]
  
  entries = []
  warnings = ['# P_VSD Warnings:']
  for row in instrumentRows:

    if(checkIfRowUsable(row, typeCol, tagCol)): pass
    else: continue
    
    type = getType(row, typeCol)
    if type not in filterTypes: continue

    fullTag = createFullTag(type, row, tagCol)
    label = createLabel(fullTag, row, safetyCols, routeCol)
    desc = getDescription(row, descCol)
    area = findSafetyArea(row, safetyAreas, locationCol)
    
    entries.append([fullTag, label, desc, area])
  
  return entries, warnings

def P_VSD_Merge(masterData, processLibData, i):
  mergedOutput = []
  controlOutput = []
  iteration = 0
  for xrow in processLibData:
    if iteration >= i['firstRow']:
      if xrow[i['key']] is None or str(xrow[i['key']]).strip() == '': continue
    iteration += 1
    xrow[i['PCmdLock']] = int(i['PCmdLockStatic'])
    for row in masterData:
      if xrow[i['key']] == row[0]:
        controlOutput.append(row)
        xrow[i['tag']]        = row[0]
        xrow[i['label']]      = row[1]
        xrow[i['desc']]       = row[2]
        xrow[i['area']]       = row[3]
        break 
    mergedOutput.append(xrow)
  return compressAndSortFinalData(mergedOutput, i['firstRow'], i['instanceKey']), controlOutput


typicals = {
  'Faceplates': [Faceplates_Filter, Faceplates_Merge],
  'PT_AInGas': [PT_AInGas_Filter, PT_AInGas_Merge],
  'PT_ElectricalRef': [PT_ElectricalRef_Filter, PT_ElectricalRef_Merge],
  'PT_AInGasPART': [PT_AInGasPART_Filter, PT_AInGasPART_Merge],
  'PT_Intlk': [PT_Intlk_Filter, PT_Intlk_Merge],
  'PT_CfgModeChg': [PT_CfgModeChg_Filter, PT_CfgModeChg_Merge],
  'PT_CondSel': [PT_CondSel_Filter, PT_CondSel_Merge],
  'PT_ForkEH': [PT_ForkEH_Filter, PT_ForkEH_Merge],
  'PT_Perm': [PT_Perm_Filter, PT_Perm_Merge],
  'PT_Valve_Diag': [PT_Valve_Diag_Filter, PT_Valve_Diag_Merge],
  'P_AInHART': [P_AInHART_Filter, P_AInHART_Merge],
  'P_AIChan': [P_AIChan_Filter, P_AIChan_Merge],
  'P_AIn': [P_AIn_Filter, P_AIn_Merge],
  'P_DIn': [P_DIn_Filter, P_DIn_Merge],
  'P_E300Ovld': [P_E300Ovld_Filter, P_E300Ovld_Merge],
  'P_Motor': [P_Motor_Filter, P_Motor_Merge],
  'P_PF52x': [P_PF52x_Filter, P_PF52x_Merge],
  'P_PF755': [P_PF755_Filter, P_PF755_Merge],
  'P_PIDE': [P_PIDE_Filter, P_PIDE_Merge],
  'P_ResInh': [P_ResInh_Filter, P_ResInh_Merge],
  'P_RunTime': [P_RunTime_Filter, P_RunTime_Merge],
  'P_ValveC': [P_ValveC_Filter, P_ValveC_Merge],
  'P_ValveSO': [P_ValveSO_Filter, P_ValveSO_Merge],
  'P_ValveStats': [P_ValveStats_Filter, P_ValveStats_Merge],
  'P_VSD': [P_VSD_Filter, P_VSD_Merge]
}