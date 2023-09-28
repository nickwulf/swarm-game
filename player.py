import sys, math, random, time, pygame
import pygame.gfxdraw

# Import global variables and utilities
import globals as glob
import utilities as util

# Import user classes
from caravan import *

class Neutral:
  
  def __init__(self, color):
    self.color = color
  
  def update(self):
    return

  
class Human:
  
  def __init__(self, color=(255,255,255)):
    self.color = color
    self.unselectTimer = 10
    self.boxInitPos = None
    self.selectRect = None
  
  def update(self):
    self.unselectTimer += 1.0/glob.frameRate
    if not glob.userToGameInteractionDisabled:
      if glob.mouseLeftButtonClicked:
        if glob.mousedPlanet is None:
          self.boxInitPos = glob.mousePos
          self.calcSelectRect()
          if self.unselectTimer < .4:
            for p in glob.planetList:
              p.selected = False
          self.unselectTimer = 0
        elif glob.mousedPlanet.player == self:
          if glob.shiftHeld:
            glob.mousedPlanet.selected = not glob.mousedPlanet.selected
          else:
            selectedCount = 0
            for p in glob.planetList:
              if p.selected and p is not glob.mousedPlanet:
                selectedCount += 1
                p.selected = False
            if selectedCount == 0:
              glob.mousedPlanet.selected = not glob.mousedPlanet.selected
            else:
              glob.mousedPlanet.selected = True
      if glob.mouseLeftButtonUnclicked:
        if self.selectRect is not None:
          for p in glob.planetList:
            if not glob.shiftHeld:
              p.selected = False
            if p.player == self and self.selectRect.collidepoint(p.pos):
              p.selected = True
        self.boxInitPos = None
        self.selectRect = None
      if glob.mouseRightButtonClicked:
        if glob.mousedPlanet is not None:
          for p in glob.planetList:
            if p is glob.mousedPlanet:
              continue
            if p.player == self and p.selected:
              caravanPop = int(p.population/2)
              p.attack(glob.mousedPlanet, caravanPop)
      if glob.spacePressed:
        if glob.gameTimeStep == 1.0/glob.frameRate:
          glob.gameTimeStep = 0.1/glob.frameRate
        elif glob.gameTimeStep == 0.1/glob.frameRate:
          glob.gameTimeStep = 10.0/glob.frameRate
        else:
          glob.gameTimeStep = 1.0/glob.frameRate
    
    self.calcSelectRect()
      
  def calcSelectRect(self):
    if self.boxInitPos is None:
      self.selectRect = None
    else:
      leftX = min(self.boxInitPos[0], glob.mousePos[0])+1
      topY = min(self.boxInitPos[1], glob.mousePos[1])+1
      width = math.fabs(self.boxInitPos[0]-glob.mousePos[0])-2
      height = math.fabs(self.boxInitPos[1]-glob.mousePos[1])-2
      if (width > 0 and height > 0) or self.selectRect is not None:
        self.selectRect = pygame.Rect((leftX, topY), (width, height))


class AiStupid:

  def __init__(self, color=(255,255,255)):
    self.color = color
    self.actionPeriod = 5
    self.lastActionTimer = random.random() * 2.0
  
  def update(self):
    # Update timer to stop weirdness toward planets with no population
    self.lastActionTimer += glob.gameTimeStep
    if self.lastActionTimer >= self.actionPeriod:
    # Find owned planet with highest population
      self.lastActionTimer = random.random() * 2.0
      mostPopPlanet = None
      for p in glob.planetList:
        if p.player is self:
          if mostPopPlanet is None:
            mostPopPlanet = p
          if p.population > mostPopPlanet.population:
            mostPopPlanet = p
      if mostPopPlanet is None:
        return
      # Find planet with lowest population (add some noise)
      scoreList = []
      for p in glob.planetList:
        scoreList.append(-p.population)
      targetPlanet = glob.planetList[util.decide(scoreList, 20)]
      if targetPlanet.player is self:
        mostPopPlanet.attack(targetPlanet, (mostPopPlanet.population-targetPlanet.population)/2)
      elif mostPopPlanet.population-2 > targetPlanet.population:
        mostPopPlanet.attack(targetPlanet, (mostPopPlanet.population+targetPlanet.population)/2)
      
      
class AiStupid2:

  def __init__(self, color=(255,255,255)):
    self.color = color
    self.actionPeriod = 5
    self.lastActionTimer = random.random() * 2.0
  
  def update(self):
    # Update timer to stop weirdness toward planets with no population
    self.lastActionTimer += glob.gameTimeStep
    if self.lastActionTimer >= self.actionPeriod:
    # Find owned planet with highest population
      self.lastActionTimer = random.random() * 2.0
      mostPopPlanet = None
      for p in glob.planetList:
        if p.player is self:
          if mostPopPlanet is None:
            mostPopPlanet = p
          if p.population > mostPopPlanet.population:
            mostPopPlanet = p
      if mostPopPlanet is None:
        return
      # Find planet with lowest population (add some noise)
      scoreList = []
      for p in glob.planetList:
        scoreList.append(-p.population)
      targetPlanet = glob.planetList[util.decide(scoreList, 20)]
      if targetPlanet.player is self:
        mostPopPlanet.attack(targetPlanet, (mostPopPlanet.population-targetPlanet.population)/2)
      elif mostPopPlanet.population-2 > targetPlanet.population:
        mostPopPlanet.attack(targetPlanet, (mostPopPlanet.population+targetPlanet.population)/2)
      

class AiDumb:

  def __init__(self, color=(255,255,255)):
    self.color = color
    self.actionPeriod = 5
    self.lastActionTimer = random.random() * 2.0
  
  def update(self):
    # Update timer to stop weirdness toward planets with no population
    self.lastActionTimer += glob.gameTimeStep
    if self.lastActionTimer >= self.actionPeriod:
    # Find owned planet with highest population
      self.lastActionTimer = random.random() * 2.0
      mostPopPlanet = None
      for p in glob.planetList:
        if p.player is self:
          if mostPopPlanet is None:
            mostPopPlanet = p
          if p.population > mostPopPlanet.population:
            mostPopPlanet = p
      if mostPopPlanet is None:
        return
      # Find planet with lowest population (add some noise)
      scoreList = []
      for p in glob.planetList:
        score = -p.population
        if isinstance(p.player, Neutral):
          score *= 2
        score += p.growthRate*10
        distance = math.sqrt((mostPopPlanet.pos[0]-p.pos[0])**2 + (mostPopPlanet.pos[1]-p.pos[1])**2)
        score -= distance/50
        scoreList.append(score)
      targetPlanet = glob.planetList[util.decide(scoreList, 10)]
      if targetPlanet.player is self:
        mostPopPlanet.attack(targetPlanet, (mostPopPlanet.population-targetPlanet.population)/2)
      elif mostPopPlanet.population-2 > targetPlanet.population:
        mostPopPlanet.attack(targetPlanet, (mostPopPlanet.population+targetPlanet.population)/2)


class AiDumb2:

  def __init__(self, color=(255,255,255)):
    self.color = color
    self.actionPeriod = 4
    self.lastActionTimer = random.random() * 2.0
  
  def update(self):
    # Update timer to stop weirdness toward planets with no population
    self.lastActionTimer += glob.gameTimeStep
    if self.lastActionTimer >= self.actionPeriod:
    # Find owned planet with highest population
      self.lastActionTimer = random.random() * 2.0
      mostPopPlanet = None
      for p in glob.planetList:
        if p.player is self:
          if mostPopPlanet is None:
            mostPopPlanet = p
          if p.population > mostPopPlanet.population:
            mostPopPlanet = p
      if mostPopPlanet is None:
        return
      # Find planet with lowest population (add some noise)
      scoreList = []
      for p in glob.planetList:
        score = -p.population
        if isinstance(p.player, Neutral):
          score *= 2
        score += p.growthRate*10
        distance = math.sqrt((mostPopPlanet.pos[0]-p.pos[0])**2 + (mostPopPlanet.pos[1]-p.pos[1])**2)
        score -= distance/50
        scoreList.append(score)
      targetPlanet = glob.planetList[util.decide(scoreList, 10)]
      if targetPlanet.player is self:
        mostPopPlanet.attack(targetPlanet, (mostPopPlanet.population-targetPlanet.population)/2)
      elif mostPopPlanet.population-2 > targetPlanet.population:
        mostPopPlanet.attack(targetPlanet, (mostPopPlanet.population+targetPlanet.population)/2)
      