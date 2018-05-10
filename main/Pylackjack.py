import pygame
from spritesheet import SpriteSheet
from tkinter import *
from pygame.locals import *
# from random import randint, choice
pygame.init()

# Colors! These are chosen using a tuple of RGB values:

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
dark_green = (0, 128, 0)
magenta = (255, 0, 255)

gameIcon = pygame.image.load('sprites/pylackjack.png')
pygame.display.set_icon(gameIcon)

# Global variables:

fpsclock = pygame.time.Clock()
deltaclock = pygame.time.Clock()

(screen_width, screen_height) = (480, 640)
screen_centerx = (screen_width/2)
screen_centery = (screen_height/2)

screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()
pygame.display.set_caption("PyLackJack")

# Todo: WRITE SOME FUCKING COMMENTS HOLY SHIT DUDE!!! Also rewrite CLIblackjack to follow PEP-8 guidelines.

# Functions:


def quitgame():
    """Quits the game."""
    print("Exited successfully.")
    pygame.quit()
    sys.exit()


def text_objects(text, font):
    """Helper function for message_display. Defines the font and rect of the text input."""
    textsurf = font.render(text, False, black)
    return textsurf, textsurf.get_rect()


def message_display(text, font="arial", size=28, centering=True, x=0, y=0):
    """Displays a message. Basically a GUI version of print().
       If centered, the x and y coordinates start at the center."""
    font_and_size = pygame.font.SysFont(font, size)
    textsurf, textrect = text_objects(text, font_and_size)
    if centering:
        textrect.center = (screen_centerx + x, screen_centery + y)
    else:
        textrect = (x, y)
    screen.blit(textsurf, textrect)


def end_bet():
    global betting, roundstart
    betting = False
    roundstart = True
    

# Classes:


class ImgButton:
    """Object class for image-based buttons. Only buttons with binary states are supported."""
    def __init__(self, w, h, spritesheet_img, sloc_x, sloc_y):
        """Defines the width, height, a sprite-sheet image, and sprite location on the sheet."""
        self.spritesheet = SpriteSheet(spritesheet_img)
        self.w = w
        self.h = h
        self.sloc_x = sloc_x  # Multiplier for the chosen sprite's location on the sprite-sheet.
        self.sloc_y = sloc_y  # Each increase of one moves by the width and/or height of the sprite size.

    def draw(self, x, y, action=None, center=False):
        """Draws an image-based button object and defines its action.
           If centered, the x and y coordinates start at the center."""
        global mousedown
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        index = (self.sloc_x*self.w, self.sloc_y*self.h, self.w, self.h)  # Index of the chosen sprite and its w and h.
        image = self.spritesheet.image_at(index)
        image_rect = image.get_rect()
        image_rect.x = x
        image_rect.y = y
        if center:
            x = screen_centerx
            y = screen_centery
        # if image_rect.x + self.w > mouse[0] > image_rect.x and image_rect.y + self.h > mouse[1] > image_rect.y:
        if click[0] == 1 and action is not None and image_rect.collidepoint(mouse):
            index = ((self.sloc_x+1)*self.w, self.sloc_y*self.h, self.w, self.h)
            image = self.spritesheet.image_at(index)
            image_rect = image.get_rect()
            image_rect.x = x
            image_rect.y = y
            screen.blit(image, image_rect)
            action()
        screen.blit(image, image_rect)


class Button:
    """Object class for rect-and-text based buttons."""
    def __init__(self):
        pass

    def draw(self, msg, x, y, w, h, inactivecolor, activecolor, action=None, center=False):
        """Draws a rect-and-text based button object and defines its action.
           If centered, the x and y coordinates start at the center."""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if center:
            x = (screen_centerx - (w / 2)) + x
            y = (screen_centery - (h / 2)) + y
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            self.dothing(x, w, y, h, activecolor, click, action)
        else:
            pygame.draw.rect(screen, inactivecolor, (x, y, w, h))
        font_and_size = pygame.font.SysFont("arial", 24)
        textsurf, textrect = text_objects(msg, font_and_size)
        textrect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(textsurf, textrect)

    @staticmethod
    def dothing(x, w, y, h, activecolor, click, action):
        global mousedown
        pygame.draw.rect(screen, activecolor, (x, y, w, h))
        if click[0] == 1 and action is not None and not mousedown:
            action()
            mousedown = True


class Card:
    """Class for card objects."""
    def __init__(self):
        self.self = self
        self.key = magenta
        self.cards = SpriteSheet('sprites/cardsheet.png')

        # Card indices and the width and height of an individual card:
        
        self.cix = 75
        self.ciy = 100
        self.width = 71
        self.height = 96
        
        # Use multiples of cix and ciy to access the cards in the deck.
        # cix * 0 = spades, * 1 = club, * 2 = heart, * 3 = diamond.
        # ciy * 0 thru 2 = king, queen, joker respectively.
        # ciy * 3 thru 12 = ace, and the number cards.
        # (e.g. 3 will be at 3 + 2 = 5

        self.index = (self.cix*0, self.ciy*0, self.width, self.height)
        self.image = self.cards.image_at(self.index, colorkey=self.key)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
    def draw(self, x, y):
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, self.rect)
        

class Actor:
    """Actor class for variables and methods shared by player and dealer."""
    busted = False
    gotace = False
    turn = False
    numofaces = 0
    value = 0
    ace = 11
    kqjlist = ["King!", "Queen!", "Jack!"]
    kingqueenjack = 10

    def __init__(self):
        self.name = self

    def gethand(self, nowworth):
        """Print's the person's hand. "nowworth" is a boolean for printing
           "X's hand is now worth Y." instead of "X's hand is worth Y."""""
        if nowworth:
            message_display("%s's hand is now worth %i." % (self.name, self.value))
        else:
            message_display("%s's hand is worth %i." % (self.name, self.value))


class P(Actor):
    pass


class D(Actor):
    pass


class Money:
    value = 100

    def __init__(self):
        self.modifywait = 15  # The delay between each successive increment or decrement of the value.
        self.modifywait_waittime = 15
        self.modify_value_increase_rate = 0
        self.modify_vir_waittime = 15
        self.waittime = 0

    def keep_in_valid_range(self):
        if self.value < 0:
            self.value = 0
        if self.value > 100000:
            self.value = 100000

    def add(self):
        self.change_value(1)

    def sub(self):
        self.change_value(-1)

    def change_value(self, n):
        if self.waittime < 1:
            self.value += n * (2 ** self.modify_value_increase_rate)
            self.waittime += self.modifywait
        if self.modifywait > 0 and self.modifywait_waittime < 1:
            self.modifywait -= 2.5
            self.modifywait_waittime = 15
        if self.modifywait < 1 and self.modify_vir_waittime < 1:
            self.modify_value_increase_rate += 1
            self.modify_vir_waittime = 15
        self.waittime -= 1
        self.modifywait_waittime -= 1
        if self.modifywait < 1:
            self.modify_vir_waittime -= 1

    def reset_bet(self):
        self.value = 100


# Variables inheriting from the classes:

mousedown = False

Bet = Money()

king = Card()

increasebutton = ImgButton(16, 16, "sprites/buttons.png", 0, 0)
decreasebutton = ImgButton(16, 16, "sprites/buttons.png", 0, 1)

acceptBet = Button()

hold_time = 0
hold_increase_time = 30
prev_hold_time = hold_time
Betincr = 1

betting = True
roundstart = False

# Game loop:

while True:
    deltatime = deltaclock.tick(60)  # Creates the clock for Delta Time.
    dps = deltatime/60
    # Can be used for adjusting the speed of game elements
    # if the framerate decreases.

    for event in pygame.event.get():
        if event.type == QUIT:
            quitgame()
        if event.type == pygame.MOUSEBUTTONDOWN:

            mousepos = pygame.mouse.get_pos()

            """if increasebutton.is_clicked(mousepos) and Bet <= 100000:  # <-- Todo: REWRITE THIS
                Bet += 1
                increasebutton.clicking = True
            elif decreasebutton.is_clicked(mousepos) and Bet:  # <-- Todo: AND THIS
                Bet -= 1
                decreasebutton.clicking = True"""

        if event.type == pygame.MOUSEBUTTONUP:
            # Reinitializes (i.e. resets) the betting variables (except for the betting amount):
            Bet.__init__()

    """if increasebutton.clicking:
        modifyBet(increase=True)
    if decreasebutton.clicking:
        modifyBet(decrease=True)"""

    # keep_Bet_in_range()

    # Key presses:

    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[K_LALT] or keys_pressed[K_RALT]) and keys_pressed[K_F4]:
        quitgame()

    # ---

    screen.fill(dark_green)

    if betting:
        Bet.keep_in_valid_range()
        king.draw((screen_width/2) - (king.width/2), 120)
        greeting = ["Welcome to blackjack.", "Place your bet:", str(Bet.value)]
        message_display(greeting[0], x=0, y=0)
        message_display(greeting[1], x=0, y=32)
        numoffset = (len(str(Bet.value)) - 3) * 8
        message_display(greeting[2], x=0-numoffset, y=96)
        increasebutton.draw(270, 400, action=Bet.add)
        decreasebutton.draw(270, 416, action=Bet.sub)
        acceptBet.draw("Accept", 0, 150, 100, 40, dark_green, green, action=end_bet, center=True)

    if roundstart:
        pass

            
    pygame.display.update()
    fpsclock.tick(60)
