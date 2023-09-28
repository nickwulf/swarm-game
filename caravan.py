import sys, math, random, time, pygame
import pygame.gfxdraw

# Import global variables and utilities
import globals as glob
import utilities as util

# Import user classes
from particle import *

class Caravan:
  
  def __init__(self, originPlanet, destPlanet, population):
    self.originPlanet = originPlanet
    self.player = originPlanet.player
    self.destPlanet = destPlanet
    self.population = population
    self.unexplodedPop = population
    self.pos = originPlanet.pos
    self.drawPos = self.pos[0]-glob.winPos[0], self.pos[1]-glob.winPos[1]
    self.oldPos = self.pos
    self.dir = self.destPlanet.pos[0]-self.pos[0], self.destPlanet.pos[1]-self.pos[1]
    distance = math.sqrt(self.dir[0]**2 + self.dir[1]**2)
    self.dir = self.dir[0]/distance, self.dir[1]/distance
    startDist = originPlanet.size
    self.pos = self.pos[0]+self.dir[0]*startDist, self.pos[1]+self.dir[1]*startDist
    self.speed = 120  # Pixels per second
    
  def update(self):
    self.oldPos = self.pos
    self.dir = self.destPlanet.pos[0]-self.pos[0], self.destPlanet.pos[1]-self.pos[1]
    distance = math.sqrt(self.dir[0]**2 + self.dir[1]**2)
    self.dir = self.dir[0]/distance, self.dir[1]/distance
    adjustedSpeed = self.speed * glob.gameTimeStep
    self.pos = self.pos[0]+self.dir[0]*adjustedSpeed, self.pos[1]+self.dir[1]*adjustedSpeed
    if self.isAtDestination():
      if self.destPlanet.player is self.player:
        self.destPlanet.population += self.population
      else:
        planetAngle = math.degrees(math.atan2(self.dir[1], self.dir[0]))
        self.explode(min(self.population,self.destPlanet.population), planetAngle+90, planetAngle+270, self.pos)
        self.destPlanet.population -= self.population
        if self.destPlanet.population < 0:
          self.destPlanet.changePlayer(self.player)
          self.destPlanet.population *= -1
      glob.caravanList.remove(self)
      return
    self.drawPos = self.pos[0]-glob.winPos[0], self.pos[1]-glob.winPos[1]
      
  def update2(self):
    if self.population <= 0:
      self.population = 0
    popDiff = self.unexplodedPop - self.population
    if popDiff >= .5 or self.population <= 0:
      self.explode(popDiff, 0, 360, self.pos)
      self.unexplodedPop = self.population
    if self.population <= 0:
      glob.caravanList.remove(self)
      return
  
  def draw(self):
    if self.population <= 0:
      print("Error 1")
      return
    drawSize = int(3*(self.population**(1.0/3)))
    if drawSize < 2:
      drawSize = 2
    pygame.gfxdraw.filled_circle(glob.windowSurface, int(self.drawPos[0]), int(self.drawPos[1]), drawSize, self.player.color)
    pygame.gfxdraw.aacircle(glob.windowSurface, int(self.drawPos[0]), int(self.drawPos[1]), drawSize, (0,0,0))
  
  def isAtDestination(self):
    xDiff = self.destPlanet.pos[0] - self.pos[0]
    yDiff = self.destPlanet.pos[1] - self.pos[1]
    if self.destPlanet.size**2 >= xDiff**2 + yDiff**2:
      return True
      
  def takeDamage(self, damage, explodePos=None):
    if explodePos is None:
      explodePos = self.pos
    self.population -= damage
    if self.population <= 0:
      self.population = 0
    popDiff = self.unexplodedPop - self.population
    if popDiff >= .5 or self.population <= 0:
      self.explode(popDiff, 0, 360, explodePos)
      self.unexplodedPop = self.population
    if self.population <= 0:
      glob.caravanList.remove(self)
      return
      
  def explode(self, explodePop, startAngle, endAngle, explodePos):
    speedAlpha = explodePop**(1.0/3)
    if speedAlpha < 1:
      speedAlpha = 1
    while explodePop >= 1:
      chippedPop = random.uniform(.5, explodePop * 0.5)
      explodePop -= chippedPop
      glob.particleList.append(CaravanDebris(explodePos, random.uniform(startAngle,endAngle), chippedPop, random.uniform(10*speedAlpha,50*speedAlpha), self.player.color, random.uniform(.5,1)))
    glob.particleList.append(CaravanDebris(explodePos, random.uniform(startAngle,endAngle), 0.5, random.uniform(10*speedAlpha,50*speedAlpha), self.player.color, random.uniform(.5,1)))
  