import random
import csv
from psychopy import visual, core, event


def determin_probability(prob:float) -> bool:
  i = random.randint(0, 10) / 10
  return i <= prob

def show_text_and_ask_for_continue(win, text:str, duration:int):
  clock = core.Clock()
  stim = visual.TextStim(win, text, font='Arial', languageStyle='Arabic')
  stim.autoDraw = True
  while clock.getTime() < duration:
    win.flip()
  stim.text = "لطفا با فشردن SPACE ادامه دهید."
  keyPressed = False
  while not keyPressed:
    win.flip()
    for key in event.waitKeys():
      if key == 'space':
        keyPressed = True
  stim.autoDraw = False

def draw_pie_chart(win, prob:float, radious:float, pos:tuple, angleOffset=2.5, hit_color:str='gray'):
  angle = 360 * prob
  rad1 = visual.RadialStim( win=win, name='rad1', color='gray',
    angularCycles = 0, radialCycles = 0, radialPhase = 0.5, 
    ori= 0.0, pos=pos, size=(radious, radious),  visibleWedge=(0.0, 360.0) )
  rad2 = visual.RadialStim(win=win, name='rad2', color=hit_color,
    angularCycles=0, radialCycles=0, radialPhase=0.5, 
    ori=0.0, pos=pos, size=(radious, radious),  visibleWedge=(0.0, angle + angleOffset) )
  rad1.draw()
  rad2.draw()

def drawBarChart(win, prob:float, width:float, hight:float, pos:tuple):
  rect1 = visual.Rect(win, width, hight, pos=pos, lineColor='gray')
  fillHeight = prob * hight
  hightOffset = (hight - fillHeight) / 2
  fillPos = (pos[0], pos[1] - hightOffset)
  rect2 = visual.Rect(win, width, fillHeight, pos=fillPos, fillColor='blue')
  rect1.draw()
  rect2.draw()

def random_probability():
  return random.randint(1, 9) / 10


def show_block_introduction(win, block):

  if block.extraInfo['isGain']:
    block_type = 'برد'
    hit_color = block.extraInfo['win_color']
  else:
    block_type = 'باخت'
    hit_color = block.extraInfo['lose_color']
  
  if not block.extraInfo['isOther']:
    believability_text = 'برای شماست نتیجه‌ای که مشاهده خواهید کرد تصمیم فرد قبلی انتخاب شما برای ۱۰ لاتاری بی تاثیر است و\n'
    believability_text = 'انتخاب شما در ۱۰ لاتاری بی تاثیر است\nنتیجه‌‌ای که مشاهده خواهید کرد، تصمیم فرد قبلی\n برای شماست'
  else:
    believability_text = 'لاتاری‌های پیش رو برای فرد دیگری هستند\n انتخاب شما برای اوست.'
  believability_que = visual.TextStim(win, believability_text, pos=(0.0, -0.4), font='Arial', languageStyle='Arabic')
  believability_que.draw()

  text = f'آیتمهای پیش رو از جنس {block_type} خواهند بود'
  stim = visual.TextStim(win, text, pos=(0, 0.6), font='Arial', languageStyle='Arabic')
  color1_lable = visual.TextStim(win, 'رنگ احتمال ' + block_type, pos=(0.4, 0.2), font='Arial', languageStyle='Arabic')
  color1 = visual.Rect(win, 0.2, 0.15, pos=(0.4, 0.0), fillColor=hit_color)
  color2_lable = visual.TextStim(win, 'رنگ احتمال پوچ', pos=(-0.4, 0.2), font='Arial', languageStyle='Arabic')
  color2 = visual.Rect(win, 0.2, 0.15, pos=(-0.4, 0.0), fillColor='gray')
  color1.draw()
  color1_lable.draw()
  color2.draw()
  color2_lable.draw()
  stim.autoDraw = True
  continue_stim = visual.TextStim(win, "برای ادامه کلید SPACE را فشار دهید.", pos=(0, -0.7), font='Arial', languageStyle='Arabic')
  continue_stim.draw()
  keyPressed = False
  win.flip()
  while not keyPressed:
    for key in event.waitKeys():
      if key == 'space':
        keyPressed = True
  stim.autoDraw = False


def createSlider(win, ticks:list, startValue:int, pos, size):
  slider = visual.Slider(win, ticks=ticks, pos=pos, styleTweaks=['triangleMarker'], borderColor='blue', size=size)
  slider.setMarkerPos(startValue)
  return slider

def createWeightedList(num, weight):
  return [num for _ in range(weight)]

def two_probabilities():
  p1 = random.randint(0, 10) / 10
  p2_options = [ createWeightedList(p1 - i/10, abs(i) + 4) for i in range(-10, 11) if i != 0 and p1 - i/10 >= 0 and p1 - i/10 <= 1]
  p2_options = [ p for ps in p2_options for p in ps]
  p2 = random.sample(p2_options, 1)[0]
  res = [p1, p2]
  random.shuffle(res)
  return res


def read_subject(input_file:str, ) -> dict:
  lis = list(csv.reader(open(input_file)))
  title_row = lis[0]
  data_row = lis[-1]
  subject = {}
  for title, data in zip(title_row, data_row):
    subject[title] = data
  return subject

def exit_exp():
  exit()

