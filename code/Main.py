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
    # calculating axis point for blitting images in the  welcome screen
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


def getRandomPipe():
    pipeHeight = GAME_IMAGES["pipe"][0].get_height()
    offset = SCREENHEIGHT/3 
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_IMAGES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]

    return pipe

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play() 
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_IMAGES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_IMAGES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play() 
            return True

    for pipe in lowerPipes:
        if(playery + GAME_IMAGES['player'].get_height() > pipe['y']) and (abs(playerx - pipe['x']) < GAME_IMAGES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play() 
            return True


    return False

# function for running the logic of the game
def mainGame():
    
    # local vairable for storing the score of the variable
    score = 0

    # calculating axis point for blitting images in the  welcome screen
    # Player image
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0
    
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y':newPipe1[0]['y']}
        ]

    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y':newPipe2[1]['y']}
        ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:

        for event in pygame.event.get():

            # if the user wants to quit the game or presses the Esc keyboard button
            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                GAME_SOUNDS['wing'].play()               


        # Crash condition

        # test if the bird has crashed or not        
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return


        # Calculating the score
        
        # calculates the midpoint of the bird image 
        playerMidPos = playerx + GAME_IMAGES['player'].get_width()/2

        # function that adds up the score in case the midpoint of the bird crosses the pipe
        for pipe in upperPipes:
            # calculates the midpoint of the bird image 
            pipeMidPos = pipe['x'] + GAME_IMAGES['pipe'][0].get_width()/2

            # right as the bird crosses the pipe's midposition, score is added
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play() # playing the point sound
        

        # Velocity of the bird

        # if the bird didnot flapped the playervelocity for the y axis is increased //Results in falldown
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        
        # an important aspect. condition that satisfies whenever a up arrow is pressed it only works one time
        if playerFlapped:
            playerFlapped = False
        
        playerHeight = GAME_IMAGES['player'].get_height()
        playery += min(playerVelY, GROUNDY - playery - playerHeight) 

        # loop for moving the pipes to the left by adding them velocity
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
        
        # if a pipe is about to complete its display in the screen.
        # before removing it I added a new pipe in the list
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # removes the excess pipe if it goes out of the screen
        if upperPipes[0]['x'] < -GAME_IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # now blitting in the screen 
        SCREEN.blit(GAME_IMAGES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_IMAGES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_IMAGES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_IMAGES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_IMAGES['player'], (playerx, playery))
        
        
        #For score blitting
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_IMAGES['numbers'][digit].get_width() 
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_IMAGES['numbers'][digit],(Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_IMAGES['numbers'][digit].get_width()

        # this is a necessary function for rendering or blitting any kind of update for a particular portion
        # on the screen area.In my case I am rendering the whole screen
        pygame.display.update()

        # controls our frames per second of the game and only allows upto 32 fps
        FPSCLOCK.tick(FPS)

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
        pygame.image.load('./../gallery/images/0.png').convert_alpha(),
        pygame.image.load('./../gallery/images/1.png').convert_alpha(),
        pygame.image.load('./../gallery/images/2.png').convert_alpha(),
        pygame.image.load('./../gallery/images/3.png').convert_alpha(),
        pygame.image.load('./../gallery/images/4.png').convert_alpha(),
        pygame.image.load('./../gallery/images/5.png').convert_alpha(),
        pygame.image.load('./../gallery/images/6.png').convert_alpha(),
        pygame.image.load('./../gallery/images/7.png').convert_alpha(),
        pygame.image.load('./../gallery/images/8.png').convert_alpha(),
        pygame.image.load('./../gallery/images/9.png').convert_alpha(),
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
