def getAllWithPid(pid, master_ws):
  
  from assets.database import firstRow, pidColumn
  
  try: pid = int(pid)
  except: pid = pid
  
  elements = []
  for key, *values in master_ws.iter_rows(min_row = firstRow):
    if(key.value == None):
      break

    if(values[pidColumn-2].value == pid):
      row = [None,None] + [v.value for v in values]     # [None, None] is just added for easier indexing when filtering
      elements.append(row)
  
  return elements

def convertControllerToInput(type):
  try:
    type = type.strip()
  finally:
    if(len(type) == 2 and type[-1] == 'C'):
      t = list(type)
      t[-1] = 'I'
      type = ''.join(t)
  return type