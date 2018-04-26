import pygame, tkinter, sys
import spritesheet
from pygame.locals import *
from random import randint, choice
pygame.init()

#Dictionary of colors. Colors are chosen using a tuple of RGB values:

colors = {
    "black" : (0, 0, 0),
    "white" : (255, 255, 255),
    "red" : (255, 0, 0),
    "green" : (0, 255, 0),
    "blue" : (0, 0, 255),
    "dark green" : (0, 128, 0),
    "magenta" : (255, 0, 255)
    }

#Global variables:

fpsclock = pygame.time.Clock()
deltaclock = pygame.time.Clock()

(width, height) = (480, 640)

screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()
pygame.display.set_caption("PyLackJack")

cards = spritesheet.spritesheet('sprites/cardsheet.png')

image = cards.image_at((0, 0, 71, 96), colorkey=colors["magenta"])

rect = image.get_rect()
rect.x = 0
rect.y = 0

#Functions:

def quitgame():
    print ("Exited successfully.")
    pygame.quit()
    sys.exit()

#Game loop:

while True:
    deltatime = deltaclock.tick(60) #Creates the clock for Delta Time.
    dps = deltatime/60
    #Can be used for adjusting the speed of game elements
    #if the framerate decreases.

    for event in pygame.event.get():
        if event.type == QUIT:
            quitgame()
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            rect.x, rect.y = mouseX, mouseY
            print (mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            #Checks if the mouseclick is released.
            pass

    #Key presses:

    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[K_LALT] or keys_pressed[K_RALT]) and keys_pressed[K_F4]:
        quitgame()
    #---

    screen.fill(colors["dark green"])

    screen.blit(image, rect)
    
    pygame.display.update()
    fpsclock.tick(60)
            
