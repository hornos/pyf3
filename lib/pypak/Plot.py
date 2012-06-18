import matplotlib.pyplot as plt

def plot(data,col=1):
  x = data.transpose()[0]
  y = data.transpose()[col]
  plt.plot(x,y)
  plt.show()
# end def

