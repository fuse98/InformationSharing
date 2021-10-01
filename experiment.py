from psychopy import data
import os

from utils import random_probability
from trial import Trial

class Experiment:

  def __init__(self, numTrials:int, subject:dict={}) -> None:
      self.numTrials = numTrials
      self.blocks = []
      self.subject = subject

  def __iter__(self):
    for block in self.blocks:
      yield block

  def addBlock(self, block:data.TrialHandler):
    self.blocks.append(block)

  def createBlock(self, is_win, numShare:int) -> data.TrialHandler:
    '''
      creates a TrialHandler with 'numShare' trials with share status and
      experimnet.numTrials 'is_win' trials in total  
    '''
    if numShare > self.numTrials:
      raise ValueError(f'cant have {numShare} share trials in {self.numTrials} trial block.')
    trials = []
    for i in range(self.numTrials):
      trials.append(Trial(random_probability(),
       random_probability(), random_probability(), False, is_win))
    for i in range(numShare):
      trials[i].share = True
    trials = [t.__dict__ for t in trials]
    return data.TrialHandler(trials, nReps=1, method='random', extraInfo=self.subject)

  def saveResultsInCsv(self, directory:str) -> None:
    if not os.path.isdir(directory):
      os.mkdir(directory)
    for i in range(len(self.blocks)):
      self.blocks[i].saveAsWideText(f"{directory}/{self.subject['id']}_{i}.csv", ',')
