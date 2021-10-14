from psychopy import data
import os
import random

from utils import (
  show_text_and_ask_for_continue,
  show_block_introduction,
  random_probability,
  two_probabilities
  )

from trial import Trial


class Experiment:

  def __init__(self, numTrials:int, subject:dict={}) -> None:
      self.numTrials = numTrials
      self.blocks = []
      self.extraInfo = subject
      colors = ['orange', 'magenta']
      random.shuffle(colors)
      self.win_color = colors[0]
      self.lose_color = colors[1]

  def __iter__(self):
    for block in self.blocks:
      yield block

  def create_blocks(self, sandbox:bool=False):
    id = int(self.extraInfo['id'])
    if sandbox:
      block = self.createBlock(True, True)
      self.blocks.append(block)
      return
    
    first_isGain = id % 2 == 0
    second_isGain = id % 2 == 1
    first_isShare = id % 4 == 0 or id % 4 == 1
    second_isShare = id % 4 == 2 or id % 4 == 3

    self.blocks.append(self.createBlock(first_isGain, first_isShare))
    self.blocks.append(self.createBlock(second_isGain, first_isShare))
    self.blocks.append(self.createBlock(first_isGain, first_isShare))
    self.blocks.append(self.createBlock(second_isGain, first_isShare))

    self.blocks.append(self.createBlock(first_isGain, second_isShare))
    self.blocks.append(self.createBlock(second_isGain, second_isShare))
    self.blocks.append(self.createBlock(first_isGain, second_isShare))
    self.blocks.append(self.createBlock(second_isGain, second_isShare))
  
  def addBlock(self, block:data.TrialHandler):
    self.blocks.append(block)

  def createBlock(self, isGain, isShare:int) -> data.TrialHandler:
    '''
      creates a TrialHandler with 'numTrials'
      trials of type isShare, isGain. if isShare is True
      50% of trials will have other_estimation set True
    '''
    trials = []
    for i in range(self.numTrials):
      pL, pR = two_probabilities()
      trials.append(Trial(random_probability(),
       pL, pR, isShare, isGain, False))

    numOtherEstimation = 0
    if isShare:
      numOtherEstimation = int(numOtherEstimation/2)

    for i in range(numOtherEstimation):
      trials[i].other_estimation = True

    trials = [t.__dict__ for t in trials]
    trialExtraInfo = {
      **self.extraInfo,
      'isGain': isGain,
      'isOther': isShare,
      'num_other_estimation': numOtherEstimation,
      'lose_color': self.lose_color,
      'win_color': self.win_color,
    }
    return data.TrialHandler(trials, nReps=1, method='random', extraInfo=trialExtraInfo)

  def saveResultsInCsv(self, directory:str) -> None:
    if not os.path.isdir(directory):
      os.mkdir(directory)
    for i in range(len(self.blocks)):
      self.blocks[i].saveAsWideText(f"{directory}/{self.extraInfo['id']}_{i}.csv", ',')

  def get_hit_color(self, isGain):
    if isGain:
      return self.win_color
    return self.lose_color


  def run(self, win):
    for block in self:

      show_block_introduction(win, block)

      for trialData in block:
        trial = Trial(**trialData)
        trial.showStartFixation(win, 1)
        trial.showPieChart(win, self.get_hit_color(trial.isGain), 3.0)

        if trial.share:
          trial.showResult(win)        
          estimation, slider_time = trial.askForSelfOtherEmpathyEstimation(win)
          block.addData('estimatio', estimation)
          block.addData('sliderResponseTime', slider_time)

        trial.showBarChart(win, 'left', 3.0)
        trial.showBarChart(win, 'right', 3.0)
        subjectChoice, respTime = trial.showAllAskForChoice(win, self.get_hit_color(trial.isGain))
        block.addData('sbjChoice', subjectChoice)
        block.addData('respTime', respTime)

        if subjectChoice is None:
          show_text_and_ask_for_continue(win, 'شما به موقع جواب ندادید. پاسخ شما ثبت نشد', random.randint(3, 7))
        else:
          saw_result = trial.showInfoQue(win, subjectChoice)
          block.addData('sawResult', saw_result)
          trial.showResult(win, 3, saw_result)

    self.saveResultsInCsv('results')


