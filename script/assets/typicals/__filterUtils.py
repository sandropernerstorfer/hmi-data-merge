def getAllWithPid(pid, master_ws):
  
  try: pid = int(pid)
  except: pid = pid
  
  firstRow  = 8
  pidCol    = 3
  
  elements = []
  
  for key, *values in master_ws.iter_rows(min_row = firstRow):
    if(key.value == None):  # Stop if row A has no value
      break

    if(values[pidCol-2].value == pid):  # Find row with defined PID
      row = [v.value for v in values]
      elements.append(row)
  
  return elements