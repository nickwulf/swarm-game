import os, sys, math, random, time, pygame
from pygame.locals import *
import pygame.gfxdraw

# Import global variables
import globals as glob
import utilities as util

class LaserSpark:
  
  def __init__(self, pos, angle, omega, speed, color, fadeLimit, deathLimit):
    self.pos = pos
    self.angle = angle
    self.omega = omega
    self.speed = speed
    self.color = color
    self.life = 1.0
    self.fadeLimit = fadeLimit
    self.deathLimit = deathLimit
    
  def update(self):
    adjustedSpeed = self.speed * glob.gameTimeStep
    self.pos = self.pos[0]+adjustedSpeed*math.cos(math.radians(self.angle)), self.pos[1]+adjustedSpeed*math.sin(math.radians(self.angle))
    self.angle += self.omega * glob.gameTimeStep
    self.speed *= math.exp(-3.0775977*glob.gameTimeStep)
    self.life *= math.exp(-3.0775977*glob.gameTimeStep)
    if self.life <= self.deathLimit:
      glob.particleList.remove(self)
      return
  
  def draw(self):
    drawColor = self.color
    tailDist = self.speed * 0.04
    tailPos = self.pos[0] + tailDist*math.cos(math.radians(self.angle)), self.pos[1] + tailDist*math.sin(math.radians(self.angle))
    if self.life < self.fadeLimit:
      drawColor = util.colorFade(self.color, (self.life-self.deathLimit)/(self.fadeLimit-self.deathLimit))
    pygame.gfxdraw.line(glob.windowSurface, int(tailPos[0]), int(tailPos[1]), int(self.pos[0]), int(self.pos[1]), drawColor)
    

class CaravanDebris:
  
  def __init__(self, pos, angle, population, speed, color, lifeTime):
    self.pos = pos
    self.angle = angle
    self.size = int(3*(population**(1.0/3)))
    self.speed = speed
    self.color = color
    self.age = 0
    self.lifeTime = lifeTime
    self.fadeTime = lifeTime*0.75
    
  def update(self):
    adjustedSpeed = self.speed * glob.gameTimeStep
    self.pos = self.pos[0]+adjustedSpeed*math.cos(math.radians(self.angle)), self.pos[1]+adjustedSpeed*math.sin(math.radians(self.angle))
    self.speed *= math.exp(-3.0775977*glob.gameTimeStep)
    self.age += glob.gameTimeStep
    if self.age >= self.lifeTime:
      glob.particleList.remove(self)
      return
  
  def draw(self):
    fadeRatio = 1
    if self.age > self.fadeTime:
      fadeRatio = (self.lifeTime-self.age)/(self.lifeTime-self.fadeTime)
    fillColor = util.colorFade(self.color, fadeRatio)
    borderColor = util.colorFade(util.combineColors((0,0,0),self.color,0.5), fadeRatio/2.0)
    pygame.gfxdraw.filled_circle(glob.windowSurface, int(self.pos[0]), int(self.pos[1]), self.size, fillColor)
    pygame.gfxdraw.aacircle(glob.windowSurface, int(self.pos[0]), int(self.pos[1]), self.size, borderColor)
  