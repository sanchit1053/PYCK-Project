import pygame as py
from pygame.locals import (
	K_UP,   K_w,
	K_DOWN, K_s,
	K_LEFT, K_a,
	K_RIGHT,K_d,
	K_ESCAPE,
	KEYDOWN,
	QUIT,
	RLEACCEL
)
import math
from settings import *
import camera

from random import randint


class player(py.sprite.Sprite):

	def __init__(self , camera):
		super(player,self).__init__()
		self.surf = py.Surface((30,30))
		#self.surf = py.image.load(tank).convert()
		#self.surf.set_colorkey(white,RLEACCEL)
		self.rect = self.surf.get_rect()
		self.rect.topleft =  (1,1)
		self.imagesurface = py.Surface((30,30))
		self.imagesurface = py.image.load(cannon).convert()
		self.imagesurface = py.transform.scale(self.imagesurface,(30,30))
		self.imagesurface.set_colorkey(white, RLEACCEL)
		self.rectimage = self.imagesurface.get_rect()
		# commented lines used to debug without a sprite image
		#py.draw.lines(self.imagesurface,(0,0,255),False,[(0,7),(15,7)] , 5)
		#self.imagesurface.fill((255,0,0))
		self.rot_image =self.imagesurface
		self.angle = 0
		self.camera = camera

	def update(self, pressed_keys, cells):
		i = self.rect.x // cellsize
		j = self.rect.y // cellsize
		cell = cells[i][j]

		# moving the player
		if pressed_keys[K_UP] or pressed_keys[K_w]:
			self.rect.move_ip(0, -speed)
		if pressed_keys[K_DOWN] or pressed_keys[K_s]:
			self.rect.move_ip(0, speed)
		if pressed_keys[K_LEFT] or pressed_keys[K_a]:
			self.rect.move_ip(-speed, 0)
		if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
			self.rect.move_ip(speed, 0)

		# not allowing the player to pass through walls
		if self.rect.y <= cell.y * cellsize and cell.walls[0].active == True:
			self.rect.y = cell.y * cellsize
		if self.rect.x + self.rect.width >= cell.x * cellsize + cellsize and cell.walls[1].active == True:
			self.rect.x = cell.x * cellsize + cellsize - self.rect.width
		if self.rect.y + self.rect.height >= cell.y * cellsize + cellsize and cell.walls[2].active == True:
			self.rect.y = cell.y * cellsize + cellsize - self.rect.height
		if self.rect.x <= cell.x * cellsize and cell.walls[3].active == True:
			self.rect.x = cell.x * cellsize

		# rotating the player toward the mouse
		self.rotate(self.camera)
	

	def rotate(self, camera):
		#print(self.angle)
		mousex,mousey = py.mouse.get_pos()
		mousey -= userinterface
		x,y = camera.apply(self).topleft
		relx, rely = x - mousex,y - mousey
		angle = 90 - ((180/math.pi) * -math.atan2(relx,rely))
		self.angle = angle
		self.rot_image = py.transform.rotate(self.imagesurface,int(angle))
		self.rectimage.center = self.rect.center
		#self.surf.blit(self.rot_image,(0,0))

	# returns a bullet on click
	def shoot(self):
		return bullet(self.rect.center[0], self.rect.center[1], self.angle, self.camera)




class bullet(py.sprite.Sprite):
	def __init__(self, x, y, angle, camera):
		super(bullet,self).__init__()
		self.x = x
		self.y = y
		self.angle = angle
		self.surf = py.Surface((7,7))
		self.surf.fill((255,255,255))
		self.rect = self.surf.get_rect()
		self.rect.center = (x,y) 

		mousex,mousey = py.mouse.get_pos()
		mousey -= userinterface
		x,y = camera.apply(self).topleft
		direction = (-x + mousex, -y + mousey)
		length = math.hypot(*direction)
		self.direction = (direction[0]/length,direction[1]/length)


	# uses the direction which is stored during the initialisation to move the object
	def update(self, cells):
		i = self.rect.x // cellsize
		j = self.rect.y // cellsize
		if self.rect.x > MAPSIZE or self.rect.x < 0:
			self.kill()
		if self.rect.y > MAPSIZE or self.rect.y < 0:
			self.kill()	

		try:
			cell = cells[i][j]
		except :
			self.kill()
		self.x = self.x + self.direction[0] * bulletSpeed
		self.y = self.y + self.direction[1] * bulletSpeed 
		if self.rect.y < cell.y * cellsize and cell.walls[0].active == True:
			self.kill()
		if self.rect.x + self.rect.width > cell.x * cellsize + cellsize and cell.walls[1].active == True:
			self.kill()
		if self.rect.y + self.rect.height > cell.y * cellsize + cellsize and cell.walls[2].active == True:
			self.kill()
		if self.rect.x < cell.x * cellsize and cell.walls[3].active == True:
			self.kill()
		self.rect.center  = (self.x, self.y)




class enemy(py.sprite.Sprite):
	def __init__(self, camera, ai):
		super(enemy, self).__init__()
		self.image = py.Surface((30,30))
		self.image = py.image.load(robot).convert()
		self.image.set_colorkey(white, RLEACCEL)
		self.image = py.transform.scale(self.image,(30,30))
		self.surf = self.image
		self.rect = self.surf.get_rect()
		self.rect.center = (MAPSIZE - cellsize/2, MAPSIZE - cellsize/2)
		self.dir = 0
		self.speed = enemySpeed
		self.movingTo = None
		self.AI = ai
		self.offsetx = 0
		self.offsety = 0


	# offsetting the enemy so that all enemies are not on the same grid
	def offset(self):
		self.offsetx = randint(-cellsize//2 + 30, cellsize//2 - 30)
		self.offsety = randint(-cellsize//2 + 30, cellsize//2 - 30)
		self.rect.move_ip(self.offsetx, self.offsety)


	# updating the enemy position depending on its AI
	def update(self, cells,player):
		i = self.rect.x // cellsize
		j = self.rect.y // cellsize
		cell = cells[i][j]

		k = player.rect.x // cellsize
		l = player.rect.y // cellsize
		
		# following the player if both in same cell
		if i == k and j == l:
			if player.rect.x > self.rect.x:
				self.rect.move_ip(self.speed, 0)
			if player.rect.x < self.rect.x:
				self.rect.move_ip( -self.speed, 0)
			if player.rect.y > self.rect.y:
				self.rect.move_ip(0 , self.speed)
			if player.rect.y < self.rect.y:
				self.rect.move_ip(0, -self.speed)
			self.movingTo = None
			self.offsetx = self.rect.center[0] - i*cellsize - cellsize//2
			self.offsety = self.rect.center[1] - j*cellsize - cellsize//2
			

		# if it alredy has a final position move its speed toward that direction
		if not self.movingTo == None:

			if self.dir == 0:
				self.rect.move_ip(0, -self.speed)
			if self.dir == 1:
				self.rect.move_ip(self.speed, 0)
			if self.dir == 2:
				self.rect.move_ip(0, self.speed)
			if self.dir == 3:
				self.rect.move_ip(-self.speed, 0)

			if self.rect.y <= cell.y * cellsize and cell.walls[0].active == True:
				self.rect.y = cell.y * cellsize
			if self.rect.x + self.rect.width >= cell.x * cellsize + cellsize and cell.walls[1].active == True:
				self.rect.x = cell.x * cellsize + cellsize - self.rect.width
			if self.rect.y + self.rect.height >= cell.y * cellsize + cellsize and cell.walls[2].active == True:
				self.rect.y = cell.y * cellsize + cellsize - self.rect.height
			if self.rect.x <= cell.x * cellsize and cell.walls[3].active == True:
				self.rect.x = cell.x * cellsize

			allowed  = 10
			if     self.movingTo[0] * cellsize + cellsize//2 - allowed + self.offsetx <= self.rect.center[0]  <= self.movingTo[0] * cellsize + cellsize//2 + allowed + self.offsetx   \
			   and self.movingTo[1] * cellsize + cellsize//2 - allowed + self.offsety <= self.rect.center[1]  <= self.movingTo[1] * cellsize + cellsize//2 + allowed + self.offsety:
				self.movingTo = None 

		# if it doesn't have a direction use the the AI to decide on a direction
		else:	
			if self.AI == 0:
				mouseA(self,cells)
			if self.AI == 1:
				mouseB(self,cells)
			if self.AI == 2:
				drone(self,cells,player)

			if self.dir == 0:
				self.surf = py.transform.rotate(self.image,180)
				self.movingTo = (i , j - 1)
			elif self.dir == 1:
				self.surf = py.transform.rotate(self.image,90)
				self.movingTo = (i + 1, j )
			elif self.dir == 2:
				self.surf = py.transform.rotate(self.image,0)
				self.movingTo = (i , j + 1)
			elif self.dir == 3:
				self.surf = py.transform.rotate(self.image,270)
				self.movingTo = (i - 1, j )


# simple turn left algorithm
def mouseA(enemy, cells):
	i = enemy.rect.x // cellsize
	j = enemy.rect.y // cellsize
	cell = cells[i][j]

	if not cell.walls[(enemy.dir+1)%4].active:
		enemy.dir = (enemy.dir+1)%4
	while cell.walls[(enemy.dir)].active:
		enemy.dir = (enemy.dir-1)%4


# simple turn right algorithm
def mouseB(enemy, cells):
	i = enemy.rect.x // cellsize
	j = enemy.rect.y // cellsize
	cell = cells[i][j]

	if not cell.walls[(enemy.dir-1)%4].active:
		enemy.dir = (enemy.dir-1)%4
	while cell.walls[(enemy.dir)].active:
		enemy.dir = (enemy.dir+1)%4



# complex find the path and then use the last two entries to find the direction algorithm
def drone(enemy, cells , target):
	visited = [[False for a in cells[0]] for b in cells]

	i = target.rect.x // cellsize
	j = target.rect.y // cellsize
	current = cells[i][j]
	queue = []
	queue.append(current)
	i = enemy.rect.x // cellsize
	j = enemy.rect.y // cellsize
	final = cells[i][j]
	k = 0
	c = queue[-1]
	while (c.x != final.x or c.y != final.y):
		x = c.x
		y = c.y
		visited[c.x][c.y] = True
		if  (c.walls[0].active or visited[x][y-1]) and \
			(c.walls[1].active or visited[x+1][y]) and \
			(c.walls[2].active or visited[x][y+1]) and \
			(c.walls[3].active or visited[x-1][y]):
			queue.pop()

		elif not (c.walls[0].active or visited[x][y-1]):
			queue.append(cells[x][y-1])
		elif not (c.walls[1].active or visited[x +1][y]):
			queue.append(cells[x + 1][y])
		elif not (c.walls[2].active or visited[x][y+1]):
			queue.append(cells[x][y+1])
		elif not (c.walls[3].active or visited[x-1][y]):
			queue.append(cells[x-1][y])
		
		c = queue[-1]

	if len(queue) == 1:
		enemy.dir = -1
	else:
		x = queue[-2].x - queue[-1].x
		y = queue[-2].y - queue[-1].y
		if y == -1:
			enemy.dir = 0
		if x == 1:
			enemy.dir = 1
		if y == 1:
			enemy.dir = 2
		if x == -1:
			enemy.dir = 3
	