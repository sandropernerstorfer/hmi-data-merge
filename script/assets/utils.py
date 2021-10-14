from typing import Match


def printInfoBlock(text, color = '0'):
  
  l = len(text)
  if color == 'blue':     color = '94'
  elif color == 'red':      color = '91'
  elif color == 'yellow':   color = '93'
  elif color == 'green':    color = '92'
  elif color == 'cyan':     color = '96'
  
  print('-'+l*'-'+'-')
  print(' \033['+color+'m'+text+'\033[0m ')
  print('-'+l*'-'+'-')