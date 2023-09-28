import sys, math, random, time, pygame
import pygame.gfxdraw

# Import global variables and utilities
import globals as glob
import utilities as util

# Import user classes
from player import *
from caravan import *
from laser import *

class Planet:

  def __init__(self, pos, size, population, player):
    self.pos = pos
    self.drawPos = self.pos[0]-glob.winPos[0], self.pos[1]-glob.winPos[1]
    self.size = size
    self.population = population
    self.player = player
    self.selected = False
    self.growthRate = self.size**2.0/2500
    self.maxPop = round(self.growthRate*60)
    self.weapons = []
  
  def update(self):
    growth = self.calcGrowthRate() * glob.gameTimeStep
    if math.fabs(growth) > math.fabs(self.maxPop-self.population):
      self.population = self.maxPop
    else:
      self.population += growth
    self.drawPos = self.pos[0]-glob.winPos[0], self.pos[1]-glob.winPos[1]
    
  def drawBack(self):
    # Draw selected aura and line
    if self.selected:
      period = 2
      timeStep = time.perf_counter() % period
      alpha = -(timeStep * (timeStep-period))*4/period**2
      alpha = .2 + .8*alpha
      pygame.gfxdraw.filled_ellipse(glob.windowSurface, self.drawPos[0], self.drawPos[1], int(self.size+10*alpha), 1+int(self.size+10*alpha), util.colorFade(self.player.color,alpha*.5))
      if glob.userPlayer.selectRect is None:
        if glob.mousedPlanet is None:
          pygame.draw.aaline(glob.windowSurface, self.player.color, self.drawPos, glob.mouseDrawPos, True)
        else:
          pygame.draw.aaline(glob.windowSurface, self.player.color, self.drawPos, glob.mousedPlanet.drawPos, True)
      
  def draw(self):
    for w in self.weapons:
      w.draw()
    
    # Draw base planet
    pygame.gfxdraw.filled_circle(glob.windowSurface, self.drawPos[0], self.drawPos[1], int(self.size), self.player.color)
    if not isinstance(self.player, Neutral):
      barThickness = 5
      if self.population/self.maxPop >= 0.75:
        barThickness = 10-10*math.fabs((time.perf_counter() % 1)-.5)
      util.drawPie(glob.windowSurface, self.drawPos, int(self.size), 270-180*(self.population/self.maxPop), 270+180*(self.population/self.maxPop), util.combineColors((255,255,255), self.player.color, .5))
      pygame.gfxdraw.filled_circle(glob.windowSurface, self.drawPos[0], self.drawPos[1], int(self.size-barThickness), self.player.color)
      pygame.gfxdraw.aacircle(glob.windowSurface, self.drawPos[0], self.drawPos[1], int(self.size-barThickness), self.player.color)
      if self.population/self.maxPop > 1:
        extraBar = 1-math.exp(-math.log(2.0)*(self.population/self.maxPop-1))
        util.drawPie(glob.windowSurface, self.drawPos, int(self.size), 90-180*extraBar, 90+180*extraBar, util.combineColors((255,255,255), self.player.color, barThickness/10))
        extraBarThickness = 10
        pygame.gfxdraw.filled_circle(glob.windowSurface, self.drawPos[0], self.drawPos[1], int(self.size-extraBarThickness), self.player.color)
        pygame.gfxdraw.aacircle(glob.windowSurface, self.drawPos[0], self.drawPos[1], int(self.size-extraBarThickness), self.player.color)
    pygame.gfxdraw.aacircle(glob.windowSurface, self.drawPos[0], self.drawPos[1], int(self.size), (0,0,0))
    util.drawText(int(self.population), self.drawPos)
    
    # Draw selectable indicator
    if not glob.userToGameInteractionDisabled:
      if self.isMouseOver() and glob.userPlayer.selectRect is None:
        self.drawSelectableIndicator()
      if glob.userPlayer.selectRect is not None and glob.userPlayer.selectRect.collidepoint(self.pos) and self.player == glob.userPlayer:
        self.drawSelectableIndicator()
        
  def drawSelectableIndicator(self):
    radLarge = int(self.size)+12
    radSmall = int(self.size)+6
    pygame.gfxdraw.circle(glob.windowSurface, self.drawPos[0], self.drawPos[1], radLarge, (96,96,96))
    pygame.gfxdraw.line(glob.windowSurface, self.drawPos[0], self.drawPos[1]+radSmall, self.drawPos[0], self.drawPos[1]+radLarge, (96,96,96))
    pygame.gfxdraw.line(glob.windowSurface, self.drawPos[0], self.drawPos[1]-radSmall, self.drawPos[0], self.drawPos[1]-radLarge, (96,96,96))
    pygame.gfxdraw.line(glob.windowSurface, self.drawPos[0]+radSmall, self.drawPos[1], self.drawPos[0]+radLarge, self.drawPos[1], (96,96,96))
    pygame.gfxdraw.line(glob.windowSurface, self.drawPos[0]-radSmall, self.drawPos[1], self.drawPos[0]-radLarge, self.drawPos[1], (96,96,96))
  
  def isMouseOver(self):
    sqDist = (self.pos[0]-glob.mousePos[0])**2 + (self.pos[1]-glob.mousePos[1])**2
    if sqDist < self.size**2:
      return True
  
  def calcGrowthRate(self):
    growth = 0.0
    if not isinstance(self.player, Neutral):
      if self.population < self.maxPop:
        growth += 0.5 * self.growthRate
        if self.population < self.maxPop*0.75:
          # Growthrate is halved when population exceeds 75% of maxPop
          growth += 0.5 * self.growthRate
      elif self.population > self.maxPop:
        # Reduce population by 50% of growthrate for every 10% excess of maxPop
        growth -= self.growthRate * 0.5*math.ceil(10.0*(self.population/self.maxPop - 1.0))
    return growth
    
  def attack(self, planet, population):
    population = int(population)
    if population > self.population:
      population = int(self.population)
    if population <= 0:
      return
    self.population -= population
    glob.caravanList.append(Caravan(self,planet,population))
    
  def addLaser(self, power, range, speed):
    self.weapons.append(Laser(self, power, range, speed))
    
  def changePlayer(self, player):
    self.player = player
    for w in self.weapons:
      w.updateChanges()
    