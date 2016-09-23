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

#Main Game
class Game(object):
    def __init__(self):
	
	global lives
	global platform
	global springs	
	
	#Pygame initialization
        pygame.init()  
	
        #window
        self.window=pygame.display.set_mode((800,600))
	self.menu=False
	
        # clock for ticking
        self.clock = pygame.time.Clock()
        
        # set the window title
        pygame.display.set_caption("Platform Escape")
        
        #Allows events
        pygame.event.set_allowed([QUIT,KEYDOWN,KEYUP])
        
        #Backgrounds
        self.background=pygame.Surface((800,600))
        self.background.fill((255,255,255))

	#Differentiation between K_ESCAPE and QUIT
	self.exit=False
        
        #sprite rendering group
        self.sprites = pygame.sprite.RenderUpdates()
	
	#Levengenerates the current level
	levelGen(os.path.join("Levels",levels[level]))
	
	#Adds platforms to sprites group
	self.sprites.add(platform)
	
	#Ensure first iteration
	self.running=True
	
	#Reads config for KEYDOWN inputs
	self.configRead()

	#Creates square sprite at prompted location
        self.square=square((40,500))
	
	#Adds square to sprite group
        self.sprites.add(self.square)
	
	#assigning local to global
	self.lives=lives
    
	#Fonts for instructions
	self.font=pygame.font.SysFont("Arial", 20, bold=False, italic=False)
	self.iFont=pygame.font.SysFont("Arial",12, bold=False, italic=False)
	
	#Blits lives
	self.window.blit(self.font.render("Lives : %i" %self.lives,1,((0,0,0))),(0,0))
        
    def run(self):
        while self.running: #runs
	    
	    #Refill screen
	    self.window.fill((255,255,255))
	    
            #ticks clock
            self.clock.tick(60)
            
            # handle pygame events -- if user closes game, stop running
            self.running = self.handleEvents()
            
            #updating sprites
	    self.sprites.update()
		
            # render our sprites
            self.sprites.clear(self.window, self.background)    # clears the window where the sprites currently are, using the background
	    
	    #Blits all text info on screen
	    self.window.blit(self.font.render("Lives : %i" %self.lives,1,((0,0,0))),(0,0))
	    self.window.blit(self.font.render("Press Esc to return to main menu",1,((0,0,0))),(0,550))
	    self.window.blit(self.iFont.render("Don't touch the blades!",1,((0,0,0))),(165,520))
	    self.window.blit(self.iFont.render("Poison is deadly",1,((0,0,0))),(415,550))
	    self.window.blit(self.iFont.render("Big springs give you a lot of air!",1,((0,0,0))),(260,250))
	    self.window.blit(self.iFont.render("Small springs",1,((0,0,0))),(150,225))
	    self.window.blit(self.iFont.render("Pink means the end!",1,((0,0,0))),(650,60))
	    
	    
            dirty = self.sprites.draw(self.window)         # calculates the 'dirty' rectangles that need to be redrawn
	    
            # blit the dirty areas of the screen
	    pygame.display.update(dirty)     # updates just the 'dirty' areas'
	    pygame.display.flip()


            
            
    def handleEvents(self):
	global lives
	global menu
        for event in pygame.event.get():
            if event.type == QUIT: 
		self.exit=True #Differentiate between QUIT and ESCAPE and makes main() return different values
                return False
            
            elif event.type == KEYDOWN:
		if event.key==K_ESCAPE:
		    self.menu=True
		    return False
		
		#jumps,goes left, right, depending on key pressed
		if event.key==self.firstKey and self.menu==False:
                    self.square.jump()
                if event.key==self.fourthKey and self.menu==False:
                    self.square.down()
                if event.key==self.secondKey and self.menu==False:
                    self.square.left()
                if event.key==self.thirdKey and self.menu==False:
                    self.square.right()
	    
	    #When key goes up, does opposite to simulate gravity/acceleration and other physics.
            elif event.type == KEYUP:
                if event.key==self.firstKey:
                    self.square.down()
                if event.key==self.fourthKey:
                    self.square.down()
                if event.key==self.secondKey:
                    self.square.right()
                if event.key==self.thirdKey:
                    self.square.left()

        return True
    
    #Reads config file
    def configRead(self):
	
	#Opens file, puts into list, takes out new line.
	configtxt=open(os.path.join("Options","config.txt"),"r")
	config=configtxt.readlines()
	for each in config:
	    config[config.index(each)]=each.rstrip("\n")
	    
	#Takes only past first 2 elemnts and uses values accordingly to assign KEYDOWN(event.key) values
	config=config[2:]
	self.firstKey=int(config[0])
	self.secondKey=int(config[1])
	self.thirdKey=int(config[2])
	self.fourthKey=int(config[3])	    

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
	
	#value to determing if sprite is colliding other sprites or not.
	self.through=False

    def jump(self): #increases vertical velocity then sets onground to false.
	if self.onGround:
	    self.Yvelocity=10
            self.Yvelocity=self.Yvelocity-20
	self.onGround=False
            
    def down(self): #Null because down does nothing
        pass
            
    def right(self): #increases horizontal velocity
        self.Xvelocity=self.Xvelocity+self.movementspeed
        
    def left(self): #decreases horizontal velocity
        self.Xvelocity=self.Xvelocity-self.movementspeed
        
    def air(self):
	if not self.onGround:
	    #only accelerate with gravity if in the air
	    self.Yvelocity +=0.75
	    #max falling speed
	    if self.Yvelocity > 3:  
		self.Yvelocity = 3
	    #When in air, onground is False
	self.onGround=False
	    
    def move(self,dx,dy):
        """moves square in both directions, disallows outside of window"""
	
	#Doesn't allow sprite to leave window
	if self.rect.bottom + dy > 600:
	    self.onGround=True
	    self.Yvelocity=0
	    self.rect.bottom = 600
	elif self.rect.top + dy < 0:
	    self.rect.top = 0
	else:
	    self.rect.y += dy #Updates sprite y
	    self.collisions(0,self.Yvelocity) #Checks Y collisions
	    
	#Doesn't allow sprite to leave window
	if self.rect.right + dx > 800:
	    self.rect.right = 800
	elif self.rect.left + dx <0:
	    self.rect.left = 0
	else:
	    self.rect.x = self.rect.x+dx #Updates sprite x
	    self.collisions(self.Xvelocity,0) #Checks x collisions
    
    #Checks collisions
    def collisions(self,x,y):
	global lives
	global testGame
	global level
	self.through=False #Reset self.through
	for plat in platform: #Goes through all platform sprites and checks square sprite collisions with each one.
	    if pygame.sprite.collide_rect(self,plat): #If collides
		if isinstance(plat, Spring): #If the plat is instance of class Spring
		    self.Yvelocity-=18 #Decrease velocity
		if isinstance(plat, Poison):
		    lives-=1 #Decrease lives by 1
		    testGame.running=False #End game loop
		if isinstance(plat, smallSpring):
		    self.Yvelocity=0 #Fixed jump
		    self.Yvelocity-=8 #Decreases velocity
		    self.through=True 
		if isinstance(plat, Blade):
		    lives-=1
		    testGame.running=False
		if isinstance(plat, endBlock):
		    testGame.running=False
		    level+=1 #Goes to next level
		    
		
		if y>0: #if on top of platform
		    self.onGround=True
		    self.rect.bottom=plat.rect.top #bottom of square y=top of platform y
		if y<0 and self.through==False: #If touching bottom of platform
		    self.rect.top=plat.rect.bottom
		if x<0 and self.through==False: #If touching right of platform
		    self.rect.left=plat.rect.right
		    self.onWall=True
		if x>0 and self.through==False: #if touching left of platform
		    self.rect.right=plat.rect.left
		    self.onWall=True

	    
    #Calls the movement and air functions
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
	
	#attributes are ones given through arguments
	self.width=width
	self.length=length
	
	#setting image and rect
	self.image=pygame.Surface((self.length,self.width))
	self.image=self.image.convert()
	self.image.fill((0,0,0))
	self.rect=pygame.Rect(self.x,self.y,self.length,self.width)

    def update(self):
	pass
        
#all these subclasses of platform share EXACTLY the same attributes as Platform except for colour.
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
    
class endBlock(Platform):
    """Winning block"""
    def __init__(self,x,y,length,width):
	Platform.__init__(self,x,y,length,width)
	self.image.fill((255,52,179))
    def update(self):
	pass
    
class Blade(pygame.sprite.Sprite):
    """Blades"""
    def __init__(self,x,y,load,xfactor,yfactor,Xrange,Yrange):
	global testGame
        #Initialize pygame sprite part
	pygame.sprite.Sprite.__init__(self)
	
	#set position
	self.origX=x #need original position for movement limitation
	self.origY=y
	
	self.image=load #surface is the one given in arguments
	
	self.rect=self.image.get_rect() #gets rect from image loaded
	self.degree=0 #default degrees
	self.x=x #x and y for movement
	self.y=y
	self.xfactor=xfactor #x and yfactors for different speed of movement
	self.yfactor=yfactor
	self.Xrange=Xrange #x and y ranges of maximum movement range
	self.Yrange=Yrange
	
    def rotate(self): #Rotates the blade
	if self.degree<360:#rotates 10 degrees until 360, then resets degrees
	    self.degree+=10 
	else:
	    self.degree=0
	    
	self.image=pygame.transform.rotate(self.image,self.degree)#Gets rotated surface
	self.rect=self.image.get_rect() #Gets new rect from rotated surface
	self.rect.centerx=self.x #sets centers to new centers
	self.rect.centery=self.y
	
    def update(self):
	if not self.origX<=self.x<=self.origX+self.Xrange: #Ensures blades move within range, then reverse
	    self.xfactor=-self.xfactor
	if not self.origY<=self.y<=self.origY+self.Yrange:
	    self.yfactor=-self.yfactor
	    
	self.x+=self.xfactor #Constant x/y addition/subtraction for movement
	self.y+=self.yfactor
	
	#Rotates
	self.rotate()
    

def levelGen(File):
    global platform
    
    #Reads file, each line becomes an element, strips \n, splits each line into a sublist by " "
    level=open(File,"r")
    platform=level.readlines()
    for each in platform:
	i=platform.index(each)
	platform[i]=each.rstrip("\n")
    for each in platform:
	i=platform.index(each)
	platform[i]=each.split(" ")
	
    
    for each in platform:
	
	#A different platform is created based on the letter prompted at the beginning of the element
	if platform[platform.index(each)][0][0]=="S": #Creates large spring platform
	    spring=Spring(int(each[0][1:]),int(each[1]),int(each[2]),int(each[3]))
	    platform[platform.index(each)]=spring
	elif platform[platform.index(each)][0][0]=="s": #Creates small spring platform
	    spring=smallSpring(int(each[0][1:]),int(each[1]),int(each[2]),int(each[3]))
	    platform[platform.index(each)]=spring
	elif platform[platform.index(each)][0][0]=="p": #Creates poison platform
	    poison=Poison(int(each[0][1:]),int(each[1]),int(each[2]),int(each[3]))
	    platform[platform.index(each)]=poison
	elif platform[platform.index(each)][0][0]=="b": #Creates blade sprite
	    blade=Blade(int(each[0][1:]),int(each[1]),pygame.image.load(os.path.join("Objects",each[2])),int(each[3]),int(each[4]),int(each[5]),int(each[6]))
	    platform[platform.index(each)]=blade
	elif platform[platform.index(each)][0][0]=="e": #Creates end block
	    finish=endBlock(int(each[0][1:]),int(each[1]),int(each[2]),int(each[3]))
	    platform[platform.index(each)]=finish
	else: #If not prompted, creates ordinary platform
	    plat=Platform(int(each[0]),int(each[1]),int(each[2]),int(each[3]))
	    platform[platform.index(each)]=plat

level=0 #index of level is 0(so level starts at 1)

def main():
    global platform
    global testGame
    global through
    global lives
    global levels
    through=False
    lives=50
    levels=["level1.txt","level2.txt"] #List of all levels (There is only one level)
    testGame = Game() #Needs to run at least once before the loop to establish certain attributes
    testGame.run()
    while lives!=0:
	if testGame.menu: #K_ESCAPE and QUIT differentiation, returns value accordingly
	    return True
	elif testGame.exit:
	    return False
	else:
	    testGame = Game()
	    testGame.run()
    return True
