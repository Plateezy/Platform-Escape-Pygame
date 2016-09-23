import os
import platform
import time
import MainGame
import Options

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
	
	#window
	self.window=pygame.display.set_mode((800,600))
	
	# clock for ticking
	self.clock = pygame.time.Clock()
	
	# set the window title
	pygame.display.set_caption("Pygame Drawing")
	
	#Allows events
	pygame.event.set_allowed([QUIT,KEYDOWN])


	
	self.printing() #Prints highscores
	
	self.background=pygame.image.load(os.path.join("Highscores","background.jpg")) #Assigns background surface
	
    def run(self):
	running=True
	while running: #runs
	    self.window.blit(self.background,(0,0))
	    self.printing() #Prints highscores
	    #ticks clock
	    self.clock.tick(60)
	    
	    # handle pygame events -- if user closes game, stop running
	    running = self.handleEvents()
	    
	    # update the title bar with our frames per second
	    pygame.display.set_caption('Platform Escape')
	    pygame.display.flip()
	    
    def handleEvents(self): #event loop
	for event in pygame.event.get():
	    if event.type == QUIT: #Quits if 'X' pressed
		return False
	    elif event.type == KEYDOWN:
		if event.key == K_ESCAPE: #Quits if escape is pressed
		    return False
	return True
    
    #Reads highscores
    def read(self):
	#Reads highscores, puts lines into listm strips \n, divides each element into sublist with " "
	highscoresFile=open(os.path.join("Highscores","highscores.txt"),"r")
	self.highscores=highscoresFile.readlines()
	for each in self.highscores:
	    self.highscores[self.highscores.index(each)]=each.rstrip("\n")
	for each in self.highscores:
	    self.highscores[self.highscores.index(each)]=each.split(" ")
	    
	#Sorts based on the second element in the sublist
	self.highscores=sorted(self.highscores, key=lambda score: float(score[1]))
	
	#Takes only top 10
	self.highscores=self.highscores[:10]	
    
    #Prints highscores
    def printing(self):
	y=200 #Default y value
	for each in self.highscores: #Does this for every value in highscores list
	    y+=25 #Adds 25 y each time so they are printed downwards
	    font=pygame.font.SysFont('Verdana',25,bold=True) #Font declaration
	    text=font.render(each[0],1,(0,0,0)) #Creates surface
	    self.window.blit(text,(50,y)) #Blits surface
	    
	    text=font.render(each[1],1,(0,0,0))	    
	    self.window.blit(text,(600,y))

#Runs if called from Titlescreen.py
def main():
    testGame=Game()
    testGame.run()
