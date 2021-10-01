from psychopy import visual, core, event
from utils import (
  determin_probability, draw_pie_chart, drawBarChart,
)

NUM_BLOCKS = 2
TRIAL_PER_BLOCK = 30

BAR_CHART_X = 0.8
BAR_CHART_Y = -0.6
BAR_CHART_WIDTH = 0.15
BAR_CHART_HIGHT = 0.6

PIE_CHART_RADIOUS = 0.3
PIE_CHART_Y = 0.8
PIE_CHART_X = 0.0

INFOQUE_WIDTH = 1.0
INFOQUE_HIEGHT = 0.3
INFOQUE_POS = (0.0, 0.0)


class Trial:

  def __init__(self, wl_prob:float, show_prob1:float, show_prob2:float, share:bool, is_win:bool, hit:bool=None) -> None:
    self.wl_prob = wl_prob
    # if show_prob1 == show_prob2:
    #   raise ValueError('Wrong values for show probabilities. They cant be equal.')
    self.show_prob1 = show_prob1
    self.show_prob2 = show_prob2
    self.share = share
    self.is_win = is_win
    if hit is None:
      self.hit = determin_probability(self.wl_prob)
    else:
      self.hit = hit

  def showPieChart(self, win, duration:float=3.0):
    clock = core.Clock()
    while clock.getTime() < duration:
      draw_pie_chart(win, self.wl_prob, PIE_CHART_RADIOUS, (PIE_CHART_X, PIE_CHART_Y) )
      win.flip()

  def drawBarChart(self, win, side):
    x = 0.0
    if side == 'left':
      x -= BAR_CHART_X
      prob = self.show_prob1
    else:
      x += BAR_CHART_X
      prob = self.show_prob2
    pos = (x, BAR_CHART_Y)
    drawBarChart(win, prob, BAR_CHART_WIDTH, BAR_CHART_HIGHT, pos)

  def showBarChart(self, win, side, duration:float=3.0):
    clock = core.Clock()
    self.drawBarChart(win, side)
    win.flip()
    while clock.getTime() < duration:
      pass
  
  def showAllAskForChoice(self, win, duration:int=3):
    draw_pie_chart(win, self.wl_prob, PIE_CHART_RADIOUS, (PIE_CHART_X, PIE_CHART_Y))
    self.drawBarChart(win, 'left')
    self.drawBarChart(win, 'right')
    win.flip()
    clock = core.Clock()
    while clock.getTime() < duration:
      keys = event.getKeys()
      t = clock.getTime()
      if 'right' in keys and 'left' in keys:
        continue
      elif 'right' in keys:
        return (2, t)
      elif 'left' in keys:
        return (1, t)      
    return -1, -1
  
  

  def showInfoQue(self, win, sbjChoice, duration:float=3.0) -> bool:
    if sbjChoice == 1:
      prob = self.show_prob1
    else:
      prob = self.show_prob2
    if determin_probability(prob):
      ignorance = False
      color = 'green'
    else:
      ignorance = True
      color = 'red'
    rect = visual.Rect(win, INFOQUE_WIDTH, INFOQUE_HIEGHT, pos=INFOQUE_POS, fillColor=color)
    clock = core.Clock()
    rect.draw()
    win.flip()
    while clock.getTime() < duration:
      pass
    return ignorance

  def showResult(self, win, duration:float=3.0):
    if not self.hit:
      text = "ZERO"
    elif self.is_win:
      text = "WIN"
    else:
      text = "LOSE"
    stim = visual.TextStim(win, text)
    stim.draw()
    win.flip()
    clock = core.Clock()
    while clock.getTime() < duration:
      pass

  
  
