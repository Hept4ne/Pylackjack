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

(screen_width, screen_height) = (480, 640)

screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()
pygame.display.set_caption("PyLackJack")

betting = True

#Functions:

def quitgame():
    print ("Exited successfully.")
    pygame.quit()
    sys.exit()

#Classes:

class text(object):
    '''Object for text rendering.'''
    def __init__(self):
        self.self = self
        self.font = pygame.font.SysFont("arial", 28)
    def texttoprint(self):
        pass
    def print_text(self, inp, x, y):
        '''Prints text to the screen.
           inp is the text, x and y is the change from the screen center.'''
        self.string = inp
        self.text = self.font.render(self.string, False, (colors["black"]))
        self.rect = self.text.get_rect()
        self.centerx = ((screen_width/2) - self.text.get_width()//2) + x
        self.centery = ((screen_height/2) - self.text.get_height()//2) + y
        screen.blit(self.text, (self.centerx, self.centery))
        

class card(object):
    '''Class for card objects.'''
    def __init__(self):
        self.self = self
        self.key = colors["magenta"]
        self.cards = spritesheet.spritesheet('sprites/cardsheet.png')

        #Card indices and the width and height of an individual card:
        
        self.cix = 75
        self.ciy = 100
        self.width = 71
        self.height = 96
        
        #Use multiples of cix and ciy to access the cards in the deck.
        #cix * 0 = spades, * 1 = club, * 2 = heart, * 3 = diamond.
        #ciy * 0 thru 2 = king, queen, joker respectively.
        # ciy * 3 thru 12 = ace, and the number cards.
        #(e.g. 3 will be at 3 + 2 = 5

        self.index = (self.cix*0, self.ciy*0, self.width, self.height)
        self.image = self.cards.image_at(self.index, colorkey=self.key)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
    def draw(self, x, y):
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, self.rect)
        

class actor(object):
    '''actor class for variables and methods shared by player and dealer'''
    pass

class d(actor):
    pass

class p(actor):
    pass

#Variables inheriting from the classes:

startup = text()

king = card()

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
            (mousex, mousey) = pygame.mouse.get_pos()
            if mousex < 
        elif event.type == pygame.MOUSEBUTTONUP:
            #Checks if the mouseclick is released.
            pass

    #Key presses:

    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[K_LALT] or keys_pressed[K_RALT]) and keys_pressed[K_F4]:
        quitgame()

    #---

    screen.fill(colors["dark green"])

    startup.print_text("Welcome to blackjack.", 0, 0)
    if betting:
        startup.print_text("Place your bet:", 0, 32)
        startup.print_text("%i"%(100), 0, 96)

    king.draw((screen_width/2) - (king.width/2), 120)
            
    pygame.display.update()
    fpsclock.tick(60)
            
