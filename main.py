# #####################################################################################
#
# Un exemple de jeu arkanoid en Python
#
#
# #####################################################################################

# Ne pas oublier d'installer les librairies manquantes:
# pip install pygame
# pip install pytmx

import sys,random,time,pygame,pytmx
from pygame.sprite import collide_mask, collide_rect 

from tkhelpers import *
from colliders import *

from Vaus import Vaus
from Brick import Brick
from Ball import Ball
from Bonus import Bonus
from Life import Life
from Bullet import Bullet
from Enemy import Enemy
from Explosion import Explosion
from Particle import Particle
from TextOverlay import TextOverlay
from Hiscore import HiScore

if __name__ != '__main__': 
	exit() # on sort si on a pas executé ce script car c'est certainement une erreur, il ne DOIT PAS etre importé dans un autre script

# Paramètres principaux du jeu
WIDTH = 640 # ATTENTION : on double la résolution écran par rapport à la resolution du jeu lorsque l'on est pas en FULLSCREEN (1280x960)
HEIGHT = 480
FPS = 60 
FULLSCREEN = True
TITLE = "ArkanoPy"
PLAYERNAME = None
LIFES = 3
INVINCIBLE = False # pour les tests...

# NOM DU JOUEUR
# -------------
# Le nom du joueur est passé en parametre de ligne de commande
if(len(sys.argv)>1):
	PLAYERNAME = sys.argv[1]
# sinon on demande le nom du joueur
if(PLAYERNAME == None):
	PLAYERNAME = tk_askstring("Quel est ton prénom?\t\t\t\t\t\t", "Julien")

if(PLAYERNAME == None):
	sys.exit(0) # click sur Cancel? on sort du programme
elif len(PLAYERNAME)==0:
	PLAYERNAME = "Anonyme" # Par défaut on met Anonyme
else:
	PLAYERNAME = PLAYERNAME[:20] # on prend les 20 premiers caractères 

# On initialise les variables du jeu
pygame.init()
pygame.mixer.init()
playfield = pygame.Rect(34,20,640-34*2, 480-20)

if(FULLSCREEN):
	screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF, vsync=1)
else:
	screen = pygame.display.set_mode((WIDTH*2,HEIGHT*2))

pygame.display.set_caption(TITLE)

levels = [
	'./levels/level1.tmx',
	'./levels/level2.tmx',
	'./levels/level3.tmx', 
	'./levels/level4.tmx',
	'./levels/level5.tmx',
	'./levels/level6.tmx',
	'./levels/level7.tmx',
	'./levels/level8.tmx',
	'./levels/level9.tmx',
	'./levels/level10.tmx',
	'./levels/level11.tmx',
	'./levels/level12.tmx',
	'./levels/level13.tmx',
	'./levels/level14.tmx',
	'./levels/level15.tmx',
	'./levels/level16.tmx',
	'./levels/level17.tmx',
	'./levels/level18.tmx',
	'./levels/level19.tmx',
	'./levels/level20.tmx',
	'./levels/level21.tmx',
	'./levels/level22.tmx',
	'./levels/level23.tmx',
	'./levels/level24.tmx',
	'./levels/level25.tmx',
	'./levels/level26.tmx',
	'./levels/level27.tmx',
	'./levels/level28.tmx',
	'./levels/level29.tmx',
	'./levels/level30.tmx',
	'./levels/level31.tmx',
	'./levels/level32.tmx',
]

# Cette table contient les bonus disponibles par niveau, pour "pondérer"  la chance il suffit de faire apparaitre un meme bonus plusieurs fois dans la ligne correspondate
# La ligne correspondant au niveau est utilisée pour tirer au hasard un bonus en tirant un nombre compris entre 0 et taille du tableau-1
# premiere valeur : une chance sur X que la brique donne un bonus
# deuxieme valeur : la tale pour le tirage au sort du bonus
bonustable = [
	(2, [Bonus.LASER, Bonus.LASER, Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.CATCH, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO]), # Level 1
	(1, [Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.DISRUPTION, Bonus.DISRUPTION, Bonus.DISRUPTION, Bonus.DISRUPTION, Bonus.DISRUPTION, Bonus.DISRUPTION, Bonus.BREAK, Bonus.BREAK, Bonus.BREAK, Bonus.BREAK, Bonus.BREAK, Bonus.BREAK]), # Level 1
	(1, [Bonus.LASER, Bonus.LASER, Bonus.LASER, Bonus.LASER, Bonus.LASER, Bonus.LASER, Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 1
	(2, [Bonus.LASER, Bonus.ENLARGE, Bonus.CATCH, Bonus.SLOW, Bonus.REDUCE, Bonus.DISRUPTION, Bonus.BREAK, Bonus.TORPEDO, Bonus.PLAYER]), # Level 32
]


layers = [
		("white", Brick.WHITE), 
		("orange", Brick.ORANGE), 
		("cyan", Brick.CYAN), 
		("green", Brick.GREEN), 
		("silver", Brick.SILVER), 
		("red", Brick.RED), 
		("blue", Brick.BLUE), 
		("magenta", Brick.MAGENTA), 
		("yellow", Brick.YELLOW), 
		("gold", Brick.GOLD)
]



# on cache le curseur de la souris
pygame.mouse.set_visible(False)


# ##################################################
# ##################################################
# Ecran d'accueil
# ##################################################
# ##################################################

while True:
	splashscreen = pygame.image.load("./background/splashscreen.png").convert_alpha()
	if(FULLSCREEN):
		screenbuffer = splashscreen
	else:
		screenbuffer = pygame.transform.scale2x(splashscreen) # on double la taille de l'image avant de l'afficher
	screen.blit(screenbuffer, pygame.Rect(0,0,screenbuffer.get_width(),screenbuffer.get_height()))

	pygame.mixer.music.load('./soundtracks/original/01_-_Arkanoid_-_ARC_-_Start_Demo.ogg')
	pygame.mixer.music.play()

	clock = pygame.time.Clock()
	next = False
	while not next:
		# on limite l'affichage à FPS images par secondes
		elapsedtime = clock.tick(FPS)	
		
		# on gère les evenements clavier
		###################
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				next = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					next = True
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit(0)

		# on met à jour l'affichage ecran
		pygame.display.update()

	pygame.mixer.music.stop()

	# ####################################################
	# initialisation des variables du jeu


	# niveau de départ
	currentlevel = 0
	score = 0
	nblife = LIFES
	nblife = min(nblife, 8) # 8 vies max

	while(nblife>0):
		# les overlays
		overlays = pygame.sprite.RenderClear()

		scoreWidget = TextOverlay()
		scoreWidget.setSize(32)
		scoreWidget.setText(str(score).zfill(6))
		scoreWidget.setPosition(50,10)
		overlays.add(scoreWidget)

		levelWidget = TextOverlay()
		levelWidget.setSize(32)
		levelWidget.setPosition(280,10)
		overlays.add(levelWidget)

		debugWidget = TextOverlay()
		debugWidget.setSize(24)
		debugWidget.setPosition(560,460)
		#overlays.add(debugWidget)

		lifeGroup = pygame.sprite.RenderClear()
		for i in range (nblife):
			life = Life()
			life.setPosition(560-i*24, 10)
			lifeGroup.add(life)

		gameover = False
		while not gameover:
			# raquette
			vaus = Vaus(playfield)
			vausGroup = pygame.sprite.RenderClear()
			vausGroup.add(vaus)

			# On charge le niveau
			tm = pytmx.load_pygame(levels[currentlevel])

			tileWidth = tm.tilewidth
			tileHeight = tm.tileheight

			#on initialise le groupe qui contient le bonus en cours
			ongoingbonus = pygame.sprite.RenderClear()
			(bonusrandvalueforlevel, bonusrandtableforlevel)= bonustable[currentlevel] # on récupère les informations pour faire le tirage aléatoire en fonction du niveau

			# on initialise le groupe qui contient les munitions
			ongoingbullets = pygame.sprite.RenderClear()

			# on initialise le groupe qui contient les enemis
			ongoingenemies = pygame.sprite.RenderClear()

			# on initialise le groupe qui contient les explosions
			ongoingexplosions = pygame.sprite.RenderClear()

			# on initialise le groupe qui contient les particules
			particleGroup = pygame.sprite.RenderClear()

			# on charge et on positionne l'ensemble des briques
			bricks = pygame.sprite.RenderClear()
			breakablebricks = pygame.sprite.RenderClear()

			for (layername, bricktype) in layers:
				layer = tm.get_layer_by_name(layername)
				for x,y,image in layer.tiles():
					brick = Brick(currentlevel+1)
					brick.setBrickType(bricktype)
					brick.setPosition(x*Brick.WIDTH-10, y*Brick.HEIGHT)
					bricks.add(brick)
					if(brick.isBreakable()):
						breakablebricks.add(brick)


			# ##################################################
			# ##################################################
			# Boucle principale du jeu
			# ##################################################
			# ##################################################
			buffer = pygame.Surface((WIDTH, HEIGHT),32)
			buffer.convert_alpha()
			bck = "./background/background"+str(1+currentlevel%5)+".png"
			background = pygame.image.load(bck).convert_alpha()
			border = pygame.image.load("./background/borders.png").convert_alpha()
			background.blit(border, pygame.Rect(0,0,background.get_width(),background.get_height()))

			buffer.blit(background, pygame.Rect(0,0,background.get_width(),background.get_height()))

			ball = Ball(playfield)
			ball.setPosition(640/2,400)
			ball.stick(vaus) # on accroche la balle a la raquette
			ball.launch(60,3) # orientation initiale du tir
			if(INVINCIBLE):
				ball.setInvicible()
			balls = pygame.sprite.RenderClear()
			balls.add(ball)

			enemycount = 0 #compteur pour trouver l'emplacement de la prochaine apparition de l'enemi
			enemytimer = 0 #timer qui permet de faire une pause avant la réapparition d'un ennemi 
			nbenemis = min(1+(currentlevel+1)//5,3) # entre 1 et 3 ennemis. 2 ennemis a partir du 5 eme niveau, 3 ennemis a partir du 10eme... 

			clock = pygame.time.Clock()
			nextlevel = False
			introDone = False
			while not gameover and not nextlevel:
				# on limite l'affichage à FPS images par secondes
				elapsedtime = clock.tick(FPS)	
				
				# on gère les evenements clavier
				###################
				for event in pygame.event.get():
					if event.type == pygame.QUIT: 
						pygame.quit()
						sys.exit(0)
					elif event.type == pygame.MOUSEBUTTONDOWN:
						if(vaus.getVausType() == Vaus.LASERVAUS): # on tire
							bullet = Bullet(playfield)
							bullet.setPosition(vaus.rect.x+16, vaus.rect.y)
							ongoingbullets.add(bullet)
							bullet = Bullet(playfield)
							bullet.setPosition(vaus.rect.x+vaus.rect.width-22, vaus.rect.y)
							ongoingbullets.add(bullet)
							bullet.playSound()
						else:
							for ball in balls:
								ball.unstick()
					elif event.type == pygame.MOUSEMOTION:
						x_rel, y_rel = pygame.mouse.get_rel()
						vaus.move(x_rel*2) # on accelere le mouvement de la souris
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_n:
							nextlevel = True
						if event.key == pygame.K_i:
							INVINCIBLE = not INVINCIBLE
							i=0
							for ball in balls: # on reinitialise l'état 'invicible' de la premiere balle
								if(i==0):
									if(INVINCIBLE):
										ball.setInvicible()
									else:
										ball.unsetInvicible()
								else:
									ball.unsetInvicible()
								i+=1

						if event.key == pygame.K_l:
							if(nblife<8):
								life = Life()
								life.setPosition(560-nblife*24, 10)
								lifeGroup.add(life)
								nblife += 1
								nblife = min(nblife, 8)
						if event.key == pygame.K_a:
							nblife=0
							gameover = True
						if event.key == pygame.K_ESCAPE:
							exit()

				if(enemytimer>0):
					enemytimer -= 1
				# on fait apparaitre un ennemi si besoin
				if(enemytimer==0):
					if(len(ongoingenemies)<nbenemis):
						if(enemycount%3==0):
							enemy = Enemy(playfield)
							enemy.setEnemyType(random.randint(0,5))
							enemy.setPosition(Brick.WIDTH*3-10,Brick.HEIGHT-2)
							ongoingenemies.add(enemy)
						elif(enemycount%3==1):
							enemy = Enemy(playfield)
							enemy.setEnemyType(random.randint(0,5))
							enemy.setPosition(WIDTH/2,Brick.HEIGHT-2)
							ongoingenemies.add(enemy)
						else:
							enemy = Enemy(playfield)
							enemy.setEnemyType(random.randint(0,5))
							enemy.setPosition(WIDTH-Brick.WIDTH*3-20,Brick.HEIGHT-2)
							ongoingenemies.add(enemy)
						enemycount += 1
						enemytimer = 300

				# on met a jour les widgets de vies et de niveau
				levelWidget.setText("level "+str(currentlevel+1))

				# on génère des particules derriere la balle si besoin
				for ball in balls:
					if(ball.isSilverBall()):
						for i in range(0,10):
							particle = Particle(FPS, playfield)
							particle.setPositionCenter(ball.rect.centerx, ball.rect.centery)
							particle.setDirection((180+ball.getOrientation())%360)
							particleGroup.add(particle)

				# on met a jour les briques
				###################
				ongoingbullets.update(elapsedtime)
				bricks.update(elapsedtime)
				vausGroup.update(elapsedtime)
				balls.update(elapsedtime)
				overlays.update(elapsedtime)
				ongoingbonus.update(elapsedtime)
				lifeGroup.update(elapsedtime)
				ongoingenemies.update(elapsedtime)
				ongoingexplosions.update(elapsedtime)
				particleGroup.update(elapsedtime)

				# collisions
				############

				# on teste la collision entre les balles et les ennemis
				ballhits = pygame.sprite.groupcollide(balls, ongoingenemies, False, False, collide_mask)
				for ballhit in ballhits: # si des balles ont touché des ennemis
					enemyhits = []
					ballhit.goToPreviousPosition() #marche arriere toute...
					secu = 50
					while(len(enemyhits)==0 and secu>0):
						ballhit.smallMove() # on avance pas à pas pour aller jusqu'à la collision
						enemyhits = pygame.sprite.spritecollide(ballhit, ongoingenemies, False, collide_mask)
						secu -=1 # par sécurité pour eviter une boucle infinie (qui ne ne ddevrait jamais arriver en theorie)
					if(secu==0):
						# erreur! nous n'avons finalement pas trouvé de collision...
						break

					rect = enemyhits[0].rect # on récupère le rectangle sur lequel affiner le test de collision
					enemyhit = enemyhits[0] # on récupère l'ennemi en question (meme si il y en a plusieurs on ne récupère que la premiere...)

					wall = ballhit.hitPosition(rect) # on récupère le coté de la collision pour savoir comment la balle rebondit
					if(wall=='left' or wall=='right'):
						ballhit.horizontalSwap()
					else:
						ballhit.verticalSwap()
					ballhit.goToPreviousPosition() # on repositionne la balle juste avant la collision
					if(enemyhit.injured()):  # on indique à la brique qu'elle est touchée
						explosion = Explosion(FPS,enemyhit)
						ongoingexplosions.add(explosion)
						enemytimer = 300

				# on teste la collision entre les balles et les briques
				ballhits = pygame.sprite.groupcollide(balls, bricks, False, False, collide_circle_rect)
				for ballhit in ballhits: # si des balles ont touché des briques
					brickhits = []
					ballhit.goToPreviousPosition() #marche arriere toute...
					secu = 50
					while(len(brickhits)==0 and secu>0):
						ballhit.smallMove() # on avance pas à pas pour aller jusqu'à la collision
						brickhits = pygame.sprite.spritecollide(ballhit, bricks, False, collide_circle_rect)
						secu -=1 # par sécurité pour eviter une boucle infinie (qui ne ne ddevrait jamais arriver en theorie)
					if(secu==0):
						# erreur! nous n'avons finalement pas trouvé de collision...
						break

					# on récupère le rectangle sur lequel affiner le test de collision
					if(len(brickhits)==1):
						rect = brickhits[0].rect
					elif(len(brickhits)==2): # cas tres particulier ou la balle a tapé entre deux briques
						if(brickhits[0].rect.x == brickhits[1].rect.x or brickhits[0].rect.y == brickhits[1].rect.y): # deux briques alignées
							rect = brickhits[0].rect.union(brickhits[1].rect)
						else:
							rect = brickhits[0].rect
					brickhit = brickhits[0] # on récupère la brique en question (meme si il y en a plusieurs on ne récupère que la premiere...)

					score += brickhit.getScore()*(2 if vaus.getVausType()==vaus.REDUCEVAUS else 1) # on met a jour le score (doublé si la barre est réduite)

					silverball = ballhit.isSilverBall() # on regarde si nous avons une balle normale ou une "silver bullet"
					breakablebrick = brickhit.isBreakable() # on regarde si la brique peut etre cassée
					canlaunchbonus = False

					if(silverball and breakablebrick): # nous avons une balle qui peut casser les briques "standard sans rebondir"
						brickhit.destroy()
						canlaunchbonus = True
					else: # nous avons une balle normale qui rebondie (ou une brique incassable)
						wall = ballhit.hitPosition(rect) # on récupère le coté de la collision pour savoir comment la balle rebondit
						if(wall=='left' or wall=='right'):
							ballhit.horizontalSwap()
						else:
							ballhit.verticalSwap()
						ballhit.goToPreviousPosition() # on repositionne la balle juste avant la collision
						if(brickhit.injured()): # on indique à la brique qu'elle est touchée
							canlaunchbonus = True

					if(canlaunchbonus): # on a cassé une brique, on peut donc tirer au sort pour savoir si il faut lancer un bonus
						if(len(ongoingbonus)==0 and len(balls)==1): # seulement si il n'y a pas deja un bonus en cours de descente et qu'il y a une seule balle en jeu
							if(random.randint(0,bonusrandvalueforlevel-1)==0): # un chance sur bonusrandvalueforlevel
								bonus = Bonus()	# on créé un bonus
								bonustype = random.randint(0, len(bonusrandtableforlevel)-1) # on tire au hasard un bonus dans la liste correspondant au niveau
								bonus.setBonusType(bonusrandtableforlevel[bonustype])
								bonus.setPosition(brickhit.rect.x-1, brickhit.rect.y)
								ongoingbonus.add(bonus)

				# on teste la collision entre les munitions et les ennemis
				bullethits = pygame.sprite.groupcollide(ongoingbullets, ongoingenemies, True, False, collide_point_rect)
				for bullethit in bullethits: # si des munitions ont touché des enemis
					enemyhits = bullethits[bullethit]
					for enemyhit in enemyhits: # on récupère la liste des enemis touchés par la munition	
						if(enemyhit.injured()): # et on indique à l'enemi qu'il a été touché 
							explosion = Explosion(FPS,enemyhit)
							ongoingexplosions.add(explosion)
							enemytimer = 300

				# on teste la collision entre les munitions et les briques
				bullethits = pygame.sprite.groupcollide(ongoingbullets, bricks, True, False, collide_point_rect)
				for bullethit in bullethits: # si des munitions ont touché des briques
					brickhits = bullethits[bullethit]
					for brickhit in brickhits: # on récupère la liste des briques touchées par la munition	
						score += brickhit.getScore() # on met a jour le score
						brickhit.injured() # et on indique à la brique qu'elle a été touchée 

				# on teste la collision entre les ennemis et les briques
				enemyhits = pygame.sprite.groupcollide(ongoingenemies, bricks, False, False, collide_rect)
				for enemyhit in enemyhits: # si des enemis ont touché des briques
					i=0
					while(i<100 and len(pygame.sprite.spritecollide(enemyhit, bricks, False, collide_rect))>0):
						enemyhit.fastForward()
						i+=1
					if(i==100): # si on a pas réussi a trouver une trajectoire qui ne collisionne pas au bout de 100 itérations...
						enemyhit.goToPreviousPosition()
				# on teste la collision entre la raquette et la balle
				collisionlist = pygame.sprite.spritecollide(vaus,balls,False, pygame.sprite.collide_mask)
				for ball in collisionlist: # collision détectée
					vaus.playBouncingSound()
					ball.goToPreviousPosition()
					(effect, direction) = vaus.getBallEffect(ball)
					ball.verticalSwap()
					if(direction=="left"):
						ball.liftLeft(effect)
					elif(direction=='right'):
						ball.liftRight(effect)
					ball.setYPosition(480 - 41) # on repositionne la balle au dessus de la raquette
					if(vaus.getVausType()==Vaus.CATCHVAUS): # si le vaisseau à la "colle" comme bonus, on colle la balle au vaisseau
						ball.stick(vaus)

				# on teste la collision entre la raquette et les ennemis
				collisionlist = pygame.sprite.spritecollide(vaus,ongoingenemies,True, pygame.sprite.collide_mask)
				for enemy in collisionlist: # collision détectée
					explosion = Explosion(FPS, enemy)
					ongoingexplosions.add(explosion)
					enemytimer = 300

				# on teste la collision entre la raquette et un bonus
				collisionlist = pygame.sprite.spritecollide(vaus,ongoingbonus,True, collide_rect)
				if(len(collisionlist)>0): # collision détectée
					catchedbonus = collisionlist[0]
					bonustype = catchedbonus.getBonusType() # on récupère le bonus
					vaus.setBonus(bonustype) # on indique au vaisseau que l'on a attrapé un bonus
					if(bonustype !=Bonus.CATCH): # on libere les balles acrrochées à la raquette si on a attrapé un autre bonus
						for ball in balls:
							ball.unstick()
					if(bonustype !=Bonus.TORPEDO): # on enleve l'effet "silver bullet" si on a attrapé aute chose qu'un Torpedo
						for ball in balls:
							ball.unsetSilverBall()
					if(bonustype == Bonus.BREAK): # on passe au niveau suivant
						nextlevel = True
					elif(bonustype == Bonus.PLAYER): # on gagne une vie
						if(nblife<8):
							life = Life()
							life.setPosition(560-nblife*24, 10)
							lifeGroup.add(life)
							nblife += 1
							nblife = min(nblife, 8) # 8 vies max
					elif(bonustype == Bonus.SLOW): # on ralenti les balles
						for ball in balls:
							ball.appendSpeed(-3)
					elif(bonustype == Bonus.TORPEDO): # on transforme les balles en "silver bullets"
						for ball in balls:
							ball.setSilverBall()
					elif(bonustype == Bonus.DISRUPTION): # on lance deux autres balles
						currentballspeed = 3
						currentballorientation = 60
						currentballposition = pygame.Rect(0,0,0,0)
						if(len(balls)>0):
							for currentball in balls:
								currentballspeed = currentball.getSpeed() # on récupère la vitesse de la balle courante
								currentballposition = currentball.rect
								currentballorientation = currentball.getOrientation()
								break
						# deuxieme balle
						ball = Ball(playfield)
						ball.setPosition(currentballposition.x, currentballposition.y)
						ball.launch(currentballorientation+30,currentballspeed) # orientation initiale du tir
						balls.add(ball)
						# troisieme balle
						ball = Ball(playfield)
						ball.setPosition(currentballposition.x, currentballposition.y)
						ball.launch(currentballorientation-30,currentballspeed) # orientation initiale du tir
						balls.add(ball)

				# on met à jour le score si besoin
				scoreWidget.setText(str(score).zfill(6))

				# on affiche la map
				###################
				ongoingbullets.clear(buffer, background)
				balls.clear(buffer, background)
				bricks.clear(buffer, background)
				vausGroup.clear(buffer, background)
				ongoingbonus.clear(buffer, background)
				overlays.clear(buffer, background)
				lifeGroup.clear(buffer, background)
				ongoingenemies.clear(buffer, background)
				ongoingexplosions.clear(buffer, background)
				particleGroup.clear(buffer, background)

				particleGroup.draw(buffer)
				ongoingbullets.draw(buffer)
				balls.draw(buffer)
				bricks.draw(buffer)
				ongoingbonus.draw(buffer)
				ongoingenemies.draw(buffer)
				ongoingexplosions.draw(buffer)
				vausGroup.draw(buffer)
				overlays.draw(buffer)
				lifeGroup.draw(buffer)

				# on met à jour l'affichage ecran
				if(FULLSCREEN):
					screenbuffer = buffer
					screen.blit(screenbuffer, pygame.Rect(0,0,WIDTH,HEIGHT))
				else:
					screenbuffer = pygame.transform.scale2x(buffer) # on double la taille de l'image avant de l'afficher
					screen.blit(screenbuffer, pygame.Rect(0,0,WIDTH*2,HEIGHT*2))
				pygame.display.update()

				# plus de balles? game over...
				if(len(balls)==0):
					gameover = True

				# plus de briques à détruire? niveau suivant
				if(len(breakablebricks)==0):
					nextlevel = True

				# on joue la musique d'introduction si le niveau démarre...
				if(not introDone):
					introDone = True
					pygame.mixer.music.load('soundtracks/original/02_-_Arkanoid_-_ARC_-_Game_Start.ogg')
					pygame.mixer.music.play()
					pygame.time.delay(2000) 
					for event in pygame.event.get(): #on purge les evements
						if event.type == pygame.MOUSEMOTION:
							pygame.mouse.get_rel()

			# on passe au niveau suivant
			# ou on perd une vie et on recommence le niveau...
			if(gameover):
				nblife -= 1
			elif(nextlevel):
				currentlevel += 1
				currentlevel = currentlevel%len(levels)

	pygame.mixer.music.load('soundtracks/original/05_-_Arkanoid_-_ARC_-_Game_Over.ogg')
	pygame.mixer.music.play()
	pygame.time.delay(3000) 
	for event in pygame.event.get(): #on purge les evements
		nop = 1


	# ##################################################
	# ##################################################
	# Ecran de HiScore
	# ##################################################
	# ##################################################

	buffer = pygame.Surface((WIDTH, HEIGHT),32)
	buffer.convert_alpha()
	gameoverscreen = pygame.image.load("./background/gameover.png").convert_alpha()
	hiscorewidget = HiScore(FPS, playfield)
	# on insere le score du joueur
	# dans la table des HiScore
	hiscorewidget.addScore(score, PLAYERNAME)
	clock = pygame.time.Clock()
	starttime = time.time()
	next = False
	while not next:
		# on limite l'affichage à FPS images par secondes
		elapsedtime = clock.tick(FPS)	
		
		# on gère les evenements clavier
		###################
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				next = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					next = True
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit(0)

		hiscorewidget.update(elapsedtime)
		buffer.blit(gameoverscreen, pygame.Rect(0,0,gameoverscreen.get_width(),gameoverscreen.get_height()))
		buffer.blit(hiscorewidget.image, hiscorewidget.rect)

		if(FULLSCREEN):
			screenbuffer = buffer
			screen.blit(screenbuffer, pygame.Rect(0,0,WIDTH,HEIGHT))
		else:
			screenbuffer = pygame.transform.scale2x(buffer) # on double la taille de l'image avant de l'afficher
			screen.blit(screenbuffer, pygame.Rect(0,0,WIDTH*2,HEIGHT*2))

		# on met à jour l'affichage ecran
		pygame.display.update()
