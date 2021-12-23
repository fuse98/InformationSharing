import random

from psychopy import clock, visual, event

from utils import read_subject, exit_exp
from experiment import Experiment

if __name__ == '__main__':

  random.seed(clock.Clock().getTime(False))

  subject = read_subject('subjects.csv')
  efficient_data = { key: subject[key] for key in ['id', 'age', 'sex'] }
  print(f'running experiment with {subject}')

  event.globalKeys.add(key='f', func=exit_exp)
  win = visual.Window(color='black', fullscr=True)
  win.setMouseVisible(False)
  
  experiment = Experiment(25, subject=efficient_data)
  experiment.create_blocks(sandbox=False)
  experiment.run(win)
