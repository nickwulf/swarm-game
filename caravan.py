import sys, math, random, time, pygame
import pygame.gfxdraw

# Import global variables and utilities
import globals as glob
import utilities as util

class Caravan:
  
  def __init__(self, originPlanet, destPlanet, population):
    self.originPlanet = originPlanet
    self.player = originPlanet.player
    self.destPlanet = destPlanet
    self.population = population
    self.pos = originPlanet.pos
    self.dir = self.destPlanet.pos[0]-self.pos[0], self.destPlanet.pos[1]-self.pos[1]
    distance = math.sqrt(self.dir[0]**2 + self.dir[1]**2)
    self.dir = self.dir[0]/distance, self.dir[1]/distance
    startDist = originPlanet.size
    self.pos = self.pos[0]+self.dir[0]*startDist, self.pos[1]+self.dir[1]*startDist
    self.speed = 120  # Pixels per second
    
  def update(self):
    self.dir = self.destPlanet.pos[0]-self.pos[0], self.destPlanet.pos[1]-self.pos[1]
    distance = math.sqrt(self.dir[0]**2 + self.dir[1]**2)
    self.dir = self.dir[0]/distance, self.dir[1]/distance
    adjustedSpeed = self.speed * glob.gameTimeStep
    self.pos = self.pos[0]+self.dir[0]*adjustedSpeed, self.pos[1]+self.dir[1]*adjustedSpeed
    if self.isAtDestination():
      if self.destPlanet.player is self.player:
        self.destPlanet.population += self.population
      else:
        self.destPlanet.population -= self.population
        if self.destPlanet.population < 0:
          self.destPlanet.player = self.player
          self.destPlanet.population *= -1
      glob.caravanList.remove(self)
      return
    if self.population == 0:
      glob.caravanList.remove(self)
      return
  
  def draw(self):
    pygame.gfxdraw.filled_circle(glob.windowSurface, int(self.pos[0]), int(self.pos[1]), int(3*(self.population**(1.0/3))), self.player.color)
    pygame.gfxdraw.aacircle(glob.windowSurface, int(self.pos[0]), int(self.pos[1]), int(3*(self.population**(1.0/3))), (0,0,0))
  
  def isAtDestination(self):
    xDiff = self.destPlanet.pos[0] - self.pos[0]
    yDiff = self.destPlanet.pos[1] - self.pos[1]
    if self.destPlanet.size**2 >= xDiff**2 + yDiff**2:
      return True