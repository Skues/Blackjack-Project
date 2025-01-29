import random

def printFunc(cards):
    for card in cards:
        print(*card)

pot = 100
def createDeck():
    suits = ['Heart', 'Diamond', 'Spade', 'Club']
    ranks = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
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
    print(f"Player hand: {playerHand}")
    print(f"Dealer card: {dealerHand[0]}")
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
        playerHand, mult = basic_strategy(playerHand, dealerHand, shuffledDeck)
        if mult < 0:
            print("Player bust")
            return -1
        dealerPlay(dealerHand, shuffledDeck)
        print(f"Player hand: {playerHand} \n Dealer hand: {dealerHand}")
        if handValue(dealerHand) > 21:
            print("Dealer bust")
            return 1*mult
        elif handValue(dealerHand) == handValue(playerHand):
            print("PUSH")
            return 0
        elif handValue(dealerHand) > handValue(playerHand):
            print("DEALER WIN")
            return -1*mult
        else:
            print("PLAYER WIN")
            return 1*mult

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
        playerHand = [shuffledDeck.pop(), shuffledDeck.pop()]
        dealerHand = [shuffledDeck.pop(), shuffledDeck.pop()]


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

def never_bust(playerHand, shuffledDeck):
    while handValue(playerHand) < 12:
        # hit on 11 and below
        print(f"Never bust value: {handValue(playerHand)}")
        playerHand.append(shuffledDeck.pop())
        print(playerHand)
    return playerHand
    
def basic_strategy(playerHand, dealerHand, shuffledDeck):

    if dealerHand[0][0] in ['J', 'Q', 'K']:
        dealerCard = 10
    elif dealerHand[0][0] == 'A':
        dealerCard = 11
    else:
        dealerCard = int(dealerHand[0][0])
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
        ('A', 10): {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        ('A', 9): {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        ('A', 8): {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Double", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        ('A', 7): {2: "Double", 3: "Double", 4: "Double", 5: "Double", 6: "Double", 7: "Stand", 8: "Stand", 9: "Hit", 10: "Hit", 11: "Hit"},
        ('A', 6): {2: "Hit", 3: "Double", 4: "Double", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        ('A', 5): {2: "Hit", 3: "Hit", 4: "Double", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        ('A', 4): {2: "Hit", 3: "Hit", 4: "Double", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        ('A', 3): {2: "Hit", 3: "Hit", 4: "Hit", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        ('A', 2): {2: "Hit", 3: "Hit", 4: "Hit", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"}
        # SOFT hands only count on the first two cards so (A, 2) or (A, 9) not having multiple cards with an ace??
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
    counter = 0
    completed = False
    while completed == False:
        if handValue(playerHand) > 21:
            completed = True
            return playerHand, -1
        if playerHand[0][0] == playerHand[1][0] and counter == 0:
            print("PAIR")
            # playerHands = [0, 0]
            # for i in range(len(playerHand)):
            #     if 
            #     if isinstance(int(playerHand[i][0]), int):
            #         playerHands[i] = int(playerHand[i][0]) 
            #     else:
            #         playerHands[i] = playerHand[i][0]
            #     if playerHand[i][0] in ['J', 'Q', 'K']:
            #         playerHands[i] = 10
            #     elif playerHand[i][0] == 'A':
            #         playerHands[i] = 11
            #     else:
            #         playerHands[i] = int(playerHand[i][0])
            print(playerHand)
            action = pairSplit.get((playerHand[0][0], playerHand[1][0])).get(dealerCard, "dk")
            print(action)
            if action == "dk":
                print(f"DK ERROR: {playerHand} and {dealerCard}")
                break
            if action == "Yes":
                print("SPLITTT")
                counter += 1
                return playerHand, bs_split(playerHand, dealerHand, shuffledDeck)
            counter += 1
        if handType(playerHand) == "soft" and playerHand[0][0] == 'A' or playerHand[1][0] == 'A' and playerHand[0][0] != playerHand[1][0]:
            print("SOFT")
            print(handType(playerHand))
            temp = ""
            for i in range(len(playerHand)):
                print(len(playerHand))
                if playerHand[i][0] == 'A':
                    print("YEP")
                    temp = playerHand.pop(i)
                    print(temp, playerHand)
                    break
            playerHand.insert(0, temp)
            action = softHands.get((playerHand[0][0], handValue(playerHand[1:])), {}).get(dealerCard, "dk")
            # action = softHands.get(handValue(playerHand), {}).get(dealerCard, "dk")
            if action == "dk":
                print(f"DK ERROR: {playerHand} and {dealerCard}")
                break
            print(action)
            if action == "Hit":
                playerHand.append(shuffledDeck.pop())
                print(f"AFTER HIT: {playerHand}")
            elif action == "Double":
                playerHand.append(shuffledDeck.pop())
                completed = True
                return playerHand, 2
            elif action == "Stand":
                completed = True
                print("STAND")
                print(playerHand, "STANDING")
                return playerHand, 1
        else:
            print("HARD")
            action = hardHands.get(handValue(playerHand), {}).get(dealerCard, "dk")
            if action == "dk":
                print(f"DK ERROR: {playerHand} and {dealerCard}")
                break
            print(action)
            if action == "Hit":
                playerHand.append(shuffledDeck.pop())
                print(f"AFTER HIT: {playerHand}")
            elif action == "Double":
                playerHand.append(shuffledDeck.pop())
                print(f"AFTER DOUBLE: {playerHand}")
                completed = True
                return playerHand, 2
            elif action == "Stand":
                print(f"AFTER STAND: {playerHand}")

                completed = True
                return playerHand, 1

def bs_split(playerHand, dealerHand, shuffledDeck):
    playerHand2 = [playerHand.pop()]
    playerHand.append(shuffledDeck.pop())
    playerHand2.append(shuffledDeck.pop())
    hand1, result1 = basic_strategy(playerHand, dealerHand, shuffledDeck)
    hand2, result2 = basic_strategy(playerHand2, dealerHand, shuffledDeck)

    total = result1 + result2

    return total

    
def handType(hand):
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
    while ace > 0:
        if total > 21:
            return "hard"
        else:
            return "soft"

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
    # results = []
    results = 0
    wins = 0
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
        result = bs_blackjack(playerHand, dealerHand, deck)
        results += result
        if result > 0:
            wins += 1
        # if result > 1:
        #     results.append("D WIN")
        # elif result > 0:
        #     results.append("WIN")
        # elif result < -1:
        #     results.append("D LOSS")
        # elif result < 0:
        #     results.append("LOSS")
        # else:
        #     results.append("PUSH")
    print(results)
    print(f"Win rate: {(wins/num)*100}%")

choice = input("Normal, Mimic The Dealer, Never Bust or Basic Strategy? ")
if choice.lower() == "mimic":
    main_mimic()
elif choice.lower() == "never":
    main_never_bust()
elif choice.lower() == "basic":
    basic_strategy_main()
elif choice.lower() == "normal":
    blackjack()
