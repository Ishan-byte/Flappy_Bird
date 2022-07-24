#Imports
from email import message
import random # Module for generating random numbers
import sys # Module for controlling the game window
import pygame
from pygame.locals import * # Basic and Necessary Pygame imports

#Global Variables
# tracks welcome screen is running or not
welcomeScreenIsOperating = True

# tracks game window is running or not
gameIsOperating = True

# Window Screen related
FPS = 32 # frames to render on the screen per second
SCREENWIDTH = 289 # screen width
SCREENHEIGHT = 511 # screen height 

# Intializing a window screen
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

# Determining space for the base or the ground image in the window screen
GROUNDY = SCREENHEIGHT * 0.8

# Initializing empty Dictonaries for storing images and sounds for the game
GAME_IMAGES = {}
GAME_SOUNDS = {}

# Images for objects of the game
PLAYER = './../gallery/images/bird.png'
BG = './../gallery/images/background.png'
PIPE = './../gallery/images/pipe.png'

#Functions

# function for rendering welcome screen till the player starts the game or exits
def welcomeScreen():
    # calculating axis point for blitting images in the screen
    # Player image
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_IMAGES['player'].get_height())/2)
    
    # Message image
    messageX = int((SCREENWIDTH - GAME_IMAGES['message'].get_width())/2)
    messageY = int(SCREENHEIGHT * 0.13)
    baseX = 0

    # loop for displaying welcome screen
    while (welcomeScreenIsOperating):
        # event loop
        # so every window has a message or an event queue and every now an then we have to 
        # check it in order to handle the game events.
        for event in pygame.event.get():

            # if the user wants to quit the game or presses the Esc keyboard button
            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # the game starts whenever the user will press the space button or the up arrow key.
            # so this case checks that event and returns from this function and the main function is executed
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

           # however if no events are in the event queue, then the game will render the same welcome screen
           # over and over till the user performs any event 
            else:
                # blitting images in our created screen
                SCREEN.blit(GAME_IMAGES['background'], (0,0))
                SCREEN.blit(GAME_IMAGES['player'], (playerx,playery))
                SCREEN.blit(GAME_IMAGES['message'], (messageX,messageY))
                SCREEN.blit(GAME_IMAGES['base'], (baseX,GROUNDY))

                # this is a necessary function for rendering or blitting any kind of update for a particular portion
                # on the screen area.In my case I am rendering the whole screen
                pygame.display.update()

                # controls our frames per second of the game and only allows upto 32 fps
                FPSCLOCK.tick(FPS)


def mainGame():
    pass


# Main function
if __name__ == "__main__":
    
    # this method call intializes all the imported modules of pygame
    pygame.init()

    # creating a clock object for controlling our FPS for the screen 
    FPSCLOCK = pygame.time.Clock()

    # For setting the caption of the game window 
    pygame.display.set_caption("Ishan's Flappy Bird")

    #IMAGES
    # loading image files in the game_images dictonary by storting them in a tuple first
    # Later on, the tuple will be stored in the main dictionary
    # convert alpha optimizes the image including per pixels alphas
    # TODO :- minmize hard coded variables
    GAME_IMAGES['numbers'] = (
        pygame.image.load('./../gallery/images/0.png').convert_alpha,
        pygame.image.load('./../gallery/images/1.png').convert_alpha,
        pygame.image.load('./../gallery/images/2.png').convert_alpha,
        pygame.image.load('./../gallery/images/3.png').convert_alpha,
        pygame.image.load('./../gallery/images/4.png').convert_alpha,
        pygame.image.load('./../gallery/images/5.png').convert_alpha,
        pygame.image.load('./../gallery/images/6.png').convert_alpha,
        pygame.image.load('./../gallery/images/7.png').convert_alpha,
        pygame.image.load('./../gallery/images/8.png').convert_alpha,
        pygame.image.load('./../gallery/images/9.png').convert_alpha,
    )

    GAME_IMAGES['message'] = pygame.image.load('./../gallery/images/message.png').convert_alpha()
    GAME_IMAGES['base'] = pygame.image.load('./../gallery/images/base.png').convert_alpha()

    # same pipe image has been blitted upside down for blitting pipes on both sides of the window screen
    # by using rotate function that take two arguments, image file and rotation degree
    GAME_IMAGES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_IMAGES['background'] = pygame.image.load(BG).convert_alpha()
    GAME_IMAGES['player'] = pygame.image.load(PLAYER).convert_alpha()


    # SOUNDS
    # importing sound files 
    # mixer.Sound creates a new Sound object from the provided file or readable buffer object
    GAME_SOUNDS['die'] = pygame.mixer.Sound('./../gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('./../gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('./../gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('./../gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('./../gallery/audio/wing.wav')

    # this is the main loop for running the game 
    while (gameIsOperating):
        welcomeScreen()
        mainGame()





