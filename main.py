import random

pot = 100
def createDeck():
    suits = ['Heart', 'Diamond', 'Spade', 'Club']
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    return [[rank, "of", suit] for suit in suits for rank in ranks]

def shuffleDeck(deck):
    random.shuffle(deck)
    return deck

def getBet():
    bet = 0
    while bet == 0:
        bet = int(input("How much will you bet? "))
        if bet > pot:
            print("You are betting more than you have, try again ")
            bet = 0
        else:
            return bet

def initialise_blackjack():
    shuffledDeck = shuffleDeck(createDeck())
    playerHand = []
    dealerHand = []
    for i in range(2):
        playerHand.append(shuffledDeck.pop())
        dealerHand.append(shuffledDeck.pop())
    return playerHand, dealerHand, shuffledDeck

def mimic_blackjack(playerHand, dealerHand, shuffledDeck):
    if blackjackCheck(dealerHand) == True and blackjackCheck(playerHand) == True:
        print("PUSH")
        return 0
    elif blackjackCheck(dealerHand):
        print("Dealer wins, Blackjack")
        return -1
    elif blackjackCheck(playerHand):
        print("Player wins 3/2 payout")
        return 1.5
    else:
        playerHand = mimic_the_dealer(playerHand, shuffledDeck)
        if handValue(playerHand) > 21:
            print("Player bust")
            return -1
        print("ONE", len(shuffledDeck))
        dealerPlay(dealerHand, shuffledDeck)
        print("TWO", len(shuffledDeck))
        print(f"Player hand: {playerHand} \n Dealer hand: {dealerHand}")
        if handValue(dealerHand) > 21:
            print("Dealer bust")
            return 1
        elif handValue(dealerHand) == handValue(playerHand):
            print("PUSH")
            return 0
        elif handValue(dealerHand) > handValue(playerHand):
            print("DEALER WIN")
            return -1
        else:
            print("PLAYER WIN")
            return 1

def never_bust_blackjack(playerHand, dealerHand, shuffledDeck):
    if blackjackCheck(dealerHand) == True and blackjackCheck(playerHand) == True:
        print("PUSH")
        return 0
    elif blackjackCheck(dealerHand):
        print("Dealer wins, Blackjack")
        return -1
    elif blackjackCheck(playerHand):
        print("Player wins 3/2 payout")
        return 1.5
    else:
        playerHand = never_bust(playerHand, shuffledDeck)
        if handValue(playerHand) > 21:
            print("Player bust")
            return -1
        print("ONE", len(shuffledDeck))
        dealerPlay(dealerHand, shuffledDeck)
        print("TWO", len(shuffledDeck))
        print(f"Player hand: {playerHand} \n Dealer hand: {dealerHand}")
        if handValue(dealerHand) > 21:
            print("Dealer bust")
            return 1
        elif handValue(dealerHand) == handValue(playerHand):
            print("PUSH")
            return 0
        elif handValue(dealerHand) > handValue(playerHand):
            print("DEALER WIN")
            return -1
        else:
            print("PLAYER WIN")
            return 1
        
def bs_blackjack(playerHand, dealerHand, shuffledDeck):
    if blackjackCheck(dealerHand) == True and blackjackCheck(playerHand) == True:
        print("PUSH")
        return 0
    elif blackjackCheck(dealerHand):
        print("Dealer wins, Blackjack")
        return -1
    elif blackjackCheck(playerHand):
        print("Player wins 3/2 payout")
        return 1.5
    else:
        playerHand = basic_strategy(playerHand, dealerHand[0], shuffledDeck)
        if handValue(playerHand) > 21:
            print("Player bust")
            return -1
        print("ONE", len(shuffledDeck))
        dealerPlay(dealerHand, shuffledDeck)
        print("TWO", len(shuffledDeck))
        print(f"Player hand: {playerHand} \n Dealer hand: {dealerHand}")
        if handValue(dealerHand) > 21:
            print("Dealer bust")
            return 1
        elif handValue(dealerHand) == handValue(playerHand):
            print("PUSH")
            return 0
        elif handValue(dealerHand) > handValue(playerHand):
            print("DEALER WIN")
            return -1
        else:
            print("PLAYER WIN")
            return 1

def blackjack():
    result = 1
    strategy = input("What strategy would you like to play? ")
    global pot
    shuffledDeck = shuffleDeck(createDeck())
    play = "Y"
    while play.upper() == "Y": 
        bet = getBet()
        playerHand = []
        dealerHand = []
        # playerHand = [shuffledDeck.pop(), shuffledDeck.pop()]
        # dealerHand = [shuffledDeck.pop(), shuffledDeck.pop()]


        #playerHand = [['4', 'of', 'Club'], ['4', 'of', 'Spade']]
        print(f"Player Hand: {playerHand}")
        # print(f"Dealer Hand: {dealerHand}")
        print(f"Dealer Hand: {dealerHand[0]}, HIDDEN CARD")
        
        if blackjackCheck(dealerHand) == True and blackjackCheck(playerHand) == True:
            print("PUSH")
        elif blackjackCheck(dealerHand):
            print("Dealer wins, Blackjack")
            pot -= bet
            play = input("Do you want to play? Y/N ")
        elif blackjackCheck(playerHand):
            print("Player wins 3/2 payout")
            pot += bet*1.5
            play = input("Do you want to play? Y/N ")
            print(f"Pot: {pot}")
        else:
            print("HELLO")
            if strategy.lower() != "mimic_dealer":
                if playerHand[0][0] == playerHand[1][0]:
                    action = input("Hit, Stand, Split or Double? ")
                    if action.lower() == "split":
                        splitResult = splitFunction(playerHand, shuffledDeck, dealerHand)
                        for result in splitResult:
                            pot += bet*result
                    else:
                        pass
                else:
                    print("HELLO2")
                    result = playHand(playerHand, shuffledDeck)
                    if result < 0:
                        pot += bet*result
                    else:
                        print(handValue(dealerHand))
                        dealerPlay(dealerHand, shuffledDeck)
                        print(handValue(dealerHand))
            else:
                print("Mimic the Dealer strategy: ")
                playerHand = mimic_the_dealer(playerHand, shuffledDeck)
                dealerPlay(dealerHand, shuffledDeck)
                print(f"Player hand: {playerHand} \n Dealer hand: {dealerHand}")
            if handValue(dealerHand) > 21:
                print("Dealer bust")
                pot += bet*result
            elif handValue(playerHand) > 21:
                print("Player bust")
                pot -= bet*result
            elif handValue(dealerHand) == handValue(playerHand):
                print("PUSH")
            elif handValue(dealerHand) > handValue(playerHand):
                print("DEALER WIN")
                pot -= bet*result
            else:
                print("PLAYER WIN")
                pot += bet*result
        print(f"Pot after hand: {pot}")
        print(pot, result, bet)
        if pot > 0:
            play = input("Do you want to play? Y/N ")
        else:
            print("Ran out of money")
            play = "N"


def handValue(hand):
    total = 0
    ace = 0
    for i in range (len(hand)):
        if hand[i][0] == "J" or hand[i][0] == "Q" or hand[i][0] == "K":
            total += 10
        elif hand[i][0] == "A":
            total += 11
            ace += 1
        else:
            total += int(hand[i][0])
    while total > 21 and ace > 0:
        total -= 10
        ace -= 1
    return total
        # for j in range(len(hand)):
        #     if hand[j][0] == "A" and total+int(hand[i][0]) > 21:
        #         total += int(hand[i][0])-10
        #         return total
        #     else:
        #         total += int(hand[i][0])
        #         return total
        # total += int(hand[i][0])
def blackjackCheck(hand):
    if hand[0][0] == "J" or hand[0][0] == "Q" or hand[0][0] == "K" or hand[0][0] == "10":
        if hand[1][0] == "A":
            return True
    elif hand[0][0] == "A":
        if hand[1][0] == "J" or hand[1][0] == "Q" or hand[1][0] == "K" or hand[1][0] == "10":
            return True
    else:
        return False

def playHand(playerHand, shuffledDeck):
    counter = 0
    gameOver = False
    while gameOver == False:
        if counter == 0:
            action = input("Hit, Stand or Double? ")
            if action.lower() == "hit":
                counter += 1
                playerHand.append(shuffledDeck.pop())
                print(f"Player Hand: {playerHand}")
                print(f"Player hand value: {handValue(playerHand)}")
                if handValue(playerHand) > 21:
                    print("Bust!")
                    return 1
            elif action.lower() == "stand":
                return 1
            elif action.lower() == "double":
                counter += 1
                playerHand.append(shuffledDeck.pop())
                print(f"Player Hand: {playerHand}")
                if handValue(playerHand) > 21:
                    print("Bust!")
                    return -2
                else:
                    return 2
        elif counter != 0:
            action = input("Hit or Stand? ")
            if action.lower() == "hit":
                playerHand.append(shuffledDeck.pop())
                print(f"Player Hand: {playerHand}")
                print(f"Player hand value: {handValue(playerHand)}")
                if handValue(playerHand) > 21:
                    print("Bust!")
                    return -1
            elif action.lower() == "stand":
                return 1
            
def dealerPlay(dealerHand, shuffledDeck):
    print(f"Dealers hand: {dealerHand}")
    while handValue(dealerHand) < 17:
        dealerHand.append(shuffledDeck.pop())
        print(f"Dealers hand: {dealerHand}")


def splitFunction(playerHand, shuffledDeck, dealerHand):
    print("HELLOOO")
    total = []
    playerHand2 = [playerHand.pop()]
    playerHand.append(shuffledDeck.pop())
    print(f"Player Hand: {playerHand}")
    playerHand2.append(shuffledDeck.pop())
    print(f"Split Player Hand: {playerHand2}")
    result1 = playHand(playerHand, shuffledDeck)
    result2 = playHand(playerHand2, shuffledDeck)
    results = [result1, result2]
    playerHands = [playerHand, playerHand2]
    print("RESULTS:" ,results)
    for result, playerH in zip(results, playerHands):
        print(f"Player Hand11111111111: {playerH}")
        if result < 0:
            print(f"DEALER: {handValue(dealerHand)}")
            print(f"PLAYER: {handValue(playerH)}")
            total.append(result)
        else:
            dealerPlay(dealerHand, shuffledDeck)
            print(f"DEALER: {handValue(dealerHand)}")
            print(f"PLAYER: {handValue(playerH)}")

            if handValue(dealerHand) > 21:
                print("Dealer bust")
                total.append(1*result)
            elif handValue(dealerHand) == handValue(playerH):
                print("PUSH")
                total.append(0)
            elif handValue(dealerHand) > handValue(playerH):
                print("DEALER WIN")
                total.append(-1*result)
            else:
                print("PLAYER WIN")
                total.append(1*result)
    print(total)
    return total

def mimic_the_dealer(playerHand, shuffledDeck):
    print("FIRST", playerHand)
    while handValue(playerHand) < 17:
        print("MIMIC VALUE:", handValue(playerHand))
        playerHand.append(shuffledDeck.pop())
        print(playerHand)
    return playerHand

<<<<<<< HEAD
def never_bust(playerHand, shuffledDeck):
    while handValue(playerHand) < 12:
        # hit on 11 and below
        print(f"Never bust value: {handValue(playerHand)}")
        playerHand.append(shuffledDeck.pop())
        print(playerHand)
    return playerHand

=======
def basic_strategy(playerHand, dealerCard, shuffledDeck):
    completed = False
    dealerValue = handValue(dealerCard)
    # check if player hand is hard or soft (no aces)
    if playerHand[0][0] == 'A' or playerHand[0][1] == 'A':
        while completed == False:
            if playerHand[0][0] == 'A':
                if playerHand[1][0] == 9:
                    # stand on 9
                    return 1
                elif playerHand[1][0] == 8 and dealerValue in [2, 3, 4, 5, 7, 8, 9, 10, 11]:
                    #stand
                    return 1
                elif playerHand[1][0] == 8 and dealerValue == 6:
                    #Double
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                    completed = True
                elif playerHand[1][0] == 7 and dealerValue in range(2, 6):
                    # Double
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                    completed = True
                elif playerHand[1][0] == 7 and dealerValue in range(7, 8):
                    # stand
                    return 1
                elif playerHand[1][0] == 7 and dealerValue in range(9, 11):
                    # Hit 
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                elif playerHand[1][0] == 6 and dealerValue == 2:
                    # hit
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                elif playerHand[1][0] == 6 and dealerValue in range(3, 4):
                    # Double
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                    completed = True
                elif playerHand[1][0] in range(2, 6) and dealerValue in [2, 7, 8, 9, 10, 11]:
                    # hit
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                elif playerHand[1][0] in range(2, 6) and dealerValue in range(5,6):
                    # Double
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                    completed = True
                elif playerHand[1][0] in range(2, 5) and dealerValue in range(2,3):
                    # hit
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                elif playerHand[1][0] in [4, 5] and dealerValue == 4:
                    # double
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                    completed = True
                elif playerHand in [2, 3] and dealerValue == 4:
                    # hit
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
            elif playerHand[1][0] == 'A':
                if playerHand[0][0] == 9:
                    # stand on 9
                    return 1
                elif playerHand[0][0] == 8 and dealerValue in [2, 3, 4, 5, 7, 8, 9, 10, 11]:
                    #stand
                    return 1
                elif playerHand[0][0] == 8 and dealerValue == 6:
                    #Double
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                    completed = True
                elif playerHand[0][0] == 7 and dealerValue in range(2, 6):
                    # Double
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                    completed = True
                elif playerHand[0][0] == 7 and dealerValue in range(7, 8):
                    # stand
                    return 1
                elif playerHand[0][0] == 7 and dealerValue in range(9, 11):
                    # Hit 
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                elif playerHand[0][0] == 6 and dealerValue == 2:
                    # hit
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                elif playerHand[0][0] == 6 and dealerValue in range(3, 4):
                    # Double
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                    completed = True
                elif playerHand[0][0] in range(2, 6) and dealerValue in [2, 7, 8, 9, 10, 11]:
                    # hit
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                elif playerHand[0][0] in range(2, 6) and dealerValue in range(5,6):
                    # Double
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                    completed = True
                elif playerHand[0][0] in range(2, 5) and dealerValue in range(2,3):
                    # hit
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                elif playerHand[0][0] in [4, 5] and dealerValue == 4:
                    # double
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                    completed = True
                elif playerHand in [2, 3] and dealerValue == 4:
                    # hit
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")          
                
    # need a while loop that keeps checking if the hand are these values until a certain point
    completed = False
    while completed == False:
        if handValue(playerHand) > 16: # Stands on any value above 16, no matter what the dealers up card is
            return 1
        elif handValue(playerHand) in range(13,16) and dealerValue in range(2, 6):
            return 1
        elif handValue(playerHand) in range(13,16) and dealerValue in range(7, 11):
            # hit
            playerHand.append(shuffledDeck.pop())
            print(f"Player Hand: {playerHand}")
        elif handValue(playerHand) == 12 and dealerValue in [2, 3, 7, 8, 9, 10, 11]:
            #hit
            playerHand.append(shuffledDeck.pop())
            print(f"Player Hand: {playerHand}")
        elif handValue(playerHand) == 12 and dealerValue in range(4, 6):
            return 1
        elif handValue(playerHand) == 11:
            # Double
            playerHand.append(shuffledDeck.pop())
            print(f"Player Hand: {playerHand}")
            completed = True
        elif handValue(playerHand) == 10 and dealerValue in range(2, 9):
            # Double
            playerHand.append(shuffledDeck.pop())
            print(f"Player Hand: {playerHand}")
            completed = True
        elif handValue(playerHand) == 10 and dealerValue in range(10, 11):
            # hit
            playerHand.append(shuffledDeck.pop())
            print(f"Player Hand: {playerHand}")
        elif handValue(playerHand) == 9 and dealerValue in [2, 7, 8, 9, 10, 11]:
            # hit
            playerHand.append(shuffledDeck.pop())
            print(f"Player Hand: {playerHand}")
        elif handValue(playerHand) == 9 and dealerValue in range(3,6):
            # double 
            playerHand.append(shuffledDeck.pop())
            print(f"Player Hand: {playerHand}")
            completed = True
        elif handValue(playerHand) == 8:
            # hit 
            playerHand.append(shuffledDeck.pop())
            print(f"Player Hand: {playerHand}")
>>>>>>> ddabca525ed7f6ff7ce2ec1107c4ac4c6d8510d2

def basic_strategy(playerHand, dealerHand, shuffledDeck):
   
    print(type(handValue(playerHand)))
    if dealerHand[0][0] in ['J', 'Q', 'K']:
        dealerCard = 10
    elif dealerHand[0][0] == 'A':
        dealerCard = 11
    else:
        dealerCard = int(dealerHand[0][0])
    print(f"Player Hand: {playerHand}")
    print(f"Dealer Card: {dealerCard}")
    hardHands = {
        21: {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        20: {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        19: {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        18: {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        17: {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        16: {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        15: {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        14: {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        13: {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        12: {2: "Hit", 3: "Hit", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        11: {2: "Double", 3: "Double", 4: "Double", 5: "Double", 6: "Double", 7: "Double", 8: "Double", 9: "Double", 10: "Double", 11: "Double"},
        10: {2: "Double", 3: "Double", 4: "Double", 5: "Double", 6: "Double", 7: "Double", 8: "Double", 9: "Double", 10: "Hit", 11: "Hit"},
        9: {2: "Hit", 3: "Double", 4: "Double", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        8: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        7: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        6: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        5: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        4: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        3: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        2: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"}
      }
    
    softHands = {
        20: {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        19: {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Double", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        18: {2: "Double", 3: "Double", 4: "Double", 5: "Double", 6: "Double", 7: "Stand", 8: "Stand", 9: "Hit", 10: "Hit", 11: "Hit"},
        17: {2: "Hit", 3: "Double", 4: "Double", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        16: {2: "Hit", 3: "Hit", 4: "Double", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        15: {2: "Hit", 3: "Hit", 4: "Double", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        14: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        13: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"}
    }

    pairSplit = {
        ('A', 'A'): {2: "Yes", 3: "Yes", 4: "Yes", 5: "Yes", 6: "Yes", 7: "Yes", 8: "Yes", 9: "Yes", 10: "Yes", 11: "Yes"},
        ('K', 'K'): {2: "No", 3: "No", 4: "No", 5: "No", 6: "No", 7: "No", 8: "No", 9: "No", 10: "No", 11: "No"},
        ('Q', 'Q'): {2: "No", 3: "No", 4: "No", 5: "No", 6: "No", 7: "No", 8: "No", 9: "No", 10: "No", 11: "No"},
        ('J', 'J'): {2: "No", 3: "No", 4: "No", 5: "No", 6: "No", 7: "No", 8: "No", 9: "No", 10: "No", 11: "No"},
        (10, 10): {2: "No", 3: "No", 4: "No", 5: "No", 6: "No", 7: "No", 8: "No", 9: "No", 10: "No", 11: "No"},
        (9, 9): {2: "Yes", 3: "Yes", 4: "Yes", 5: "Yes", 6: "Yes", 7: "No", 8: "Yes", 9: "Yes", 10: "No", 11: "No"},
        (8, 8): {2: "Yes", 3: "Yes", 4: "Yes", 5: "Yes", 6: "Yes", 7: "Yes", 8: "Yes", 9: "Yes", 10: "Yes", 11: "Yes"},
        (7, 7): {2: "Yes", 3: "Yes", 4: "Yes", 5: "Yes", 6: "Yes", 7: "Yes", 8: "No", 9: "No", 10: "No", 11: "No"},
        (6, 6): {2: "No", 3: "Yes", 4: "Yes", 5: "Yes", 6: "Yes", 7: "No", 8: "No", 9: "No", 10: "No", 11: "No"},
        (5, 5): {2: "No", 3: "No", 4: "No", 5: "No", 6: "No", 7: "No", 8: "No", 9: "No", 10: "No", 11: "No"},
        (4, 4): {2: "No", 3: "No", 4: "No", 5: "No", 6: "No", 7: "No", 8: "No", 9: "No", 10: "No", 11: "No"},
        (3, 3): {2: "No", 3: "No", 4: "Yes", 5: "Yes", 6: "Yes", 7: "Yes", 8: "No", 9: "No", 10: "No", 11: "No"},
        (2, 2): {2: "No", 3: "No", 4: "Yes", 5: "Yes", 6: "Yes", 7: "Yes", 8: "No", 9: "No", 10: "No", 11: "No"}
    }


    # initially check for blackjack (maybe in the function before)
    # then check for a pair, deal with the pair
    # then check if an there is an ace in either of the two cards then use soft totals
    # if not then use hard totals

    if playerHand[0][0] == playerHand[1][0]:
        action = pairSplit.get((playerHand[0][0], playerHand[1][0])).get(dealerCard)
        print(action)
    else:
        if playerHand[0][0] == 'A' or playerHand[1][0] == 'A':
            action = softHands.get(handValue(playerHand), {}).get(dealerCard, "dk")
            print(action)
        else:
            action = hardHands.get(handValue(playerHand), {}).get(dealerCard, "dk")
            print(action)

    

# ph, dh, d = initialise_blackjack()
# results = []
#
# num = int(input("How many hands: "))
#
#     for i in range(num):
#         result = mimic_blackjack(ph, dh, d)
#         if result > 0:
#             results.append("WIN")
#         elif result < 0:
#             results.append("LOSS")
#         else:
#             results.append("PUSH")
#     print(results)
# elif choice.lower() == "normal":
#     blackjack()

def main_mimic():
    deck = shuffleDeck(createDeck())
    results = []
    num = int(input("How many hands: "))

    for i in range(num):
        print(f"Hand number: {i}")
        if len(deck) < 10:
            print("Reshuffling deck")
            deck = shuffleDeck(createDeck())
        playerHand = []
        dealerHand = []
        for j in range(2):
            playerHand.append(deck.pop())
            dealerHand.append(deck.pop())
        result = mimic_blackjack(playerHand, dealerHand, deck)
        if result > 0:
            results.append("WIN")
        elif result < 0:
            results.append("LOSS")
        else:
            results.append("PUSH")
    print(results)

def main_never_bust():
    deck = shuffleDeck(createDeck())
    results = []
    num = int(input("How many hands: "))

    for i in range(num):
        print(f"Hand number: {i}")
        if len(deck) < 10:
            print("Reshuffling deck")
            deck = shuffleDeck(createDeck())
        playerHand = []
        dealerHand = []
        for j in range(2):
            playerHand.append(deck.pop())
            dealerHand.append(deck.pop())
        result = never_bust_blackjack(playerHand, dealerHand, deck)
        if result > 0:
            results.append("WIN")
        elif result < 0:
            results.append("LOSS")
        else:
            results.append("PUSH")
    print(results)

def basic_strategy_main():
    deck = shuffleDeck(createDeck())
    results = []
    num = int(input("How many hands: "))
    for i in range(num):
        print(f"Hand number: {i}")
        if len(deck) < 10:
            print("Reshuffling deck")
            deck = shuffleDeck(createDeck())
        playerHand = []
        dealerHand = []
        for j in range(2):
            playerHand.append(deck.pop())
            dealerHand.append(deck.pop())
        result = basic_strategy(playerHand, dealerHand, deck)
        if result > 0:
            results.append("WIN")
        elif result < 0:
            results.append("LOSS")
        else:
            results.append("PUSH")
    print(results)

choice = input("Normal, Mimic The Dealer, Never Bust or Basic Strategy? ")
if choice.lower() == "mimic":
    main_mimic()
elif choice.lower() == "never":
    main_never_bust()
elif choice.lower() == "basic":
    basic_strategy_main()
elif choice.lower() == "normal":
    blackjack()


