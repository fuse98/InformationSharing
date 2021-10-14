from random import randint
from psychopy import visual, core, event
from utils import (
  determin_probability, draw_pie_chart, drawBarChart,
  createSlider
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

SLIDER_POS = (0.0, 0.0)
SLIDER_SIZE = [1.7, 0.06]

SLIDER_GUIDE_MESSAGE = 'با فشردن کلید SPACE نتیجه را ثبت کنید'

class Trial:

  def __init__(
      self, wl_prob:float, show_probL:float,
      show_probR:float, share:bool, isGain:bool, other_estimation:bool,
      hit:bool=None,
    ) -> None:
    self.wl_prob = wl_prob
    # if show_probL == show_probR:
    #   raise ValueError('Wrong values for show probabilities. They cant be equal.')
    self.show_probL = show_probL
    self.show_probR = show_probR
    self.share = share
    self.isGain = isGain
    if hit is None:
      self.hit = determin_probability(self.wl_prob)
    else:
      self.hit = hit
    self.other_estimation = other_estimation

  def showStartFixation(self, win, duration:int=1):
    stem = visual.TextStim(win, '+')
    stem.draw()
    win.flip()
    clock = core.Clock()
    while clock.getTime() < duration:
      pass

  def showPieChart(self, win, hit_color:str, duration:float=3.0):
    self.believability_que(win)
    clock = core.Clock()
    draw_pie_chart(win, self.wl_prob, PIE_CHART_RADIOUS, (PIE_CHART_X, PIE_CHART_Y), hit_color=hit_color)
    win.flip()
    while clock.getTime() < duration:
      pass

  def drawBarChart(self, win, side):
    x = 0.0
    if side == 'left':
      x -= BAR_CHART_X
      prob = self.show_probL
    else:
      x += BAR_CHART_X
      prob = self.show_probR
    pos = (x, BAR_CHART_Y)
    drawBarChart(win, prob, BAR_CHART_WIDTH, BAR_CHART_HIGHT, pos)

  def showBarChart(self, win, side, duration:float=3.0):
    self.believability_que(win)
    clock = core.Clock()
    self.drawBarChart(win, side)
    win.flip()
    while clock.getTime() < duration:
      pass
  
  def believability_que(self, win):
    text = f'لاتاری یک شرکت کننده دیگر'
    if self.share:
      stim = visual.TextStim(win, text, font='Arial', languageStyle='Arabic', pos=(-0.65, 0.8))
      stim.draw()

  def showAllAskForChoice(self, win, hit_color:str, duration:int=3):
    self.believability_que(win)    
    draw_pie_chart(win, self.wl_prob, PIE_CHART_RADIOUS, (PIE_CHART_X, PIE_CHART_Y), hit_color=hit_color)
    self.drawBarChart(win, 'left')
    self.drawBarChart(win, 'right')
    win.flip()
    clock = core.Clock()
    event.clearEvents()
    while clock.getTime() < duration:
      keys = event.getKeys()
      t = clock.getTime()
      if 'right' in keys and 'left' in keys:
        continue
      elif 'right' in keys:
        return ('r', t)
      elif 'left' in keys:
        return ('l', t)      
    return None, -1

  def showInfoQue(self, win, sbjChoice, duration:float=3.0) -> bool:
    if sbjChoice == 'l':
      prob = self.show_probL
    elif sbjChoice == 'r':
      prob = self.show_probR
    if determin_probability(prob):
      saw_result = True
      text = 'مشاهده نتیجه'
      # color = 'green'
    else:
      saw_result = False
      text = 'عدم مشاهده نتیجه'
      # color = 'red'
    # rect = visual.Rect(win, INFOQUE_WIDTH, INFOQUE_HIEGHT, pos=INFOQUE_POS, fillColor=color)
    stim = visual.TextStim(win, text, font='Arial', languageStyle='Arabic')
    clock = core.Clock()
    # rect.draw()
    stim.draw()
    win.flip()
    while clock.getTime() < duration:
      pass
    return saw_result

  def showResult(self, win, duration:float=3.0, saw_result:bool=True):
    if not self.hit:
      text = "پوچ"
    elif self.isGain:
      text = "برد"
    else:
      text = "باخت"
    if not saw_result:
      text = '----'
    stim = visual.TextStim(win, text, font='Arial', languageStyle='Arabic')
    stim.draw()
    win.flip()
    clock = core.Clock()
    while clock.getTime() < duration:
      pass

  def estimationMessage(self, win):
    if self.other_estimation:
      line1 = 'فکر میکنید پس از انتقال نتیجه به فرد مقابل\n چه احساسی داشته باشید؟'
      line2 = 'احساس شما'
    else:
      line1 = 'فکر میکنید فرد مقابل پس از فهمیدن نتیجه\n چه احساسی داشته باشد؟'
      line2 = 'احساس فرد مقابل'
    labelR = 'خیلی خوب'
    labelL = 'خیلی بد'
    stim_line1 = visual.TextStim(win, line1,
     font='Arial', languageStyle='Arabic', pos=(0.0, 0.8))
    stim_line2 = visual.TextStim(win, line2,
     font='Arial', languageStyle='Arabic', pos=(0.0, -0.8))
    stim_labelL = visual.TextStim(win, labelL,
     font='Arial', languageStyle='Arabic', pos=(-0.8, -0.1))
    stim_lableR = visual.TextStim(win, labelR,
     font="Arial", languageStyle='Arabic', pos=(0.8, -0.1))
    stim_line1.draw()
    stim_line2.draw()
    stim_labelL.draw()
    stim_lableR.draw()

  def askForSelfOtherEmpathyEstimation(self, win):
    keyPressed = False
    mouse = event.Mouse(win=win)
    clock = core.Clock()
    ticks = [ i for i in range(-100, 100)]
    startValue = randint(-40, 40)
    slider = createSlider(win, ticks, startValue, SLIDER_POS, SLIDER_SIZE)
    event.clearEvents()
    while not keyPressed:
      pos = slider.getMarkerPos()
      pos += int(mouse.getWheelRel()[1])
      slider.markerPos = pos
      slider.draw()
      self.estimationMessage(win)
      win.flip()
      for key in event.getKeys():
        if key == 'space':
          keyPressed = True
    return (slider.getMarkerPos(), clock.getTime())
