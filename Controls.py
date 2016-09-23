import os
import platform
import time
import MainGame

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
	global platform
        
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()        
        
        #window
        self.window=pygame.display.set_mode((800,600))
	
        # clock for ticking
        self.clock = pygame.time.Clock()
        
        # set the window title
        pygame.display.set_caption("Pygame Drawing")
        
        #Allows events
        pygame.event.set_allowed([QUIT,KEYDOWN,MOUSEBUTTONDOWN])
        
        #Font for control display
	self.font=pygame.font.SysFont('Verdana',20,bold=True)
	
	#Load all default pictures
	self.first=pygame.image.load(os.path.join("Options","Controls1.jpg"))
	self.second=pygame.image.load(os.path.join("Options","Controls2.jpg"))
	self.third=pygame.image.load(os.path.join("Options","Controls3.jpg"))
	self.fourth=pygame.image.load(os.path.join("Options","Controls4.jpg"))
	self.fifth=pygame.image.load(os.path.join("Options","Controls5.jpg"))
	
	#Setting rects for mouse collision
	self.secondRect=pygame.Rect(0,190,490,50)
	self.thirdRect=pygame.Rect(0,280,490,50)
	self.fourthRect=pygame.Rect(0,370,490,50)
	self.fifthRect=pygame.Rect(0,465,490,50)
	self.backRect=pygame.Rect(0,100,100,50)
	
	#Reads in current config
	self.configRead()
	
	#Current selection is default
	self.selection=self.first
        
    def run(self):
        running=True
        while running: #Gameloop

            self.clock.tick(60) #Ticks clock
	    
            self.window.blit(self.selection,(0,0)) #Blits selected frame
	    
	    #Blits current key/desired keys beside corresponding control
	    self.window.blit(self.font.render(pygame.key.name(self.secondKey), 1, (255,255,255)),(590,200))
	    self.window.blit(self.font.render(pygame.key.name(self.thirdKey), 1, (255,255,255)),(590,290))
	    self.window.blit(self.font.render(pygame.key.name(self.fourthKey), 1, (255,255,255)),(590,380))
	    self.window.blit(self.font.render(pygame.key.name(self.fifthKey), 1, (255,255,255)),(590,475))
	    
	    #Draws back rect
	    pygame.draw.rect(self.window,(0,0,0),self.backRect)
	    
	    #Blits "Back" onto it
	    self.window.blit(self.font.render("Back", 1, (255,255,255)),(20,110))

            # handle pygame events -- if user closes game, stop running
            running = self.handleEvents()
            # update the title bar with our frames per second
	    
	    pygame.display.flip()

	
    def handleEvents(self): #event loop
	    
        for event in pygame.event.get():
            if event.type == QUIT:
		
		self.back=False #Differentiation between K_ESCAPE and QUIT
                return False
	    elif event.type == MOUSEBUTTONDOWN: #If clicked and mouse collides with specific rects, changes selection
		if self.secondRect.collidepoint(pygame.mouse.get_pos()):
		    self.selection=self.second
		elif self.thirdRect.collidepoint(pygame.mouse.get_pos()):
		    self.selection=self.third
		elif self.fourthRect.collidepoint(pygame.mouse.get_pos()):
		    self.selection=self.fourth
		elif self.fifthRect.collidepoint(pygame.mouse.get_pos()):
		    self.selection=self.fifth
		elif self.backRect.collidepoint(pygame.mouse.get_pos()):
		    self.back=True
		    return False
	    elif event.type == KEYDOWN: #If key is pressed that isn't Return or Escape, the corresponding key is changed to the key pressed.
		if event.key!=K_RETURN and event.key!=K_ESCAPE:
		    if self.selection==self.second:
			self.secondKey=event.key
		    elif self.selection==self.third:
			self.thirdKey=event.key
		    elif self.selection==self.fourth:
			self.fourthKey=event.key
		    elif self.selection==self.fifth:
			self.fifthKey=event.key
		elif event.key==K_ESCAPE: #If escape pressed, end game loop
		    self.configWrite()
		    self.back=False
		    return False
        return True
    
    #Reads configuration file
    def configRead(self):
	
	#Opens, puts each line into a list, takes only values after the second element, strips \n
	configFile=open(os.path.join("Options","config.txt"),"r")
	config=configFile.readlines()
	config=config[2:]
	for each in config:
	    config[config.index(each)]=each.rstrip("\n")
	    
	#Assigns keys accordingly
	self.secondKey=int(config[0])
	self.thirdKey=int(config[1])
	self.fourthKey=int(config[2])
	self.fifthKey=int(config[3])
	configFile.close()
	
    #rewrites config file according to changes
    def configWrite(self):
	
	#Reads, puts each line to list, closes
	configFile=open(os.path.join("Options","config.txt"),"r")
	config=configFile.readlines()
	configFile.close()
	
	#Opens,adds \n, and writes to file.
	configFile=open(os.path.join("Options","config.txt"),"w")
	config=config[:2]
	config.append(str(self.secondKey)+"\n")
	config.append(str(self.thirdKey)+"\n")
	config.append(str(self.fourthKey)+"\n")
	config.append(str(self.fifthKey)+"\n")
	configFile.writelines(config)
	configFile.close()
	
	    
def main(): #Runs if called from Options
    game=Game()
    game.run()
    if game.back:
	return True
    else:
	return False
