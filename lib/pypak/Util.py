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

def c_cont(arr):
  if not arr.flags['C_CONTIGUOUS']:
    return arr.copy(order='C')
  else:
    return arr
# end if

def f_cont(arr):
  if not arr.flags['F_CONTIGUOUS']:
    return arr.copy(order='F')
  else:
    return arr
# end if

