import os, sys
import pygame
from pygame.locals import *

#Yell at the user for having buggy pygame.

if not pygame.font: print('[WARN]:Fonts disabled.')
if not pygame.mixer: print('[WARN]:Sound disabled. There will be no music.')

#Game main class.
#This class handles main init and game creation.

class PyManMain:
    def __init__(self, width=640,height=480):
        #Pretty self-explanitory.
        pygame.init()
        #Set size of game. What is it with 640*480
        self.width = width
        self.height = height
        #That game I talked about? let's make it a screen to be on.
        self.screen = pygame.display.set_mode((self.width, self.height))
    #Let's make the main loop of out game. (keypress detection, logic, etc)
    def MainLoop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
#READY PLAYER ONE.
if __name__=="__main__":
    print("READY PLAYER ONE")
    MainWindow = PyManMain()
    MainWindow.MainLoop()
