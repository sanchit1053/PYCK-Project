import pygame as py
from settings import *


class Camera:
	def __init__(self,width,height):
		self.camerascreen  = py.Rect(0,0,width,height)
		self.width = width
		self.height = height

	# returns an offset to the entity
	def apply(self,entity):
		return entity.rect.move(self.camerascreen.topleft)

	# updates the camera location not allowing it to leave the game area
	def update(self,player):
		x = -player.rect.x  + (self.width//2)
		y = -player.rect.y  + (self.height//2)
		x = min(0,x)
		y = min(0,y)
		x = max((self.width - MAPSIZE) , x)
		y = max((self.height - MAPSIZE) , y)
		self.camerascreen = py.Rect(x,y,self.width,self.height)