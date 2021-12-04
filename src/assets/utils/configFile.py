import json
from assets.filtering.filterLogic import typicals


def parseConfigJSON(jsonData):
  try:
    configData = json.loads(jsonData)
    return configData
  except:
    return None

def checkConfigData(configData):
  
  errors = []
  
  # Check if needed objects exist
  if('areaParameters' not in configData):
    errors.append('"Safety Areas" Object is missing.')
  if('typicalParameters' not in configData):
    errors.append('"Typicals Filter Parameters" Object is missing.')  
  if('indexParameters' not in configData):
    errors.append('"Index Parameters" Object is missing.')  
  if('processLibParameters' not in configData):
    errors.append('"ProcessLib Parameters" Object is missing.')  
  if(len(errors) > 0): return errors
  
  # Check if needed Typical keys exist
  for key in typicals:
    if key not in configData['typicalParameters']:
      errors.append('"'+key+'" key missing in "Typicals Filter Parameters".')
    if key not in configData['processLibParameters']:
      errors.append('"'+key+'" key missing in "ProcessLib Parameters".')
  if(len(errors) > 0): return errors
  
  # Collect warnings if Typical keys hold no value
  warnings = ['warnings']
  for key in configData['typicalParameters']:
    if key in typicals:
      if len(configData['typicalParameters'][key]) == 0:
        warnings.append('"'+key+'" key in "Typicals Filter Parameters" holds no filtering values.')
  if len(warnings) > 1: return warnings
  
  # Add default Safety Area value
  configData['areaParameters']['default'] = 'area01'
  
  # Subtract 1 from all ProcessLib keys for index computing
  for typical in configData['processLibParameters']:
    for key in configData['processLibParameters'][typical]:
      try:
        configData['processLibParameters'][typical][key] -= 1
      except: pass
  
  # Return empty array if no errors or warnings occured
  return []
