import pygame as py
import numpy as np
from random import randint

from settings import *

from cellclass import cell
import player
import camera


import time
import sys
from random import randint

from pygame.locals import MOUSEBUTTONDOWN



clock = py.time.Clock()

# finding the corner farthest away from player
def spawnspot(player):
	m = player.rect.x > MAPSIZE//2
	n = player.rect.y > MAPSIZE//2
	if m == True and n == True: 
		m,n = cellsize//2, cellsize//2
	if m == True and n == False:
		m,n = cellsize//2, MAPSIZE - cellsize//2
	if m == False and n == True:
		m,n =  MAPSIZE - cellsize//2 , 	cellsize//2 
	if m == False and n == False:
		m,n = MAPSIZE - cellsize//2, MAPSIZE - cellsize//2
	return (m,n)	
	

class Game:
	def __init__(self):
		self.cells = [[cell(i, j, red) for j in range(numberOfCells)] for i in range(numberOfCells)]
		self.cam = camera.Camera(screensize,screensize)
		self.Player = player.player(self.cam)
		self.events = None
		self.running = True
		self.bullets = py.sprite.Group()
		self.enemies = py.sprite.Group()
		self.enemies.add(player.enemy(self.cam, 1))
		#self.enemies.add(player.enemy(self.cam, 1))
		for e in self.enemies:
			e.offset()

		self.score = 0
		self.font = py.font.Font("freesansbold.ttf", 16)
		self.text = self.font.render(f"score : {self.score}", False, green, blue)

	def menu(self):
		f = py.font.Font("freesansbold.ttf",64)
		name = f.render("THE GAME", False, black, white)
		rect = name.get_rect()
		rect.center = (screensize//2, 30)
		GameBoard.blit(name,rect)

	# making a list a cells in the maze
	def maze(self,color = red):
		current = self.cells[0][0]
		current = current.next(self.cells)
		#current.show()
		while(current != self.cells[0][0]):
			current = current.next(self.cells)
		for _ in range(3):
			x = randint(1,numberOfCells - 2)
			y = randint(1,numberOfCells - 2)

			c = self.cells[x][y]
		
			c.walls[0].active = False
			self.cells[x][y-1].walls[2].active = False
			c.walls[1].active = False
			self.cells[x+1][y].walls[3].active = False
			c.walls[2].active = False
			self.cells[x][y+1].walls[0].active = False
			c.walls[3].active = False
			self.cells[x-1][y].walls[1].active = False

	def get_events(self):
		self.events = py.event.get()
		for event in self.events:
			if event.type == py.locals.QUIT:
				self.running = False

			if event.type == SPAWN:
				if len(self.enemies) < 20:
					newenemy = player.enemy(self.cam, randint(0,2))
					newenemy.rect.center = spawnspot(self.Player)
					newenemy.offset()
					self.enemies.add(newenemy)

			if event.type == SCORE:
				self.score += len(self.enemies)



	# blitting everything in the screnn
	def show(self):
		screen.fill(white)
		for i in range(0,numberOfCells,1):
			for j in range(0,numberOfCells,1):
				self.cells[i][j].show()
				screen.blit(self.cells[i][j].surf,self.cam.apply(self.cells[i][j]))
		screen.blit(self.Player.rot_image,self.cam.apply(self.Player))

		for b in self.bullets:
			screen.blit(b.surf,self.cam.apply(b))

		for e in self.enemies:
			screen.blit(e.surf,self.cam.apply(e))
			#uncomment the lines to see where the enemy is moving to
			#a =py.Surface((20,20))
			#a.fill(white)
			#r = a.get_rect()
			#if e.movingTo != None:
			#	r.center = (e.movingTo[0] * cellsize + cellsize/2 + e.offsetx, e.movingTo[1] * cellsize + cellsize/2 + e.offsety)
			#	screen.blit(a, r)


		GameBoard.blit(self.text,self.text.get_rect())



	# calling update funtion of each object and handling collision
	def update(self):
		pressed_keys = py.key.get_pressed()
		for event in self.events:
			if event.type == py.MOUSEBUTTONDOWN:
				self.bullets.add(self.Player.shoot())
				self.score -= 10
				if self.score <0:
					self.score = 0
		for b in self.bullets:
			b.update(self.cells)

		for e in self.enemies: 
			for b in self.bullets:
					if b.rect.colliderect(e.rect):
						self.score += 10 
						e.kill()
						b.kill()
			if e.rect.colliderect(self.Player.rect):
				self.Player.kill()
				self.running = False
		for e in self.enemies:
			e.update(self.cells, self.Player)
		self.Player.update(pressed_keys,self.cells)
		self.cam.update(self.Player)

		self.text = self.font.render(f"score : {self.score}", False, green, blue)





def getClick():
	pos = None
	while pos == None:
		event = py.event.get()
		for e in event:
			if e.type == MOUSEBUTTONDOWN:
				pos = py.mouse.get_pos()
				break
	return pos




py.init()
GameBoard = py.display.set_mode((screensize,screensize + userinterface))

screen = py.Surface((screensize,screensize))
game = Game()

SPAWN =py.USEREVENT + 1
py.time.set_timer(SPAWN, spawntime)

SCORE = py.USEREVENT + 2
py.time.set_timer(SCORE, second)


game.menu()
py.display.flip()
getClick()


cells = game.maze()
while game.running:


	GameBoard.blit(screen, (0,50))
	clock.tick(120)
	game.get_events()
	game.show()
	game.update()
	py.display.flip() 

GameBoard.fill(white)
font = py.font.Font("freesansbold.ttf", 64)
gameover = font.render("GAME OVER", False, black, white)
gamerect = gameover.get_rect()
gamerect.center = ((screensize//2),screensize//2 - 40)
text = font.render(f"SCORE = {game.score}", False, black,white)
rect = text.get_rect()
rect.center = ((screensize//2,screensize//2 + 30))
GameBoard.blit(gameover,gamerect)
GameBoard.blit(text,rect)
py.display.flip()
running = True
while running:
	events = py.event.get()
	for event in events:
		if event.type == py.locals.QUIT:
			running = False
py.quit()
sys.exit()