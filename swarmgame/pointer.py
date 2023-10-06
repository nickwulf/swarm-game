import os, sys, math, random, time, pygame
from pygame.locals import *
import pygame.gfxdraw

# Import global variables and utilities
from . import globals as glob
from . import utilities as util

class Pointer:

   def __init__(self):
      self.state = "Idle"
      self.stateFrame = 0
      frameSize = 40
      dir_path = os.path.dirname(os.path.realpath(__file__))
      rawPointerSurf = pygame.image.load(os.path.join(dir_path, 'images', 'Pointer.bmp'))
      frameCount = int(rawPointerSurf.get_width()/frameSize)
      self.frames = []
      for i in range(frameCount):
         self.frames.append(pygame.Surface((frameSize,frameSize), flags=SRCALPHA))
         self.frames[i].blit(rawPointerSurf, (-i*frameSize,0))
      self.idleFrames = []
      self.idleFrames.extend(self.makeCloneList(0,210))
      self.idleFrames.extend(self.makeCloneList(1,9))
      self.idleFrames.extend(self.makeCloneList(2,6))
      self.idleFrames.extend(self.makeCloneList(3,6))
      self.idleFrames.extend(self.makeCloneList(4,9))
      self.idleFrames.extend(self.makeCloneList(5,30))
      self.idleFrames.extend(self.makeCloneList(4,9))
      self.idleFrames.extend(self.makeCloneList(3,6))
      self.idleFrames.extend(self.makeCloneList(2,6))
      self.idleFrames.extend(self.makeCloneList(1,9))

   def draw(self):
      pic = self.frames[self.idleFrames[self.stateFrame]]
      glob.windowSurface.blit(pic, (glob.mouseDrawPos[0], glob.mouseDrawPos[1]))
      self.stateFrame += 1
      if self.stateFrame >= len(self.idleFrames):
         self.stateFrame = 0

   def makeCloneList(self, value, count):
      list = []
      for i in range(count):
         list.append(value)
      return list
