def printInfoBlock(text):
  l = len(text) + 1
  print('-'+l*'-'+'-')
  print(' \033[2;34;40m'+text+'\033[0m ')
  print('-'+l*'-'+'-')