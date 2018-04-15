#Blackjack.

import sys
from random import randint, choice

#Strings (too long to fit in PEP-8 guidelines otherwise):

optionlist = "Hit (1), Stand (2), Double down (3), Split (4), or Surrender (5)."

#Classes:

class actor(object):
    '''actor class for variables and methods shared by player and dealer'''
    busted = False
    gotace = False
    turn = False
    numofaces = 0
    value = 0
    ace = 11
    kqjlist = ["King!", "Queen!", "Jack!"]
    kingqueenjack = 10
    def __init__(self):
        pass
    def gethand(self, nowworth):
        '''Print's the person's hand. "nowworth" is a boolean for printing
           "X's hand is now worth Y." instead of "X's hand is worth Y."'''
        if nowworth:
            print ("%s's hand is now worth %i."%(self.name, self.value))
        print ("%s's hand is worth %i."%(self.name, self.value))
    def silentcardpick(self):
        '''Picks card with no announcement.'''
        cpick = randint(1,14)
        if cpick == 1:
            print ("Ace!")
            self.value += self.ace
            self.gotace = True
        elif cpick > 10:
            print (choice(self.kqjlist))
            self.value += self.kingqueenjack
        else:
            print (str(cpick))
            self.value += cpick        
    def cardpick(self):
        '''Picks card with announcement.'''
        self.silentcardpick()
        self.gethand(False)
    def softace(self):
        '''Sets the ace's value to 1 and lower's the person's value by 10.'''
        self.ace = 1
        self.value -= 10
        self.gethand(True)

class d(actor):
    '''Dealer class.'''
    name = "Dealer"
    holeace = False
    holekqj = False
    holecard = 0
    revealhole = True
    def __init__(self):
        pass
    def holecardpick(self):
        '''Picks the dealer's hole card.'''
        cpick = randint(1,14)
        if cpick == 1:
            self.holeace = True
            self.value += self.ace
            self.gotace = True
        elif cpick > 10:
            self.holekqj = True
            self.value += self.kingqueenjack
        else:
            self.holecard = cpick
            self.value += cpick
    def revealholepick(self):
        '''Reveals the dealer's hole card.'''
        print ("Dealer's hole card revealed.")
        if self.holeace:
            print ("Ace!")
        elif self.holekqj:
            print (choice(self.kqjlist))
        else:
            print (str(self.holecard))

class p(actor):
    '''Player class.'''
    name = "Player"
    stand = False
    surrender = False
    def __init__(self):
        pass

##################

playing = True

while playing:

    #Game variables, reset each round:
    
    dealer = d()
    player = p()
    roundstart = True

    if roundstart:
        #Starts the round. Sets up the dealer's initial hand,
        #dealer's hole (hidden/face down) card, and
        #gives the player their initial two cards.
        
        print ("Welcome to blackjack.\n---\nDealer's initial hand:")
        dealer.cardpick()
        dealer.holecardpick()
        
        #Player's initial two cards:
        
        print ("-\nPlayer's initial hand:")
        player.silentcardpick()
        player.cardpick()
        if player.value == 21:
            #Checks if player got 21 on first two cards (blackjack/natural).
            print ("Player got a natural 21!\n-")
            player.turn = False
            dealer.turn = True
        else:
            player.turn = True
            print ("-\nPlayer's turn.")
        roundstart = False

    #Player's turn.
    while player.turn:
        if (player.value > 21 and not player.gotace)\
           or (player.value > 21 and player.gotace and player.ace == 1):
            #Checks if the player busted. Instant lose.
            player.turn = False
            dealer.turn = False
            break
        if player.value > 21 and player.gotace and player.ace == 11:
            #Checks if the player busted with one ace.
            print ("Player had a soft bust. Ace is now worth 1.")
            player.softace()
        pchoice = input("Choose to %s\n"%(optionlist) + "Choice: ")
        while not pchoice.isdigit() or int(pchoice) not in range(1,6):
            #If the choice is not a digit or not in the range of choices.
            print ("Invalid input.")
            pchoice = input("Choice: ")
        if int(pchoice) == 1:
            #If Hit is chosen, randomly selects a card.
            player.cardpick()
        elif int(pchoice) == 2:
            #If Stand is chosen, end turn.
            print ("Player stood.\n-")
            player.turn = False
            dealer.turn = True
        elif int(pchoice) in range(3,6):
            print ("WIP")

    #Dealer's turn.
    while dealer.turn:
        if dealer.revealhole:
            #Reveals the hole card.
            dealer.revealholepick()
            dealer.revealhole = False
        if dealer.value < 17:
            #Dealer keeps hitting until their hand is 17 or greater.
            dealer.cardpick()
        if dealer.value >= 17 and dealer.gotace and dealer.ace == 11:
            #If the dealer's value is greater than or equal to 17,
            #the dealer got an ace, and he hasn't had his ace
            #revalued to one (soft hand).
            print ("Dealer got a soft 17. Ace is now worth 1.")
            dealer.softace()
        if dealer.value == 21:
            #If the dealer got 21.
            print ("Dealer got 21!\n-")
            dealer.turn = False
        if dealer.value > 21:
            #If the dealer got more than 21 (busted).
            print ("-")
            dealer.turn = False
        if (dealer.value >= 17 and not dealer.gotace)\
           or (dealer.value >= 17 and dealer.gotace and dealer.ace == 1):
            #If the dealer's hand is >= 17 without an ace,
            #or the dealer's hand  is > 17 with the ace already used (hard).
            print ("Dealer stood.\n-")
            dealer.turn = False
            break

    #Game condition check:
    if player.value > 21:
        print ("Player busted! You lose.")
        player.busted = True
    if dealer.value > 21:
        print ("Dealer busted! You win!")
        dealer.busted = True
    if not (player.busted or dealer.busted):
        if player.value > dealer.value:
            print ("Player hand is greater than dealer's. You Win!")
        elif player.value == dealer.value:
            print ("Player's hand is the same as the dealer's. Tie.")
        else:
            print ("Player's hand is less than dealer's. You Lose.")

    #Resets the game.
    print ("-")
    while True:
        print ("New game? y/n")
        newgameinput = input("Choice: ")
        if newgameinput in "Yy":
            break
        elif newgameinput in "Nn":
            sys.exit()
        print ("Invalid input.")
    print ("---\n--\n-")
