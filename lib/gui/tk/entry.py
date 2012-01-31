from Tkinter import *

### class
class captcha:
  def __init__(self,root):
    f = Frame(root)
    f.pack()
    self.entry = Entry(f)
    self.entry.pack(side=LEFT)
    self.entry.config(font=("Helvetica", 16, "bold"))
    print self.entry.keys()
  # end def

  def say_hi(self):
    print "hi there, everyone!"
  # end def
# end class
