import sys, math, random, time, pygame
import pygame.gfxdraw

# Import global variables and utilities
import globals as glob
import utilities as util

# Import user classes
from player import *
from caravan import *

class Planet:

  def __init__(self, pos, size, population, player):
    self.pos = pos
    self.size = size
    self.population = population
    self.player = player
    self.selected = False
    self.growthRate = self.size**2.0/2500
  
  def update(self):
    if not isinstance(self.player, Neutral):
      self.population += glob.gameTimeStep * self.growthRate
    
  def drawBack(self):
    # Draw selected aura and line
    if self.selected:
      period = 2
      timeStep = time.clock() % period
      alpha = -(timeStep * (timeStep-period))*4/period**2
      alpha = .2 + .8*alpha
      pygame.gfxdraw.filled_ellipse(glob.windowSurface, self.pos[0], self.pos[1], int(self.size+10*alpha), 1+int(self.size+10*alpha), util.colorFade(self.player.color,alpha*.5))
      if glob.mousedPlanet is None:
        pygame.draw.aaline(glob.windowSurface, self.player.color, self.pos, glob.mousePos, True)
      else:
        pygame.draw.aaline(glob.windowSurface, self.player.color, self.pos, glob.mousedPlanet.pos, True)
      
  def draw(self):
    # Draw base planet
    pygame.gfxdraw.filled_circle(glob.windowSurface, self.pos[0], self.pos[1], self.size, self.player.color)
    pygame.gfxdraw.aacircle(glob.windowSurface, self.pos[0], self.pos[1], self.size, (0,0,0))
    util.drawText(int(self.population), self.pos)
    
    # Draw selectable indicator
    if self.isMouseOver():
      radLarge = self.size+12
      radSmall = self.size+6
      pygame.gfxdraw.circle(glob.windowSurface, self.pos[0], self.pos[1], radLarge, (96,96,96))
      pygame.gfxdraw.line(glob.windowSurface, self.pos[0], self.pos[1]+radSmall, self.pos[0], self.pos[1]+radLarge, (96,96,96))
      pygame.gfxdraw.line(glob.windowSurface, self.pos[0], self.pos[1]-radSmall, self.pos[0], self.pos[1]-radLarge, (96,96,96))
      pygame.gfxdraw.line(glob.windowSurface, self.pos[0]+radSmall, self.pos[1], self.pos[0]+radLarge, self.pos[1], (96,96,96))
      pygame.gfxdraw.line(glob.windowSurface, self.pos[0]-radSmall, self.pos[1], self.pos[0]-radLarge, self.pos[1], (96,96,96))
      
  def isMouseOver(self):
    sqDist = (self.pos[0]-glob.mousePos[0])**2 + (self.pos[1]-glob.mousePos[1])**2
    if sqDist < self.size**2:
      return True
    
  def attack(self, planet, population):
    population = int(population)
    if population > self.population:
      population = int(self.population)
    if population <= 0:
      return
    self.population -= population
    glob.caravanList.append(Caravan(self,planet,population))
    