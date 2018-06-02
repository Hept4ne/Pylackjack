import pygame
from spritesheet import SpriteSheet
from tkinter import *
from pygame.locals import *
from random import randint  # , choice

# Initializes pygame and creates the game icon:

pygame.init()

gameIcon = pygame.image.load('sprites/pylackjack.png')
pygame.display.set_icon(gameIcon)

# Colors! These are chosen using a tuple of RGB values:

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
dark_green = (0, 128, 0)
magenta = (255, 0, 255)
keycolor = (217, 87, 99)

# Global variables:

fpsclock = pygame.time.Clock()
deltaclock = pygame.time.Clock()

(screen_width, screen_height) = (480, 640)
screen_centerx = (screen_width/2)
screen_centery = (screen_height/2)
(s_w, s_h) = (screen_width, screen_height)

screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()
pygame.display.set_caption("PyLackJack")

# Todo: WRITE SOME MORE COMMENTS!
# Todo: add polish!

# Functions:


def quitgame():
    """Quits the game."""
    print("Exited successfully.")
    pygame.quit()
    sys.exit()


def text_objects(text, font, textcolor=black):
    """Helper function for message_display. Defines the font and rect of the text input."""
    textsurf = font.render(text, False, textcolor)
    return textsurf, textsurf.get_rect()


def message_display(text, font="microsoft sans serif", size=24, center=True, x=0, y=0, textcolor=black):
    """Displays a message. Basically a GUI version of print().
       If centered, the x and y coordinates start at the center."""
    font_and_size = pygame.font.SysFont(font, size)
    textsurf, textrect = text_objects(text, font_and_size, textcolor)
    if center:
        textrect.center = (screen_centerx + x, screen_centery + y)
    else:
        textrect = (x, y)
    screen.blit(textsurf, textrect)


def end_bet():
    """Ends the bet and initiates the start of the round."""
    global Bet, Player, actiontimer, betting, roundstart, playing
    if Bet.value > Player.available_money:
        actiontimer = 60
    else:
        Player.available_money -= Bet.value
        betting = False
        playing = True
        roundstart = True
        initgame()


def draw_rect(rectcolor, x, y, w, h, center=False):
    """Draws a rect. Pretty straightforward."""
    if center:
        x = screen_centerx - (w/2)
        y = screen_centery - (h/2)
    pygame.draw.rect(screen, rectcolor, (x, y, w, h))


def draw_img(img, x=0, y=0, center=True, colorkey=magenta):
    """Draws an image. The colorkey by default is magenta aka (255, 0, 255)."""
    img = pygame.image.load(img)
    w, h = img.get_size()
    if center:
        x = screen_centerx - (w/2) + x
        y = screen_centery - (h/2) + y
    img = img.convert()
    img.set_colorkey(colorkey)
    img_rect = img.get_rect()
    img_rect.x = x
    img_rect.y = y
    screen.blit(img, img_rect)


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
        self.releaseactivate = False
        self.timeouttimer = 30
        self.canexec = True

    def draw(self, x=0, y=0, action=None, center=False, act_on_release=False, canmoveoff=False):
        """Draws an image-based button object and defines its action. If centered, the x and y coordinates
           start at the center. Action defines what action is executed when the button is clicked, and
           act_on_release determines if the action will execute when the button is released."""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        index = (self.sloc_x*self.w, self.sloc_y*self.h, self.w, self.h)  # Index of the chosen sprite and its w and h.
        image = self.spritesheet.image_at(index)
        image_rect = image.get_rect()
        if center:
            x = (screen_centerx - (self.w/2)) + x
            y = (screen_centery - (self.h/2)) + y
        image_rect.x = x
        image_rect.y = y
        if click[0] == 1 and action is not None and image_rect.collidepoint(mouse):
            # This Sets a timer for the action to execute.
            # This is useful if some condition is not met, so the action won't just run forever.
            index = ((self.sloc_x+1)*self.w, self.sloc_y*self.h, self.w, self.h)
            image = self.spritesheet.image_at(index)
            image_rect = image.get_rect()
            image_rect.x = x
            image_rect.y = y
            screen.blit(image, image_rect)
            if not act_on_release:
                action()
            elif act_on_release:
                self.releaseactivate = True
        if not click[0] and self.releaseactivate and (image_rect.collidepoint(mouse) or canmoveoff):
            action()
            self.releaseactivate = False
        elif not click[0] and self.releaseactivate:
            self.releaseactivate = False
        screen.blit(image, image_rect)


class CardDraw(pygame.sprite.Sprite):
    """Class for card objects."""
    cards = SpriteSheet('sprites/cardsheet.png')

    cix = 75
    ciy = 100
    width = 71
    height = 96
    center = (screen_centerx - (width/2), screen_centery - (height/2))

    card_values = [10, 10, 10, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def __init__(self, cchoice, csuit, targetactor, x=0, y=0, center=True):
        pygame.sprite.Sprite.__init__(self)
        self.index = (CardDraw.cix * csuit, CardDraw.ciy * cchoice, CardDraw.width, CardDraw.height)
        self.image = CardDraw.cards.image_at(self.index, colorkey=keycolor)
        self.image_rect = self.image.get_rect()
        self.value = self.card_values[cchoice]
        if center:
            self.image_rect.x, self.image_rect.y = CardDraw.center[0] + x, CardDraw.center[1] + y
        else:
            self.image_rect.x = x
            self.image_rect.y = y
        targetactor.value += self.value
        targetactor.cards.append(self)
        if cchoice == 3:
            targetactor.gotace = True
        if len(targetactor.cards) > 2:
            targetactor.cards[-1].image_rect.x = targetactor.cardoffset
            if targetactor.cardoffset < 10:
                targetactor.cardoffset = 130
            else:
                targetactor.cardoffset -= 11

    def draw(self):
        screen.blit(self.image, self.image_rect)


class Actor:
    """Actor class for variables and methods shared by player and dealer."""

    def __init__(self):
        self.name = self

        self.busted = False
        self.gotace = False
        self.acecount = 0
        self.turn = False
        self.value = 0
        self.kqjlist = ["King!", "Queen!", "Jack!"]
        self.kingqueenjack = 10
        self.cardoffset = 130
        self.natural = False

        self.cards = []

    def gethand(self, nowworth):
        """Print's the person's hand. "nowworth" is a boolean for printing
           "X's hand is now worth Y." instead of "X's hand is worth Y."""""
        if nowworth:
            message_display("%s's hand is now worth %i." % (self.name, self.value))
        else:
            message_display("%s's hand is worth %i." % (self.name, self.value))


class P(Actor):
    available_money = 100
    surrendered = False

    def hit(self):
        CardDraw(randint(0, 12), randint(0, 3), self, x=+64, y=121)

    @staticmethod
    def stand():
        global roundstart, standing, actiontimer
        roundstart = False
        standing = True
        actiontimer = 240

    def dbl_down(self):
        pass

    def surrender(self):
        global roundstart, betting, Bet, restart, playing, actiontimer
        betting = True
        roundstart = False
        playing = False
        restart = True
        self.surrendered = True
        actiontimer += 120
        self.available_money += (Bet.value//2)
        Bet.value = self.available_money


class D(Actor):
    holecardrevealed = False


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


# Variables inheriting from the classes, and other useful game-loop global variables:

Bet = Money()

Player = P()
Dealer = D()

increasebutton = ImgButton(16, 16, "sprites/betbuttons.png", 0, 0)
decreasebutton = ImgButton(16, 16, "sprites/betbuttons.png", 0, 1)

hitbutton = ImgButton(48, 32, "sprites/button_hit.png", 0, 0)
standbutton = ImgButton(78, 32, "sprites/button_stand.png", 0, 0)
doubledownbutton = ImgButton(122, 32, "sprites/button_doubledown.png", 0, 0)
surrenderbutton = ImgButton(124, 32, "sprites/button_surrender.png", 0, 0)

acceptbutton = ImgButton(96, 32, "sprites/acceptbutton.png", 0, 0)

hold_time = 0
hold_increase_time = 30
prev_hold_time = hold_time

betting = True
roundstart = False
standing = False
endgame = False
playing = False
restart = False

actiontimer = 0

debugmode = False

won = False
tie = False


# For the card coordinates:
# to move a centered card back to the origin for x is -(screen_width/2 - (card.width/2)), or -int(204.5)
# to move a centered card back to the origin for y is -(screen_height/2 - (card.height/2)), or -272
# to convert center=False coords to center=True cords, simply add the old (x, y) coords to (205, -272)


def initgame():
    # Player's cards:
    CardDraw(randint(0, 12), randint(0, 3), Player, x=-64, y=121)
    CardDraw(randint(0, 12), randint(0, 3), Player, x=+64, y=121)
    # Dealer's card:
    CardDraw(randint(0, 12), randint(0, 3), Dealer, x=-64, y=-152)


def restartgame():
    global restart
    restart = True


# Game loop:

while True:

    if restart:
        Player.__init__()
        Dealer.__init__()
        betting = True
        roundstart = False
        standing = False
        endgame = False
        playing = False

        if won:  # If the player won:
            Player.available_money += Bet.value*2
            won = False

        if tie:  # If the player tied:
            tie = False
            Player.available_money += Bet.value

        restart = False

    deltatime = deltaclock.tick(60)  # Creates the clock for Delta Time.
    dps = deltatime/60  # Can be used for adjusting the speed of game elements if the frame-rate decreases.

    for event in pygame.event.get():
        if event.type == QUIT:
            quitgame()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.MOUSEBUTTONUP:
            # Re-initializes (i.e. resets) the betting variables (except for the betting amount):
            Bet.__init__()

    # Key presses:

    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[K_LALT] or keys_pressed[K_RALT]) and keys_pressed[K_F4]:
        quitgame()

    # - Screen-clearing code:

    screen.fill(dark_green)

    # - Game logic and drawing code:

    draw_img("sprites/bottombox.png", 0, screen_height-25, center=False)
    draw_img("sprites/menubar.png", 0, 0, center=False)
    message_display("Money: " + str(Player.available_money), size=18, x=4, y=screen_height-24, center=False)

    # Debugging stuff:

    # message_display("Dealer value: " + str(Dealer.value), size=18, x=s_w-132, y=s_h-24, center=False)
    # message_display("Player value: " + str(Player.value), size=18, x=s_w-264, y=s_h-24, center=False)

    if betting:  # Betting stage.
        Bet.keep_in_valid_range()
        draw_img("sprites/cardback.png", y=-152, colorkey=keycolor)
        message_display("Welcome to blackjack.", x=0, y=0)
        message_display("Place your bet:", x=0, y=32)
        draw_img("sprites/betbox.png", 178, 400, center=False)
        numoffset = (len(str(Bet.value)) - 3) * 8
        message_display(str(Bet.value), x=16-numoffset, y=96, size=28)
        increasebutton.draw(x=286, y=400, action=Bet.add)
        decreasebutton.draw(x=286, y=416, action=Bet.sub)
        acceptbutton.draw(y=150, center=True, action=end_bet, act_on_release=True)
        if actiontimer:
            if Bet.value > Player.available_money:
                message_display("Insufficient funds.", y=200)
            if Player.surrendered:
                if actiontimer == 1:
                    Player.surrendered = False
                message_display("Player surrendered.", y=188)
                message_display("House takes half of bets.", y=212)
            actiontimer -= 1

    if playing:  # Starts the game.

        for card in Player.cards:
            card.draw()
        for card in Dealer.cards:
            card.draw()
        if len(Dealer.cards) < 2:
            draw_img("sprites/cardback.png", x=64, y=-152, colorkey=keycolor)

        if roundstart:
            message_display("Dealer's hand:", y=-225)
            message_display("Player's hand:", y=48)
            hitbutton.draw(x=-174, y=240, center=True, act_on_release=True, action=Player.hit)
            standbutton.draw(x=-103, y=240, center=True, act_on_release=True, action=Player.stand)
            doubledownbutton.draw(x=5, y=240, center=True, act_on_release=True, action=Player.dbl_down)
            surrenderbutton.draw(x=136, y=240, center=True, act_on_release=True, action=Player.surrender)
            if Player.value == 21 and len(Player.cards) == 2:
                Player.natural = True

        if standing:
            if actiontimer > 120:
                message_display("Player stood. Dealers turn.")
            elif actiontimer == 120:
                CardDraw(randint(0, 12), randint(0, 3), Dealer, x=64, y=-152)
                actiontimer -= 1
            if actiontimer <= 120:
                if not Dealer.holecardrevealed:
                    message_display("Dealer's hole card revealed.")
                if Dealer.holecardrevealed:
                    message_display("Dealer hits.")
            if not actiontimer and Dealer.value < 17:
                # Dealer doesn't stop hitting until their hand is at least 17.
                Dealer.holecardrevealed = True
                actiontimer = 120
            elif not actiontimer and Dealer.value >= 17:
                endgame = True
                standing = False
            else:
                actiontimer -= 1

        # Automatic win/lose conditions:

        if Player.natural:
            roundstart = False
            betting = False
            standing = False
            endgame = False
            message_display("Player got a natural 21!")
            message_display("You win!", y=24)
            won = True
            acceptbutton.draw(y=240, center=True, action=restartgame, act_on_release=True)

        if Player.value > 21 and not debugmode:
            if Player.gotace and Player.acecount == 0:
                Player.value -= 10
                Player.acecount += 1
            else:
                roundstart = False
                betting = False
                standing = False
                endgame = False
                message_display("Player busted.")
                message_display("You lose.", y=24)
                acceptbutton.draw(y=240, center=True, action=restartgame, act_on_release=True)
        if Dealer.value > 21:
            if Dealer.gotace and Dealer.acecount == 0:
                Dealer.value -= 10
                Dealer.acecount += 1
            else:
                roundstart = False
                betting = False
                standing = False
                endgame = False
                message_display("Dealer busted.")
                message_display("You win!", y=24)
                won = True
                acceptbutton.draw(y=240, center=True, action=restartgame, act_on_release=True)

        # Win/Lose conditions:

        if endgame:
            if Player.value > Dealer.value:
                message_display("Player's hand is greater than dealer's.")
                message_display("You win!", y=24)
                won = True
            elif Player.value < Dealer.value:
                message_display("Player's hand is less than dealer's.")
                message_display("You lose.", y=24)
            else:
                message_display("Player's hand is equal to dealer's.")
                message_display("Tie.", y=24)
                tie = True
            acceptbutton.draw(y=240, center=True, action=restartgame, act_on_release=True)

    pygame.display.update()
    fpsclock.tick(60)
