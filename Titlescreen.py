import os
import platform
import time
import MainGame
import Options
import Highscores
import Time

if platform.system() == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'

try:
    import pygame
    from pygame.locals import *
 
except ImportError, err:
    print "%s Failed to Load Module: %s" % (__file__, err)
    import sys
    sys.exit(1)


#Main class, contains game loop
class Game(object):
    def __init__(self):
	global platform
        
        #Initializing pygame
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()        
        
        #window
        self.window=pygame.display.set_mode((800,600))
        
        #Creates clock
        self.clock = pygame.time.Clock()
        
        #Window Title
        pygame.display.set_caption("Platform Escape")
        
        #Allows events
        pygame.event.set_allowed([QUIT,KEYDOWN])
        
        #Default optionIndex number(0 should be the option at start)
	self.optionIndex=0
	
	#create options list to append different surfaces
	self.options=[]
	
        #Title different menu option surface assignment
        self.backgroundStart=pygame.image.load(os.path.join('Start','1.jpg')) #Os.path.join joins a folder directory
	self.options.append(self.backgroundStart) #Appending surface to our options list

	self.backgroundTime=pygame.image.load(os.path.join('Time','1.jpg'))
	self.options.append(self.backgroundTime)
	
	self.backgroundOptions=pygame.image.load(os.path.join('Options','1.jpg'))
	self.options.append(self.backgroundOptions)
	
	self.backgroundHighscores=pygame.image.load(os.path.join('Highscores','1.jpg'))
	self.options.append(self.backgroundHighscores)
	
	#Loading lazer sound
	self.lazer = pygame.mixer.Sound(os.path.join('Music','lazer.wav'))
	self.lazer.set_volume(0.3) #Setting volume
	
	#Reading config file for background music/volume
	self.configRead()
	
	#reading controls from config file
	self.controlRead()
        
    def run(self):
        running=True
	
	#game loop
        while running:
            
            #Ticks clock
            self.clock.tick(60)
            
            #Goes to handleevents, if returned False by function, stops running
            running = self.handleEvents()
	    
	    #Blits the surface according to the index in the options list
	    self.window.blit(self.options[self.optionIndex],(0,0))
	    
	    pygame.display.flip()
            
    def handleEvents(self): #Event loop
        for event in pygame.event.get():
            if event.type == QUIT: #'X' Pressed
                return False
	    elif event.type == KEYDOWN: #Any key pressed
		
		if event.key == self.fourthKey and self.optionIndex!=3: #If key down is pressed and it is not at the end of menu
		    self.optionIndex+=1 #adds one to index 
		    self.lazer.play() #Plays the sound loaded
		    
		elif event.key == self.firstKey and self.optionIndex!=0: #if key up pressed and not at top of menu
		    self.optionIndex-=1 #minuses one from index
		    self.lazer.play()
		    
		    
		#if enter is pressed, goes to corresponding option
		elif event.key == K_RETURN and self.optionIndex==0:
		    self.lazer.play()
		    return MainGame.main()
		
		elif event.key == K_RETURN and self.optionIndex==3:
		    self.lazer.play()
		    Highscores.main()
		    
		elif event.key == K_RETURN and self.optionIndex==2:
		    self.lazer.play()
		    return Options.main()
		
		elif event.key == K_RETURN and self.optionIndex==1:
		    self.lazer.play()
		    menu,exit=Time.main() #Differentiating exits between pressing Escape and pressing the 'X'
		    if not menu:
			Highscores.main()
		    elif menu and exit:
			return
        return True
	
    def configRead(self): #Reads config.txt and translates for use
	
	#Loading songs
	EDM=os.path.join('Music','EDM.mp3')
	Rap=os.path.join('Music','Rap.mp3')
	Indie=os.path.join('Music','Indie.mp3')
	Pop=os.path.join('Music','Pop.mp3')
	
	backgroundMusic=[EDM,Rap,Indie,Pop] #List of songs to easily switch between
	
	backgroundVolume=[0.9921875,0.8,0.6,0.4,0.2,0.0] #list of possible volumes to switch between
	
	#Reads, puts into list, removes new line
	configtxt=open(os.path.join("Options","config.txt"),"r")
	config=configtxt.readlines()
	for each in config:
	    config[config.index(each)]=each.rstrip("\n")

	#Takes first 2 values
	for each in config[:2]:
	    if each[0]=="m": #takes the value starting with m, makes music correspond and plays
		self.musicIndex=int(each[1])
		pygame.mixer.music.load(backgroundMusic[self.musicIndex])
		pygame.mixer.music.play(-1)		    
	    if each[0]=="v": #Takes the value starting with v, adjusts volume accordingly
		self.volumeIndex=int(each[1])
		pygame.mixer.music.set_volume(backgroundVolume[self.volumeIndex])
	configtxt.close()
    
    #Reads controls
    def controlRead(self):
	
	configtxt=open(os.path.join("Options","config.txt"),"r")
	config=configtxt.readlines()
	for each in config:
	    config[config.index(each)]=each.rstrip("\n")
	    
	#Only takes values past first 2
	config=config[2:]
	
	#Reads the values and sets them as KEYDOWN values(event.key) for controls
	self.firstKey=int(config[0])
	self.secondKey=int(config[1])
	self.thirdKey=int(config[2])
	self.fourthKey=int(config[3])	

#Runs the game
game=Game()
game.run()