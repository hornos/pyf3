import pickle

def save(obj,fn):
  fp=open(fn + ".dump", "w+")
  pickle.dump(obj,fp)
  fp.close()
# end def

def load(fn):
  fp=open(fn + ".dump", "r")
  obj=pickle.load(fp)
  fp.close()
  return obj
# end def
