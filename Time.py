#This file is almost IDENTICAL to MainGame.py except for a timer.  Please see MainGame.py for comments about how things work.
import time
import os
import platform
if platform.system() == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'

try:
    import pygame
    from pygame.locals import *
 
except ImportError, err:
    print "%s Failed to Load Module: %s" % (__file__, err)
    import sys
    sys.exit(1)

class Game(object):
    def __init__(self):
        pygame.init()
	global lives
        global platform
	global springs
        #window
        self.window=pygame.display.set_mode((800,600))
	self.menu=False
        # clock for ticking
        self.clock = pygame.time.Clock()
        
        # set the window title
        pygame.display.set_caption("Pygame Drawing")
        
        #Allows events
        pygame.event.set_allowed([QUIT,KEYDOWN,KEYUP])
        
        #Backgrounds
        self.background=pygame.Surface((800,600))
        self.background.fill((255,255,255))
        
        self.window.blit(self.background,(0,0))
        
        pygame.display.flip()
	self.exit=False
        
        #sprite rendering group
        self.sprites = pygame.sprite.RenderUpdates()
	
	levelGen(os.path.join("Levels",levels[level]))
        #create sprite
	
	
	self.sprites.add(platform)
	
	self.running=True
	self.timeEnd=False

        self.square=square((40,500))
        self.sprites.add(self.square)
    
	self.font=pygame.font.SysFont("Arial", 20, bold=False, italic=False)
        
    def run(self):
	start_time = time.time()
        while self.running: #runs
	    self.window.fill((255,255,255))
	    ti=elapsed_time = time.time() - start_time
            #ticks clock
            self.clock.tick(60)
            
            # handle pygame events -- if user closes game, stop running
            self.running = self.handleEvents()
            
            # update the title bar with our frames per second
	    x,y=pygame.mouse.get_pos()
		
            pygame.display.set_caption('Pygame Test   %i %i ' %(x,y))
            
            #updating sprites

	    self.sprites.update()
		
            # render our sprites
            self.sprites.clear(self.window, self.background)    # clears the window where the sprites currently are, using the background\
	    self.window.blit(self.font.render(str(round(ti,2)),1,((0,0,0))),(0,0))
	    self.window.blit(self.font.render("Press Esc to return to main menu",1,((0,0,0))),(0,550))
            dirty = self.sprites.draw(self.window)         # calculates the 'dirty' rectangles that need to be redrawn
            # blit the dirty areas of the screen
	    pygame.display.update(dirty)     # updates just the 'dirty' areas'
	    pygame.display.flip()


            
            
    def handleEvents(self):
	global lives
	global menu
        for event in pygame.event.get():
            if event.type == QUIT:
		self.exit=True
		self.menu=True
                return False
            
            #handle input
            elif event.type == KEYDOWN:
		if event.key==K_ESCAPE:
		    self.menu=True
		    return False
		if event.key==K_UP and self.menu==False:
                    self.square.jump()
                if event.key==K_DOWN and self.menu==False:
                    self.square.down()
                if event.key==K_LEFT and self.menu==False:
                    self.square.left()
                if event.key==K_RIGHT and self.menu==False:
                    self.square.right()
		
            elif event.type == KEYUP:
                if event.key==K_UP:
                    self.square.down()
                if event.key==K_DOWN:
                    self.square.down()
                if event.key==K_LEFT:
                    self.square.right()
                if event.key==K_RIGHT:
                    self.square.left()

        return True
    
    def highscoresWrite(self):
	highscoresFile=open(os.path.join("Highscores","highscores.txt"),"a")
	name,time=self.name()
	highscoresFile.write(name+" "+str(round(time,2))+"\n")
	highscoresFile.close()
	    
    def name(self):
	#Entirely new loop for string writing after completing time trials
	global ti
	self.font=pygame.font.SysFont("Arial", 30, bold=False, italic=False)
	name=""
	while True:
	    self.window.fill((255,255,255))
	    ti=time.clock() #time
            #ticks clock
            self.clock.tick(60)
            
            # handle pygame events -- if user closes game, stop running
            
            # update the title bar with our frames per second
	    x,y=pygame.mouse.get_pos()
		
	    for event in pygame.event.get():
		if event.type == QUIT:
		    return "N/A" #If quit is used, the player name will be N/A
		elif event.type == KEYDOWN:
		    if event.key == K_BACKSPACE:
			name=name[:-1] #Erasing letters
		    elif event.key == K_RETURN:
			name=name[:10] #only 10 letters
			return name, ti
		    elif event.unicode and len(name)<10 :
			name+=event.unicode #Adds the letter that is pressed if the length is less than 10
	    self.window.blit(self.font.render("Please enter your name:",1,((0,0,0))),(270,200))
	    font=self.font.render(name,1,(0,0,0))
	    pygame.draw.rect(self.window,(255,0,0),(200,300,420,50),5)
	    self.window.blit(font,(200,300))
	    pygame.display.flip()

class square(pygame.sprite.Sprite):
    """Square sprite sublcass of pygame sprite class, hadles its own position and ensures it stays on screen"""
    
    def __init__(self,xy):
        #Initialize pygame sprite part
        pygame.sprite.Sprite.__init__(self)
        
        #setting image and rect
        self.image = pygame.image.load(os.path.join('objects','square.jpg'))
        self.rect = self.image.get_rect()
        
        #If it is on the ground
        self.onGround=False
        
        #set position
        self.rect.centerx, self.rect.centery = xy
        
        # the movement speed of square
        self.movementspeed = 4
        
        # the current vertical velocity of the square
        self.Yvelocity = 0
        
        # the current horizontal velocity of the square
        self.Xvelocity = 0
	
	self.through=False
        
        self.onWall=False

    def jump(self): #increases vertical velocity
	if self.onGround:
	    self.Yvelocity=10
            self.Yvelocity=self.Yvelocity-20
	self.onGround=False
            
    def down(self): #decreases vertical velocity
        pass
            
    def right(self): #increases horizontal velocity
        self.Xvelocity=self.Xvelocity+self.movementspeed
        
    def left(self): #decreases horizontal velocity
        self.Xvelocity=self.Xvelocity-self.movementspeed
        
    def air(self):
	if not self.onGround:
	    # only accelerate with gravity if in the air
	    self.Yvelocity +=0.75
	    # max falling speed
	    if self.Yvelocity > 3:  
		self.Yvelocity = 3
	self.onGround=False
	    
    def move(self,dx,dy):
        """moves square in both directions, disallows outside of window"""
	if self.rect.bottom + dy > 600:
	    self.onGround=True
	    self.Yvelocity=0
	    self.rect.bottom = 600
	elif self.rect.top + dy < 0:
	    self.rect.top = 0
	else:
	    self.rect.y += dy
	    self.collisions(0,self.Yvelocity)

	if self.rect.right + dx > 800:
	    self.rect.right = 800
	elif self.rect.left + dx <0:
	    self.rect.left = 0
	else:
	    self.rect.x = self.rect.x+dx
	    self.collisions(self.Xvelocity,0)
	    
    def collisions(self,x,y):
	global lives
	global testGame
	global level
	global ti
	self.through=False
	for plat in platform:
	    if pygame.sprite.collide_rect(self,plat):
		if isinstance(plat, Spring):
		    self.Yvelocity-=18
		if isinstance(plat, Poison):
		    testGame.running=False
		    testGame.menu=True
		if isinstance(plat, smallSpring):
		    self.Yvelocity=0
		    self.Yvelocity-=8
		    self.through=True
		if isinstance(plat, Blade):
		    testGame.running=False
		    testGame.menu=True
		if isinstance(plat, endBlock):
		    testGame.highscoresWrite()
		    testGame.running=False
		    testGame.timeEnd=True
		if y>0:
		    self.onGround=True
		    self.rect.bottom=plat.rect.top

		if y<0 and self.through==False:
		    self.rect.top=plat.rect.bottom
		if x<0 and self.through==False:
		    self.rect.left=plat.rect.right
		    self.onWall=True
		if x>0 and self.through==False:
		    self.rect.right=plat.rect.left
		    self.onWall=True

	    
    def update(self):
	self.air()
        self.move(self.Xvelocity,self.Yvelocity)
	
	
	
class Platform(pygame.sprite.Sprite):
    """Square sprite sublcass of pygame sprite class, handles its own position and ensures it stays on screen"""
    
    def __init__(self,x,y,length,width):
        #Initialize pygame sprite part
        pygame.sprite.Sprite.__init__(self)

        #If it is on the ground
        self.onGround=False
        
        #set position
        self.x=x
	self.y=y
	
	self.width=width
	self.length=length
	
	#setting image and rect
	self.image=pygame.Surface((self.length,self.width))
	self.image=self.image.convert()
	self.image.fill((0,0,0))
	self.rect=pygame.Rect(self.x,self.y,self.length,self.width)

    def update(self):
	pass
        
class Spring(Platform):
    """Higher jump than usual if player lands on this"""
    
    def __init__(self,x,y,length,width):
	Platform.__init__(self,x,y,length,width)
	self.image.fill((0,0,255))
    def update(self):
	pass

class smallSpring(Platform):
    """Lower than normal jump if landed on"""
    
    def __init__(self,x,y,length,width):
	Platform.__init__(self,x,y,length,width)
	self.image.fill((0,191,255))
    def update(self):
	pass

class Poison(Platform):
    """Death square"""
    
    def __init__(self,x,y,length,width):
	Platform.__init__(self,x,y,length,width)
	self.image.fill((0,255,0))
    def update(self):
	pass
    
class Blade(pygame.sprite.Sprite):
    """Blades"""
    def __init__(self,x,y,load,xfactor,yfactor,Xrange,Yrange):
	global testGame
        #Initialize pygame sprite part
	pygame.sprite.Sprite.__init__(self)
	#set position
	self.origX=x
	self.origY=y
	self.load=load
	self.image=load
	self.rect=self.image.get_rect()
	self.degree=0
	self.x=x
	self.y=y
	self.xfactor=xfactor
	self.yfactor=yfactor
	self.Xrange=Xrange
	self.Yrange=Yrange
    def rotate(self):
	self.image=self.load
	if self.degree<360:
	    self.degree+=10
	else:
	    self.degree=0
	self.image=pygame.transform.rotate(self.image,self.degree)
	self.rect=self.image.get_rect()
	self.rect.centerx=self.x
	self.rect.centery=self.y
    def update(self):
	if not self.origX<=self.x<=self.origX+self.Xrange:
	    self.xfactor=-self.xfactor
	if not self.origY<=self.y<=self.origY+self.Yrange:
	    self.yfactor=-self.yfactor
	self.x+=self.xfactor
	self.y+=self.yfactor
	self.rotate()
	
class endBlock(Platform):
    def __init__(self,x,y,length,width):
	Platform.__init__(self,x,y,length,width)
	self.image.fill((255,52,179))
    def update(self):
	pass
    


def levelGen(File):
    global platform
    level=open(File,"r")
    platform=level.readlines()
    for each in platform:
	i=platform.index(each)
	platform[i]=each.rstrip("\n")
    for each in platform:
	i=platform.index(each)
	platform[i]=each.split(" ")
    for each in platform:
	if platform[platform.index(each)][0][0]=="S":
	    spring=Spring(int(each[0][1:]),int(each[1]),int(each[2]),int(each[3]))
	    platform[platform.index(each)]=spring
	elif platform[platform.index(each)][0][0]=="s":
	    spring=smallSpring(int(each[0][1:]),int(each[1]),int(each[2]),int(each[3]))
	    platform[platform.index(each)]=spring
	elif platform[platform.index(each)][0][0]=="p":
	    poison=Poison(int(each[0][1:]),int(each[1]),int(each[2]),int(each[3]))
	    platform[platform.index(each)]=poison
	elif platform[platform.index(each)][0][0]=="b":
	    blade=Blade(int(each[0][1:]),int(each[1]),pygame.image.load(os.path.join("Objects",each[2])),int(each[3]),int(each[4]),int(each[5]),int(each[6]))
	    platform[platform.index(each)]=blade
	elif platform[platform.index(each)][0][0]=="e":
	    finish=endBlock(int(each[0][1:]),int(each[1]),int(each[2]),int(each[3]))
	    platform[platform.index(each)]=finish
	else:
	    plat=Platform(int(each[0]),int(each[1]),int(each[2]),int(each[3]))
	    platform[platform.index(each)]=plat

level=0
#Runs
def main():
    global finishTime
    global platform
    global testGame
    global levels
    through=False
    levels=["level1.txt","level2.txt"]
    testGame = Game()
    testGame.run()
    return testGame.menu,testGame.exit