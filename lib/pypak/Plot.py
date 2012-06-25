import matplotlib.pyplot as plt

def plot(data,col=1):
  x = data.transpose()[0]
  y = data.transpose()[col]
  plt.plot(x,y)
  plt.minorticks_on()
  plt.show()
# end def

def plot2(data1,data2,col=1):
  x1 = data1.transpose()[0]
  y1 = data1.transpose()[col]
  x2 = data2.transpose()[0]
  y2 = data2.transpose()[col]

  fig = plt.figure()
  plt.plot(x1,y1)
  plt.plot(x2,y2)

  plt.minorticks_on()
  plt.show()
# end def

