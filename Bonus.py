import pygame

class Bonus(pygame.sprite.Sprite):
	#les types de brique
	LASER  = 0
	ENLARGE  = 1
	CATCH  = 2
	SLOW  = 3
	REDUCE  = 4
	DISRUPTION  = 6
	BREAK  = 7
	TORPEDO  = 8 # Traverse les briques!
	PLAYER  = 9

	# la taille d'une brique
	WIDTH = 44
	HEIGHT=22
	HGAP = 0
	VGAP = 2

	# les briques
	spriteSheet = pygame.image.load("./levels/sprites/sprites.png")

	# matrice de 15*2 briques
	sequences = [	
		(0*8,8,True), # L aser
		(1*8,8,True), # E enlarge
		(2*8,8,True), # C atch
		(3*8,8,True), # S low
		(4*8,8,True), # R educe
		(5*8,8,True), # M
		(6*8,8,True), # D isruption
		(7*8,8,True), # B reak
		(8*8,8,True), # T
		(9*8,8,True), # P layer
	]

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.numeroSequence = 0
		self.numeroImage = 0

		self.rect = pygame.Rect(0,0,Bonus.WIDTH,Bonus.HEIGHT)
		self.image = Bonus.spriteSheet.subsurface(pygame.Rect(0,326,Bonus.WIDTH,Bonus.HEIGHT))
		self.mask = None

		self.deltaTime = 0

	def update(self,time):
		# on calcule l'image à afficher
		n = Bonus.sequences[self.numeroSequence][0]+self.numeroImage
		self.image = Bonus.spriteSheet.subsurface(pygame.Rect(n%8*(Bonus.WIDTH+Bonus.HGAP),326+n//8*(Bonus.HEIGHT+Bonus.VGAP),Bonus.WIDTH,Bonus.HEIGHT))
		if(self.mask == None):
			self.mask = pygame.mask.from_surface(self.image)

		# on descend le bonus
		self.rect = self.rect.move(0,1)
		if(self.rect.y>480): # le bonus est sorti de l'écran, on le fait disparaitre
			self.kill()

		# on fait une petite animation
		self.deltaTime = self.deltaTime + time
		if self.deltaTime>=100:
			self.deltaTime = 0

			self.numeroImage = self.numeroImage+1
			
			if self.numeroImage == Bonus.sequences[self.numeroSequence][1]:
				if Bonus.sequences[self.numeroSequence][2]:
					self.numeroImage = 0
				else:
					self.numeroImage = self.numeroImage-1

	def setPosition(self, x,y):
		self.rect = pygame.Rect(x,y,self.rect.width, self.rect.height)

	def setBonusType(self, bonusType):
		'''
		Laser	Collect the red capsule to transform the Vaus into its Laser-firing configuration. In this form, you can fire lasers at the top of the screen by pushing the fire button. Lasers can be used against every brick except Gold bricks, and against enemies. Silver bricks can only be destroyed by lasers when they are hit the required number of times.\n
		Enlarge	Collect the blue capsule to extend the width of the Vaus.\n
		Catch	Collect the green capsule to gain the catch ability. When the ball hits the Vaus, it will stick to the surface. Press the Fire button to release the ball. The ball will automatically release after a certain period of time has passed.\n
		Slow	Collect the orange capsule to slow the velocity at which the ball moves. Collecting multiple orange capsules will have a cumulative effect and the ball velocity can become extremely slow. However, the ball velocity will gradually increase as it bounces and destroys bricks. The velocity may sometimes suddenly increase with little warning.\n
		Reduce	Collect the black capsule toreduce the width of the Vaus.\n
		Break	Collect the violet capsule to create a "break out" exit on the right side of the stage. Passing through this exit will cause you to advance to the next stage immediately, as well as earn a 10,000 point bonus.\n
		Disruption	Collect the cyan capsule to cause the ball to split into three instances of itself. All three balls can be kept aloft. There is no penalty for losing the first two balls. No colored capsules will fall as long as there is more than one ball in play. This is the only power up that, while in effect, prevents other power ups from falling.\n
		Player	Collect the gray capsule to earn an extra Vaus.\n
		'''
		if(bonusType<0 or bonusType>=len(Bonus.sequences)):
			bonusType=0
		self.numeroSequence = bonusType

	def getBonusType(self):
		'''
		Laser	Collect the red capsule to transform the Vaus into its Laser-firing configuration. In this form, you can fire lasers at the top of the screen by pushing the fire button. Lasers can be used against every brick except Gold bricks, and against enemies. Silver bricks can only be destroyed by lasers when they are hit the required number of times.\n
		Enlarge	Collect the blue capsule to extend the width of the Vaus.\n
		Catch	Collect the green capsule to gain the catch ability. When the ball hits the Vaus, it will stick to the surface. Press the Fire button to release the ball. The ball will automatically release after a certain period of time has passed.\n
		Slow	Collect the orange capsule to slow the velocity at which the ball moves. Collecting multiple orange capsules will have a cumulative effect and the ball velocity can become extremely slow. However, the ball velocity will gradually increase as it bounces and destroys bricks. The velocity may sometimes suddenly increase with little warning.\n
		Reduce	Collect the black capsule toreduce the width of the Vaus.\n
		Break	Collect the violet capsule to create a "break out" exit on the right side of the stage. Passing through this exit will cause you to advance to the next stage immediately, as well as earn a 10,000 point bonus.\n
		Disruption	Collect the cyan capsule to cause the ball to split into three instances of itself. All three balls can be kept aloft. There is no penalty for losing the first two balls. No colored capsules will fall as long as there is more than one ball in play. This is the only power up that, while in effect, prevents other power ups from falling.\n
		Player	Collect the gray capsule to earn an extra Vaus.\n
		'''
		return self.numeroSequence
