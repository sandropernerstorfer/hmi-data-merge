def getAllWithPid(pid, master_ws):
  
  from assets.database import firstRow, pidColumn
  
  try: pid = int(pid)
  except: pid = pid
  
  elements = []
  for key, *values in master_ws.iter_rows(min_row = firstRow):
    if(key.value == None):
      break

    if(values[pidColumn-2].value == pid):
      row = [v.value for v in values]
      elements.append(row)
  
  return elements