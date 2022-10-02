import pygame, math, random
from Brick import Brick

class Enemy(pygame.sprite.Sprite):
	BALL = 0
	SATURN = 1
	ELECTRON = 2
	PYRAMID = 3
	CUBE = 4
	CONE = 5

	LEFT = 0
	TOP = 584
	XPADDING = 0
	YPADDING = 0
	SHEETWIDTH = 44
	SHEETHEIGHT=44
	NBHOR = 5
	NBVER = 5

	WIDTH=SHEETWIDTH-2*XPADDING
	HEIGHT=SHEETHEIGHT-2*YPADDING

	spriteSheet = pygame.image.load("./levels/sprites/sprites.png")

	# liste qui contient des listes (les animations pour chacun des enemis)
	allsprites = None
	allmasks = None

	# chemin du sprite
	allpaths = None

	def createSpriteList(self, xstart, ystart):
		liste = list()
		mask = list()
		for j in range(0,5):
			for i in range(0,5):
				img = Enemy.spriteSheet.subsurface(pygame.Rect(
																Enemy.LEFT+i*Enemy.SHEETWIDTH+Enemy.XPADDING+xstart,
																Enemy.TOP+j*Enemy.SHEETHEIGHT+Enemy.YPADDING+ystart,
																Enemy.WIDTH,
																Enemy.HEIGHT)
															)
				m = pygame.mask.from_surface(img)
				liste.append(img)
				mask.append(m)
		return (liste, mask)

	def createPath1(self):
		path = list()
		for i in range(0,Brick.HEIGHT*6):
			path.append( (0,1) )
		for i in range(0,6*Brick.WIDTH):
			path.append( (1,0) )
		for i in range(0,360):
			ang = ((i)%360)*2*3.14/360
			path.append( (math.cos(ang)*2, math.sin(ang)) )
		for i in range(0,6*Brick.WIDTH):
			path.append( (1,0) )
		for i in range(0,Brick.HEIGHT*6):
			path.append( (0,1) )
		for i in range(0,6*Brick.WIDTH):
			path.append( (-1,0) )
		for i in range(0,360):
			ang = (((360-i+90))%360)*2*3.14/360
			path.append( (math.cos(ang)*2, math.sin(ang)) )
		for i in range(0,6*Brick.WIDTH):
			path.append( (-1,0) )
		return path

	def createPath2(self):
		path = list()
		j=0
		for i in range(0,22*6):
			path.append( (math.cos(j*2*3.14/360)/2,1+math.sin(j*2*3.14/360)) )
			j+=1
		for i in range(0,6*44):
			path.append( (1+math.cos(j*2*3.14/360),math.sin(j*2*3.14/360)/2) )
			j+=1
		for i in range(0,360):
			ang = ((i)%360)*2*3.14/360
			path.append( (math.cos(ang)*2, math.sin(ang)) )
		for i in range(0,6*44):
			path.append( (1+math.cos(j*2*3.14/360),math.sin(j*2*3.14/360)/2) )
			j+=1
		for i in range(0,22*6):
			path.append( (math.cos(j*2*3.14/360)/2,1+math.sin(j*2*3.14/360)) )
			j+=1
		for i in range(0,6*44):
			path.append( (-1+math.cos(j*2*3.14/360),-math.sin(j*2*3.14/360)/2) )
			j+=1
		for i in range(0,360):
			ang = (((360-i+90))%360)*2*3.14/360
			path.append( (math.cos(ang)*2, math.sin(ang)) )
		for i in range(0,6*44):
			path.append( (-1+math.cos(j*2*3.14/360),-math.sin(j*2*3.14/360)/2) )
			j+=1
		return path

	def __init__(self, playfield):
		pygame.sprite.Sprite.__init__(self)

		self.playfield = playfield

		if(Enemy.allpaths==None): # on initialise les parcours disponibles
			Enemy.allpaths = list()
			Enemy.allpaths.append(self.createPath1())
			Enemy.allpaths.append(self.createPath2())
			self.createPath2()

		self.path = Enemy.allpaths[random.randint(0, len(Enemy.allpaths)-1)] #on tire un parcours au hasard parmi les parcours disponibles

		if(Enemy.allsprites==None):
			Enemy.allsprites = list()
			Enemy.allmasks = list()
			(liste,mask) = self.createSpriteList(0,0) # balle
			Enemy.allsprites.append(liste)
			Enemy.allmasks.append(mask)
			(liste,mask) = self.createSpriteList(220,0) # saturne
			Enemy.allsprites.append(liste)
			Enemy.allmasks.append(mask)
			(liste,mask) = self.createSpriteList(440,0) # electron
			Enemy.allsprites.append(liste)
			Enemy.allmasks.append(mask)
			(liste,mask) = self.createSpriteList(0,220) # pyramide
			Enemy.allsprites.append(liste)
			Enemy.allmasks.append(mask)
			(liste,mask) = self.createSpriteList(220,220) # cube
			Enemy.allsprites.append(liste)
			Enemy.allmasks.append(mask)
			(liste,mask) = self.createSpriteList(440,220) # cone
			Enemy.allsprites.append(liste)
			Enemy.allmasks.append(mask)

		self.enemyType = Enemy.BALL

		self.sprites = Enemy.allsprites[self.enemyType]
		self.masks = Enemy.allmasks[self.enemyType]
		self.positionx = 0
		self.positiony = 0
		self.previouspositionx = 0
		self.previouspositiony = 0
		self.rect = pygame.Rect(int(self.positionx),int(self.positiony),Enemy.WIDTH,Enemy.HEIGHT)
		self.image = self.sprites[0]
		self.mask = self.masks[0]

		self.deltaTime = 0
		self.index = 0

		self.current = random.randint(0,len(self.path))

	def forward(self):
		self.previouspositionx = self.positionx
		self.previouspositiony = self.positiony

		self.current = self.current%len(self.path)
		xinc, yinc = self.path[self.current]
		self.current += 1
		self.current = self.current%len(self.path)

		self.positionx += xinc
		self.positiony += yinc

		border = False
		if(self.positionx<self.playfield.x):
			self.positionx = self.previouspositionx
			border = True
		if(self.positionx>self.playfield.x+self.playfield.w-self.rect.w):
			self.positionx = self.previouspositionx
			border = True
		if(self.positiony<self.playfield.y):
			self.positiony = self.previouspositiony
			border = True
		if(self.positiony>self.playfield.y+self.playfield.h):
			self.kill()

		self.rect = pygame.Rect(int(self.positionx),int(self.positiony),Enemy.WIDTH,Enemy.HEIGHT)

		return border

	def update(self,time):
		while(self.forward()):
			self.goToPreviousPosition()

		self.deltaTime = self.deltaTime + time
		if self.deltaTime>=100:
			self.deltaTime = 0

			self.index += 1
			self.index = self.index%len(self.sprites)

			self.image = self.sprites[self.index]
			self.mask = self.masks[self.index]

	def setPosition(self, x,y):
		self.positionx = x
		self.positiony = y
		self.rect = pygame.Rect(int(self.positionx),int(self.positiony),Enemy.WIDTH,Enemy.HEIGHT)

	def setEnemyType(self, type):
		'''
		BALL = 0
		SATURN = 1
		ELECTRON = 2
		PYRAMID = 3
		CUBE = 4
		CONE = 5
		'''
		if(type>=0 and type<len(self.allsprites)):
			self.index = 0
			self.enemyType = type
			self.sprites = self.allsprites[self.enemyType]
			self.masks = self.allmasks[self.enemyType]
			self.image = self.sprites[self.index]
			self.mask = self.masks[self.index]

	def getEnemyType(self):
		return self.enemyType

	def goToPreviousPosition(self):
		self.positionx = self.previouspositionx
		self.positiony = self.previouspositiony

	def fastForward(self):
		self.goToPreviousPosition()
		self.forward()

	def injured(self):
		self.kill()
		return True