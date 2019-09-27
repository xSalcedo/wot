import os.path

def findp(name):
  if os.path.exists(name) == True:
    return True
  else: 
    return False
  

