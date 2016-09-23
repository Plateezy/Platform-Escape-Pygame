import os
import platform
import time
import MainGame
import Controls

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
        
        #Pygame initialization
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()        
        
        #window
        self.window=pygame.display.set_mode((800,600))
        
        self.background=pygame.Surface((800,600))
	self.background.fill((255,255,255))
	
        #Ticking Clock
        self.clock = pygame.time.Clock()	
        
        #Title
        pygame.display.set_caption("Platform Escape")
        
        #Allows events
        pygame.event.set_allowed([QUIT,KEYDOWN])

	
	#Font for writing
	self.font=pygame.font.SysFont('Verdana',20,bold=True)
	
	#list to append options, default optionIndex
	self.options=[]
	self.optionIndex=0
	
        #Setting lists of possible options
	EDM=os.path.join('Music','EDM.mp3')
	Rap=os.path.join('Music','Rap.mp3')
	Indie=os.path.join('Music','Indie.mp3')
	Pop=os.path.join('Music','Pop.mp3')
        self.backgroundMusic=[EDM,Rap,Indie,Pop]
	self.backgroundVolume=[0.9921875,0.8,0.6,0.4,0.2,0.0]
	
	self.configRead()
    
	#Appending option possibilities
	self.options.append(self.backgroundMusic)
	self.options.append(self.backgroundVolume)
	
	#Load lazer sound and volume setting
	self.lazer = pygame.mixer.Sound(os.path.join('Music','lazer.wav'))
	self.lazer.set_volume(0.3)
	
	#Starting selection at first option
	self.selected=pygame.image.load(os.path.join('Options','Options1.jpg'))
	
	#Differentiate between QUIT or K_ESCAPE
	self.escape=False
	
    def run(self):
        running=True
        while running: #Run game
	    
            #Ticking clock
            self.clock.tick(60)
	    
	    #Refresh the background picture
            self.window.blit(self.background,(0,0))
	    
            #Goes to event loop
            running = self.handleEvents()
	    
	    #checks current selection
	    self.checkSelection()
	    
	    #Blits selection
	    self.window.blit(self.selected,(0,0))
	    
	    #Blits options depending on selection
	    self.optionBlitter()
	    
	    #Instructions to user
	    self.window.blit(self.font.render("Press ESC to return to main menu", 1, (0,0,0)),(0,575))
	    
	    pygame.display.flip()
	    
	#Writes changed options into config
	self.configWrite()
	
	#Part of differentiation between QUIT and K_ESCAPE
	if self.escape==True:
	    return True
	else:
	    return False
	
    #Event loop
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
	    elif event.type == KEYDOWN:
		if event.key == K_ESCAPE:
		    self.escape=True
		    return False
		
		if event.key == self.fourthKey and self.optionIndex!=2: #If key down is pressed and it is not at the end of menu
		    self.optionIndex+=1 #adds one to index 
		    self.lazer.play() #Plays the sound loaded
		elif event.key == self.firstKey and self.optionIndex!=0: #or if key up pressed and not at top of menu
		    self.optionIndex-=1 #subtracts one from index
		    self.lazer.play()
		elif event.key == K_RETURN and self.optionIndex==2: #if enter is pressed
		    self.lazer.play()
		    return Controls.main() #Goes to controls
		
		
		#Same menus but for submenus instead of main options menu
		
		#Volume list control
		elif event.key == self.secondKey and self.optionIndex==1 and self.volumeIndex!=0:
		    self.volumeIndex-=1
		    pygame.mixer.music.set_volume(self.backgroundVolume[self.volumeIndex])
		    self.lazer.play()
		elif event.key == self.thirdKey and self.optionIndex==1 and self.volumeIndex!=5:
		    self.volumeIndex+=1
		    pygame.mixer.music.set_volume(self.backgroundVolume[self.volumeIndex])
		    self.lazer.play()
		    
		#Music list control
		elif event.key == self.secondKey and self.optionIndex==0 and self.musicIndex!=0:
		    self.musicIndex-=1
		    self.lazer.play()
		    pygame.mixer.music.load(self.backgroundMusic[self.musicIndex])
		    pygame.mixer.music.play(-1)
		    print self.musicIndex
		elif event.key == self.thirdKey and self.optionIndex==0 and self.musicIndex!=3:
		    self.musicIndex+=1
		    self.lazer.play()
		    pygame.mixer.music.load(self.backgroundMusic[self.musicIndex])
		    pygame.mixer.music.play(-1)
		    print self.musicIndex
        return True
    
    def optionBlitter(self):
	
	#Music square blitting dependent on selection
	if self.musicIndex==0:
	    pygame.draw.rect(self.window, (255,0,0), (200,103,50,50)) #draws rect
	    text=self.font.render("EDM", 1, (0,255,0)) #Writes text on rect
	    self.window.blit(text,(200,113)) #Blits text to surface
	if self.musicIndex==1:
	    pygame.draw.rect(self.window, (255,0,0), (300,103,50,50))
	    text=self.font.render("Rap",1,(0,255,0))
	    self.window.blit(text,(302,113))
	if self.musicIndex==2:
	    pygame.draw.rect(self.window, (255,0,0), (400,103,50,50))
	    font=pygame.font.SysFont('Verdana',17,bold=True)
	    text=font.render("Indie",1,(0,255,0))
	    self.window.blit(text,(400,113))
	if self.musicIndex==3:
	    pygame.draw.rect(self.window, (255,0,0), (500,103,50,50))
	    text=self.font.render("Pop",1,(0,255,0))
	    self.window.blit(text,(502,113))
	    
	#Volume square blitting dependent on selection
	if self.volumeIndex==0:
	    pygame.draw.rect(self.window, (255,0,0), (200,258,50,50))
	    text=self.font.render("100",1,(0,255,0))
	    self.window.blit(text,(202,268))
	if self.volumeIndex==1:
	    pygame.draw.rect(self.window, (255,0,0), (275,258,50,50))
	    text=self.font.render("80",1,(0,255,0))
	    self.window.blit(text,(285,268))
	if self.volumeIndex==2:
	    pygame.draw.rect(self.window, (255,0,0), (350,258,50,50))
	    text=self.font.render("60",1,(0,255,0))
	    self.window.blit(text,(360,268))	 
	if self.volumeIndex==3:
	    pygame.draw.rect(self.window, (255,0,0), (425,258,50,50))
	    text=self.font.render("40",1,(0,255,0))
	    self.window.blit(text,(435,268))
	if self.volumeIndex==4:
	    pygame.draw.rect(self.window, (255,0,0), (500,258,50,50))
	    text=self.font.render("20",1,(0,255,0))
	    self.window.blit(text,(510,268))
	if self.volumeIndex==5:
	    pygame.draw.rect(self.window, (255,0,0), (575,258,50,50))
	    text=self.font.render("0",1,(0,255,0))
	    self.window.blit(text,(591,268))
	    
    #Checking selection to reassign selection accordingly
    def checkSelection(self):
	if self.optionIndex==0: #If index is 0
	    self.selected=pygame.image.load(os.path.join('Options','Options1.jpg')) #Use this surface as primary background
	if self.optionIndex==1:
	    self.selected=pygame.image.load(os.path.join('Options','Options2.jpg'))
	if self.optionIndex==2:
	    self.selected=pygame.image.load(os.path.join('Options','Options3.jpg'))
	    
    
    #Reads config and applies accordingly
    def configRead(self):
	
	#Opens file, puts each line into list, takes off new line
	configtxt=open(os.path.join("Options","config.txt"),"r")
	config=configtxt.readlines()
	for each in config:
	    config[config.index(each)]=each.rstrip("\n")
	
	
	#Grabs music and volume portions of the config
	for each in config[:2]:
	    if each[0]=="m":
		self.musicIndex=int(each[1])
	    if each[0]=="v":
		self.volumeIndex=int(each[1])
		
	#Takes elements only after first 2(which are the volume/music)
	config=config[2:]
	
	#Sets KEYDOWN keys according to config values
	self.firstKey=int(config[0])
	self.secondKey=int(config[1])
	self.thirdKey=int(config[2])
	self.fourthKey=int(config[3])
	    
	configtxt.close()
	
	
    #Rewrites config based on changes made
    def configWrite(self):
	
	#Opens file, turns each line into list element, close
	configtxt=open(os.path.join("Options","config.txt"),"r")
	config=configtxt.readlines()
	configtxt.close()
	
	music="m"+str(self.musicIndex) #new string is m+(new index)
	volume="v"+str(self.volumeIndex) #new string is v+(new index)
	config[0]=(music+"\n") #adds newlines
	config[1]=(volume+"\n")
	
	configtxt=open(os.path.join("Options","config.txt"),"w") #writes back to file
	configtxt.writelines(config)
	configtxt.close()
	
#runs when called from titlescreen.py
def main():
    game=Game()
    return game.run()
