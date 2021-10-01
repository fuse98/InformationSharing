from psychopy import visual

from experiment import Experiment
from trial import Trial
from utils import show_text_and_ask_for_continue


if __name__ == '__main__':

  win = visual.Window([800, 800])  
  experiment = Experiment(2, subject={'id': 123})
  block1 = experiment.createBlock(True, 0)
  block2 = experiment.createBlock(False, 2)
  experiment.addBlock(block1)
  experiment.addBlock(block2)
  
  for block in experiment:
    for trialData in block:
      trial = Trial(**trialData)
      trial.showPieChart(win, 1.0)
      # trial.showResult(win)
      trial.showBarChart(win, 'left', 1.0)
      trial.showBarChart(win, 'right', 1.0)
      subjectChoice, respTime = trial.showAllAskForChoice(win)
      block.addData('sbjChoice', subjectChoice)
      block.addData('respTime', respTime)
      if subjectChoice == -1:
        show_text_and_ask_for_continue(win, 'You were to late, your answer willnot be counted', 5)
      else:
        ignoranceQue = trial.showInfoQue(win, subjectChoice)
        block.addData('ignoranceQue', int(ignoranceQue))
        if not ignoranceQue:
          trial.showResult(win)

  experiment.saveResultsInCsv('results')

