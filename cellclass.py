import pygame as py
from random import randint

from settings import *


# making a sprite to be added to the cells surface 
class wall(py.sprite.Sprite):
	def __init__(self,x,y,width,height,ori):
		super(wall,self).__init__()
		self.x = x
		self.y = y
		self.active = True
		self.surf = py.Surface((width,height))
		a= py.Surface((5,5))
		a =py.image.load(walltile).convert()
		rec = a.get_rect()

		# repeating the wall sprite on the wall surface
		for i in range(0,cellsize,5):
			if ori == 0:
				rec.topleft = (i,0)
				self.surf.blit(a,rec)
			if ori == 1:
				rec.topleft = (0,i)
				self.surf.blit(a,rec)
		#self.surf.fill(color)
		self.rect = self.surf.get_rect()
		self.rect.topleft = (x,y)

	def show(self):
		pass

class cell(py.sprite.Sprite):
	
	def __init__(self,x,y,color):
		super(cell,self).__init__()
		self.surf = py.Surface(( cellsize , cellsize))
		self.rect = self.surf.get_rect()
		self.rect.topleft = (x * cellsize, y * cellsize)
		up    = wall(0       ,0       ,cellsize ,wallwidth,0)
		right = wall(cellsize,0       ,wallwidth,cellsize ,1)
		down  = wall(0       ,cellsize,cellsize ,wallwidth,0)
		left  = wall(0       ,0       ,wallwidth,cellsize ,1)
		self.walls = [up,right,down,left]
		self.color = color
		self.visited = False
		self.previous = None

		self.x = x
		self.y = y
	

	# if the wall is active then blitting to the cell surface
	def show(self):
		
		if(self.walls[0].active):
			self.surf.blit(self.walls[0].surf,self.walls[0].rect)
		if(self.walls[1].active):
			self.surf.blit(self.walls[1].surf,self.walls[1].rect)
		if(self.walls[2].active):
			self.surf.blit(self.walls[2].surf,self.walls[2].rect)
		if(self.walls[3].active):
			self.surf.blit(self.walls[3].surf,self.walls[3].rect)


	# finding the next cell to move to in a DFS algorithm
	def next(self, cells):
		self.visited = True
		numberOfCells = len(cells)

		# if covered by visited cells then return to previous cell
		if(cells[self.x][max(self.y - 1,0)].visited and  
		   cells[min(self.x + 1,numberOfCells-1)][self.y].visited and  
		   cells[self.x][min(self.y + 1,numberOfCells-1)].visited and  
		   cells[max(self.x - 1,0)][self.y].visited):
			#print("previous")
			return self.previous

		# keep choosing a random number until a valid cell is chosen
		while(True):
			random = randint(0,3)
			if((random == 0 and self.y == 0) or (random == 0 and cells[self.x][self.y - 1].visited)):
				continue
			if((random == 1 and self.x == numberOfCells - 1) or (random == 1 and cells[self.x + 1][self.y].visited)):
				continue
			if((random == 2 and self.y == numberOfCells - 1) or (random == 2 and cells[self.x][self.y + 1].visited)):
				continue
			if((random == 3 and self.x == 0) or (random == 3 and cells[self.x - 1][self.y].visited)):
				continue
			break

		if(random == 0):
			self.walls[0].active = False 
			cells[self.x][self.y - 1].walls[2].active = False
			cells[self.x][self.y - 1].previous = self
			return cells[self.x][self.y - 1]
		if(random == 1):
			self.walls[1].active = False 
			cells[self.x + 1][self.y].walls[3].active = False
			cells[self.x + 1][self.y ].previous = self
			return cells[self.x + 1][self.y ]
		if(random == 2):
			self.walls[2].active = False 
			cells[self.x][self.y + 1].walls[0].active = False
			cells[self.x][self.y + 1].previous = self
			return cells[self.x][self.y + 1]
		if(random == 3):
			self.walls[3].active = False 
			cells[self.x - 1][self.y].walls[1].active = False
			cells[self.x - 1][self.y].previous = self
			return cells[self.x - 1][self.y]
