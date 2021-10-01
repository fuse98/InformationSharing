from psychopy import visual, core, event
import random


def determin_probability(prob:float) -> bool:
  i = random.randint(0, 10) / 10
  return i <= prob

def show_text_and_ask_for_continue(win, text:str, duration:int):
  clock = core.Clock()
  stim = visual.TextStim(win, text)
  stim.autoDraw = True
  while clock.getTime() < duration:
    win.flip()
  stim.text = "please press SPACE to continue"
  keyPressed = False
  while not keyPressed:
    win.flip()
    for key in event.waitKeys():
      if key == 'space':
        keyPressed = True
  stim.autoDraw = False

def draw_pie_chart(win, prob:float, radious:float, pos:tuple, angleOffset=2.5):
  angle = 360 * prob
  rad1 = visual.RadialStim( win=win, name='rad1', color=[1,-1,-1],
  angularCycles = 0, radialCycles = 0, radialPhase = 0.5, colorSpace = 'rgb', 
  ori= 0.0, pos=pos, size=(radious, radious),  visibleWedge=(0.0, 360.0) )
  rad2 = visual.RadialStim( win=win, name='rad1', color=[-1,1,-1],
  angularCycles = 0, radialCycles = 0, radialPhase = 0.5, colorSpace = 'rgb', 
  ori=0.0, pos=pos, size=(radious, radious),  visibleWedge=(0.0, angle + angleOffset) )
  rad1.draw()
  rad2.draw()

def drawBarChart(win, prob:float, width:float, hight:float, pos:tuple):
  rect1 = visual.Rect(win, width, hight, pos=pos, lineColor='black')
  fillHeight = prob * hight
  hightOffset = (hight - fillHeight) / 2
  fillPos = (pos[0], pos[1] - hightOffset)
  rect2 = visual.Rect(win, width, fillHeight, pos=fillPos, fillColor='blue')
  rect1.draw()
  rect2.draw()

def random_probability():
  return random.randint(1, 9) / 10
