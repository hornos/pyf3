
import wx

class captcha(wx.Frame):
  def __init__(self, parent, title = 'Captcha', image = None, size = (640,480)):
    wx.Frame.__init__(self, parent, title = title, size = size )
    self.entry = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER)
    self.Bind(wx.EVT_TEXT, self.onKeyPress, self.entry)
    self.Show(True)
  # end def

  def onKeyPress(self, event):
    print event.GetKeyCode()
  # end def
# end class