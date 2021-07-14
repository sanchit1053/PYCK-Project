import os
path = os.getcwd()
# the size of the map
MAPSIZE = 800
# the size of screen which is showing
screensize = 600
# size of each cell
cellsize = 80


numberOfCells = MAPSIZE//cellsize

# speed of bullets
bulletSpeed = 5.0

# speed of enemies
enemySpeed = 1

# speed of player
speed = max(MAPSIZE / 1600 , 1) 

# width of wall
wallwidth = 5

#colors
white = (255,255,255)
black = (  0,  0,  0)
red   = (255,  0,  0)
green = (0  ,255,  0)
blue  = (  0,  0,255)

# defining a second
second = 1000
# time after which a new enemy spawns
spawntime = 10000

# blank space on top
userinterface = 50

# all the sprites
walltile = os.path.join(path,"wall.png")
cannon = os.path.join(path,"cannon.png")
robot = os.path.join(path,"robot.png")