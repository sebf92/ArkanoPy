import pygame, math, time

class Ball(pygame.sprite.Sprite):
	# la taille d'une balle
	WIDTH = 10
	HEIGHT=10

	# les balles
	spriteSheet = pygame.image.load("./levels/sprites/sprites.png")

	def __init__(self, playfield):
		pygame.sprite.Sprite.__init__(self)

		self.positionx = 0
		self.positiony = 0
		self.previouspositionx = self.positionx
		self.previouspositiony = self.positiony

		self.radius = 5
		self.orientation = 45
		self.velocity = 0

		self.playfield = playfield
		self.rect = pygame.Rect(self.positionx,self.positiony,Ball.WIDTH,Ball.HEIGHT)
		self.cyanball = Ball.spriteSheet.subsurface(pygame.Rect(58*14,36*1,Ball.WIDTH,Ball.HEIGHT))
		self.goldball = Ball.spriteSheet.subsurface(pygame.Rect(58*14,36*1+24,Ball.WIDTH,Ball.HEIGHT))
		self.image = self.cyanball
		self.mask = pygame.mask.from_surface(self.image)

		self.deltaTime = 0
		self.balllost = False

		self.invicible = False

		self.stickedTime = 0
		self.sticked = False
		self.stickdeltax = 0
		self.vaus = None

		self.silverball = False

	def update(self,ptime):

		if(self.sticked): # la balle se décroche toute seule au bout de 5 secondes
			currenttime = time.time()
			if(currenttime-self.stickedTime>5):
				self.unstick()

		if(self.silverball):
			self.image = self.goldball
		else:
			self.image = self.cyanball

		self.previouspositionx = self.positionx
		self.previouspositiony = self.positiony

		if(self.sticked):
			# si la balle est accrochée à la raquette
			# on suit la raquette...
			self.positionx = self.vaus.rect.x + self.stickdeltax
			self.positiony = self.vaus.rect.y - Ball.HEIGHT
		else:
			# sinon on la fait bouger

			# patch
			# on evite les balles verticales ou verticales
			if(self.orientation>85 and self.orientation<=90):
				self.orientation = 85
			elif(self.orientation>90 and self.orientation<95):
				self.orientation = 95
			elif(self.orientation>175 and self.orientation<=180):
				self.orientation = 175
			elif(self.orientation>180 and self.orientation<185):
				self.orientation = 185
			elif(self.orientation>265 and self.orientation<=270):
				self.orientation = 265
			elif(self.orientation>270 and self.orientation<275):
				self.orientation = 275
			elif(self.orientation>355):
				self.orientation = 355
			elif(self.orientation<5):
				self.orientation = 5

			xinc = math.cos(self.orientation*2*3.14/360)*self.velocity
			yinc = -math.sin(self.orientation*2*3.14/360)*self.velocity

			self.positionx += xinc
			self.positiony += yinc

			if(self.positionx<self.playfield.x):
				self.positionx=self.playfield.x
				self.horizontalSwap()
				self.unsetSilverBall()
			elif(self.positionx>self.playfield.x+self.playfield.width-self.WIDTH):
				self.positionx=self.playfield.x+self.playfield.width-self.WIDTH
				self.horizontalSwap()
				self.unsetSilverBall()

			if(self.positiony<self.playfield.y):
				self.positiony=self.playfield.y
				self.verticalSwap()
				self.unsetSilverBall()
			elif(self.invicible and self.positiony>self.playfield.height-10):
				self.positiony=self.positiony=self.playfield.height-10
				self.verticalSwap()
				self.unsetSilverBall()
			elif(self.positiony>self.playfield.y+self.playfield.height):
				self.balllost = True
				self.xinc = 0
				self.yinc = 0
				self.kill()

		self.orientation = self.orientation%360

		self.rect.x = int(self.positionx)
		self.rect.y = int(self.positiony)

		self.deltaTime = self.deltaTime + ptime
		if self.deltaTime>=100:
			self.deltaTime = 0
			# animation si besoin

	def setPosition(self, x,y):
		self.positionx = x
		self.positiony = y
		self.rect = pygame.Rect(x,y,self.rect.width, self.rect.height)

	def setYPosition(self, y):
		self.positiony = y
		self.rect = pygame.Rect(self.rect.x,y,self.rect.width, self.rect.height)

	def isBallLost(self):
		return self.balllost

	def isInvicible(self):
		return self.invicible

	def setInvicible(self):
		self.invicible = True

	def unsetInvicible(self):
		self.invicible = False

	def launch(self, orientation, velocity):
		if(orientation<0):
			orientation +=360
		self.orientation = orientation%360
		self.velocity = min(max(velocity,0),8)

	def goToPreviousPosition(self):
		self.positionx = self.previouspositionx
		self.positiony = self.previouspositiony
		self.rect.x = int(self.positionx)
		self.rect.y = int(self.positiony)

	def smallMove(self):
		self.previouspositionx = self.positionx
		self.previouspositiony = self.positiony

		xinc = math.cos(self.orientation*2*3.14/360)
		yinc = -math.sin(self.orientation*2*3.14/360)

		self.positionx += xinc
		self.positiony += yinc

		if(self.positionx<self.playfield.x):
			self.positionx=self.playfield.x
			self.horizontalSwap()
		elif(self.positionx>self.playfield.x+self.playfield.width):
			self.positionx=self.playfield.x+self.playfield.width
			self.horizontalSwap()

		if(self.positiony<self.playfield.y):
			self.positiony=self.playfield.y
			self.verticalSwap()
		elif(self.invicible and self.positiony>self.playfield.height-20):
			self.positiony=self.positiony=self.playfield.height-20
			self.verticalSwap()
		elif(self.positiony>self.playfield.y+self.playfield.height):
			self.balllost = True
			self.xinc = 0
			self.yinc = 0
			self.kill()

		self.orientation = self.orientation%360

		self.rect.x = int(self.positionx)
		self.rect.y = int(self.positiony)

	# Pour accrocher la balle à la raquette
	def stick(self, vaus):
		self.vaus = vaus
		self.stickdeltax = self.positionx-vaus.rect.x # l'endroit ou accrocher la raquette
		if(self.stickdeltax<0 or self.stickdeltax>vaus.rect.width):
			self.stickdeltax = vaus.rect.width/2-Ball.WIDTH # si la balle n'etait pas au dessus de la raquette on la pose dessus
		self.positiony = vaus.rect.y-self.HEIGHT # on pose la balle sur la raquette

		if(self.orientation>180): # si la balle était en train de descendre, on la fera remonter
			self.verticalSwap()
		
		self.stickedTime = time.time() # date/heure courante en secondes
		self.sticked = True # on accroche la balle

	def unstick(self):
		self.sticked = False # on décroche la balle

	# on rebondit par rapport à la "normale" de la ligne horizontale
	def verticalSwap(self):
		self.appendSpeed(0.05) # on accelere très legerement à chaque collision		
		if(self.orientation>0 and self.orientation<180): # going up
			if(self.orientation>90): # UL => DL
				self.orientation += 180-(self.orientation-90)*2
			else:					# UR => DR
				self.orientation -= self.orientation*2
		else: 											# going down
			if(self.orientation>270): # DR => UR
				self.orientation += 180-(self.orientation-270)*2
			else:					# UL => DL
				self.orientation -= self.orientation*2
		self.orientation = self.orientation%360

	# on rebondit par rapport à la "normale" de la ligne verticale
	def horizontalSwap(self):
		self.appendSpeed(0.05) # on accelere très legerement à chaque collision		
		if(self.orientation>90 and self.orientation<270): # going left
			if(self.orientation>180): # DL => DR
				self.orientation +=180-(self.orientation-180)*2
			else:					# UL => UR
				self.orientation -=(self.orientation-90)*2
		else: 											# going right
			if(self.orientation>270): # DR => DL
				self.orientation -=(self.orientation-270)*2
			else:					# UR => UL
				self.orientation +=180-(self.orientation-180)*2
		self.orientation = self.orientation%360

	def liftLeft(self,effect):
		if(self.orientation>0 and self.orientation<180): #only if ball is going up
			self.orientation += effect
			self.orientation = min(max(self.orientation, 10), 170) # no horizontal effect please
			self.orientation = self.orientation%360

	def liftRight(self,effect):
		if(self.orientation>0 and self.orientation<180): #only if ball is going up
			self.orientation -= effect
			self.orientation = min(max(self.orientation, 10), 170) # no horizontal effect please
			self.orientation = self.orientation%360

	def	appendOrientation(self, deg):
		self.orientation += deg
		return self.orientation

	def	appendSpeed(self, speed):
		self.velocity += speed
		self.velocity = min(max(self.velocity,1),8)
		return self.velocity

	def getSpeed(self):
		return self.velocity

	def setSpeed(self, speed):
		self.velocity = speed
		self.velocity = min(max(self.velocity,0),8)
		return self.velocity

	def getOrientation(self):
		return self.orientation

	def getPosition(self):
		return self.rect

	def hitPosition(self, brick):
		# on récupère les coordonnées courantes et précédentes du centre de la balle
		ballpositionx = self.positionx+5
		ballpositiony = self.positiony+5
		ballpreviouspositionx = self.previouspositionx+5
		ballpreviouspositiony = self.previouspositiony+5

		# on fait calcul d'intersection entre la droite située au centre de la trajectoire de la balle et le rectangle
		position = self.innerhitPosition(brick, ballpositionx, ballpositiony, ballpreviouspositionx, ballpreviouspositiony)
		if(position != None):
			return position

		# si cela n'a pas abouti c'est que c'est un "bord" de la balle qui a touché
		orientation = self.orientation+90 # on calcule le deplacement pour aller sur les bords de la balle
		orientation = orientation%360 #en tenant compte de la direction de la balle
		dx=math.cos(orientation*2*3.14/360)
		dy=-math.sin(orientation*2*3.14/360)

		for i in range (1,6): # on élargi petit à petit les rayons
			# on fait calcul d'intersection entre la droite située sur un des bords de la balle et le rectangle
			position = self.innerhitPosition(brick, ballpositionx-dx*i, ballpositiony-dy*i, ballpreviouspositionx-dx*i, ballpreviouspositiony-dy*i)
			if(position != None):
				return position

			# on fait calcul d'intersection entre la droite située sur l'autre bord de la balle et le rectangle
			position = self.innerhitPosition(brick, ballpositionx+dx*i, ballpositiony+dy*i, ballpreviouspositionx+dx*i, ballpreviouspositiony+dy*i)
			if(position != None):
				return position

		return 'bottom' # ne devrait jamais arriver...

	def innerhitPosition(self, brick, ballpositionx, ballpositiony, ballpreviouspositionx, ballpreviouspositiony):
		# on récupère les coordonnées de la brique
		left = brick.x # X
		right = brick.x+brick.width # X
		top = brick.y # y
		bottom = brick.y+brick.height # y

		deltay = ballpositiony-ballpreviouspositiony
		deltax = ballpositionx-ballpreviouspositionx 

		solutions = list()
		if(deltax==0 and deltay==0): # ce cas ne devrait pas arriver car cela signifie que la balle ne bouge pas... on renvoi alors arbitrairement un collision en dessous de la brique
			return 'bottom'
		elif(deltax==0): # mouvement vertical de la brique
			if(deltay>0):
				return 'top' # la balle descend c'est donc forcement une collision sur le dessus
			else:
				return 'bottom'
		elif(deltay==0): # mouvement horizontal de la brique
			if(deltax>0):
				return 'left' # la balle va de gauche à droite, c'est donc forcement une collision sur la gauche
			else:
				return 'right'
		else:
			# dans tous les autres cas on va calculer l'intersection de la droite de direction de la balle avec les segments qui entourent la brique
			# puis on va comparer la distance entre la position avant collision et les murs
			# la distance la plus courte correspond à la collision

			# on calcule l'equation de la droite
			a = (deltay)/(deltax)
			b = ballpreviouspositiony-a*ballpreviouspositionx

			# on calcule l'intersection de cette droite avec les bords de la brique
			# bord gauche
			xint = left
			yint = a*xint+b
			if(yint>=brick.y and yint<=brick.y+brick.height): # l'intersection est dans la brique
				distance = (ballpreviouspositionx-xint)*(ballpreviouspositionx-xint)+(ballpreviouspositiony-yint)*(ballpreviouspositiony-yint)
				solutions.append((distance,'left')) # on stocke dans la liste de résultats le carré de la distance entre la position de la balle avant collision et la brique, ainsi que le coté correspondant
			# bord droit
			xint = right
			yint = a*xint+b
			if(yint>=brick.y and yint<=brick.y+brick.height): # l'intersection est dans la brique
				distance = (ballpreviouspositionx-xint)*(ballpreviouspositionx-xint)+(ballpreviouspositiony-yint)*(ballpreviouspositiony-yint)
				if(len(solutions)>0): # il y avait deja au moins une intersection
					saveddistance, savedwall = solutions[0]
					if(distance<saveddistance): # on insere en tete
						solutions.insert(0, (distance,'right')) # on stocke dans la liste de résultats le carré de la distance entre la position de la balle avant collision et la brique, ainsi que le coté correspondant
				else:
					solutions.insert(0, (distance,'right')) # on stocke dans la liste de résultats le carré de la distance entre la position de la balle avant collision et la brique, ainsi que le coté correspondant
			# bord haut
			yint = top
			xint = (yint-b)/a
			if(xint>=brick.x and xint<=brick.x+brick.width): # l'intersection est dans la brique
				distance = (ballpreviouspositionx-xint)*(ballpreviouspositionx-xint)+(ballpreviouspositiony-yint)*(ballpreviouspositiony-yint)
				if(len(solutions)>0): # il y avait deja au moins une intersection
					saveddistance, savedwall = solutions[0]
					if(distance<saveddistance): # on insere en tete
						solutions.insert(0, (distance,'top')) # on stocke dans la liste de résultats le carré de la distance entre la position de la balle avant collision et la brique, ainsi que le coté correspondant
				else:
					solutions.insert(0, (distance,'top')) # on stocke dans la liste de résultats le carré de la distance entre la position de la balle avant collision et la brique, ainsi que le coté correspondant
			# bord bas
			yint = bottom
			xint = (yint-b)/a
			if(xint>=brick.x and xint<=brick.x+brick.width): # l'intersection est dans la brique
				distance = (ballpreviouspositionx-xint)*(ballpreviouspositionx-xint)+(ballpreviouspositiony-yint)*(ballpreviouspositiony-yint)
				if(len(solutions)>0): # il y avait deja au moins une intersection
					saveddistance, savedwall = solutions[0]
					if(distance<saveddistance): # on insere en tete
						solutions.insert(0, (distance,'bottom')) # on stocke dans la liste de résultats le carré de la distance entre la position de la balle avant collision et la brique, ainsi que le coté correspondant
				else:
					solutions.insert(0, (distance,'bottom')) # on stocke dans la liste de résultats le carré de la distance entre la position de la balle avant collision et la brique, ainsi que le coté correspondant
			
			# on retourne la solution
			if(len(solutions)>0):
				saveddistance, savedwall = solutions[0]
				return savedwall
			else: 
				return None

	def setSilverBall(self):
		'''Silver balls can break standard bricks without bouncing'''
		self.silverball = True

	def unsetSilverBall(self):
		'''Silver balls can break standard bricks without bouncing'''
		self.silverball = False

	def isSilverBall(self):
		'''Silver balls can break standard bricks without bouncing'''
		return self.silverball