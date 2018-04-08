#Blackjack.

from random import randint
from random import choice

gametime = True

kingqueenjack = 10

kqjlist = ["King!", "Queen!", "Jack!"]

#----------------------------------------

while gametime is True: #Main game loop.

    playervalue = 0
    dealervalue = 0
    playerace = 11
    dealerace = 11

    playernumofaces = 0
    dealernumofaces = 0

    holeace = False
    holekqj = False
    holecard = 0
    revealhole = True

    playerinit = 0
    playerbusted = False
    dealerbusted = False
    playergotace = False
    dealergotace = False
    playerturn = False
    playerstand = False
    dealerturn = False
    roundstart = True
    surrender = False
    
    if roundstart is True:
        print ("Welcome to Blackjack.")
        print ("-")
        #Starts the round. Sets up the dealer's initial hand, and
        #gives the player their initial two cards.
        #Dealer's initial hand:
        cardpick = randint(1,14)
        print ("Dealer's initial hand:")
        if cardpick == 1:
            print ("Ace!")
            dealervalue += dealerace
            dealergotace = True
        elif cardpick > 10:
            print (choice(kqjlist))
            dealervalue += kingqueenjack
        else:
            print (str(cardpick))
            dealervalue += cardpick
        print ("Dealer's hand is worth " + str(dealervalue) + ".")
        #Dealer's hole (hidden/face down) card:
        cardpick = randint(1,14)
        if cardpick == 1:
            holeace = True
            dealervalue += dealerace
            dealergotace = True
        elif cardpick > 10:
            holekqj = True
            dealervalue += kingqueenjack
        else:
            holecard += cardpick
            dealervalue += cardpick
        print ("-")
        print ("Player's initial hand:")
        #Player's initial two cards:
        while playerinit < 2:
            cardpick = randint(1,14)
            if cardpick == 1:
                print ("Ace!")
                playervalue += playerace
                playergotace = True
            elif cardpick > 10:
                print (choice(kqjlist))
                playervalue += kingqueenjack
            else:
                print (str(cardpick))
                playervalue += cardpick
            playerinit += 1
        print ("Player's hand is worth " + str(playervalue) + ".")
        if playervalue == 21:
            #Checks if the player got 21 on the first two cards (blackjack/natural).
            print ("Player got a natural 21!")
            roundstart = False
            playerturn = False
            dealerturn = True
            print ("-")
        else:
            print ("-")
            roundstart = False
            playerturn = True
            print ("Player's turn.")
            #Ends the round start and begins the player's turn.

    while playerturn is True: #Player's turn.
        if (playervalue > 21 and playergotace is False) or (playervalue > 21 and playergotace is True and playerace == 1):
            #Checks if the player busted. Instant lose.
            playerturn = False
            dealerturn = False
            print ("-")
            break
        if (playervalue > 21 and playergotace is True and playerace == 11):
            #Checks if the player busted with an ace.
            print ("Player had a soft bust. Ace is now worth 1.")
            playerace = 1
            playervalue -= 10
            print ("Player's hand is now worth " + str(playervalue) + ".")
        print ("Choose to Hit (1), Stand (2), Double down (3), Split (4), or Surrender (5).")
        playerchoice = input("Choice: ")
        while playerchoice.isdigit() is False: #Checks if the input is a digit.
            print ("Invalid input.")
            playerchoice = input("Choice: ")
        if int(playerchoice) == 1: #If Hit is chosen, randomly selects a card.
            cardpick = randint(1,14)
            if cardpick == 1:
                print ("Ace!")
                playervalue += playerace
                playergotace = True
            elif cardpick > 10:
                print (choice(kqjlist))
                playervalue += kingqueenjack
            else:
                print (str(cardpick))
                playervalue += cardpick
            print ("Player's hand is worth " + str(playervalue) + ".")
        elif int(playerchoice) == 2: #If Stand is chosen, end turn.
            print ("Player stood.")
            print ("-")
            playerturn = False
            dealerturn = True
        elif int(playerchoice) == 3:
            print ("WIP")
        elif int(playerchoice) == 4:
            print ("WIP")
        elif int(playerchoice) == 5:
            print ("WIP")
        else: #If the inputted number is greater than 5.
            print ("Invalid input.")

    while dealerturn is True: #Dealer's turn.
        if revealhole is True: #Reveals the hole card.
            print ("Dealer's hole card revealed.")
            if holeace is True:
                print ("Ace!")
            elif holekqj is True:
                print (choice(kqjlist))
            else:
                print (str(holecard))
            print ("Dealer's hand is worth " + str(dealervalue) + ".")
            revealhole = False
        while dealervalue < 17: #Dealer keeps hitting until his hand is 17 or greater.
            print ("Dealer hits.")
            cardpick = randint(1,14)
            if cardpick == 1:
                print ("Ace!")
                dealervalue += dealerace
                dealergotace = True
            elif cardpick > 10:
                print (choice(kqjlist))
                dealervalue += kingqueenjack
            else:
                print (str(cardpick))
                dealervalue += cardpick
            print ("Dealer hand is worth " + str(dealervalue) + ".")
        if dealervalue >= 17 and dealergotace is True and dealerace == 11:
            #If the dealer's value is greater than or equal to 17,
            #the dealer got an ace, and he hasn't had his ace revalued to one (soft hand).
            print ("Dealer got a soft 17 (has ace card with a hand worth 17 or more).")
            dealerace = 1
            dealervalue -= 10
            print ("Dealer's hand is now worth " + str(dealervalue) + ".")
        if dealervalue == 21: #If the dealer got 21.
            print ("Dealer got 21!")
            print ("-")
            dealerturn = False
        if dealervalue > 21: #If the dealer got more than 21 (busted).
            print ("-")
            dealerturn = False
            break
        if (dealervalue >= 17 and dealergotace is False) or (dealervalue >= 17 and dealergotace is True and dealerace == 1):
            #If the dealer's hand is greater than or equal to 17 without an ace,
            #or the dealer's hand is greater than 17 with the ace already used (hard).
            print ("Dealer stood.")
            print ("-")
            dealerturn = False
            break

    if playervalue > 21:
        print ("Player busted! You lose.")
        playerbusted = True
    if dealervalue > 21:
        print ("Dealer Busted! You win!")
        dealerbusted = True
    if playerbusted is False and dealerbusted is False:
        if playervalue > dealervalue:
            print ("Player hand is greater than dealer's. You Win!")
        elif playervalue == dealervalue:
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
            gametime = False
            break
        else:
            print ("Invalid input.")
    print ("---")
    print ("--")
    print ("-")
