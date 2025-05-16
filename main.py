import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
hasSplit = False

# def printFunc(cards):
#     for card in cards:
#         print(*card)

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
        
def update_count(card, strategy):
    global running_count
    if strategy == "hilo":
        card_value = {2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0, 10: -1, "J": -1, "Q": -1, "K": -1, "A": -1}
    elif strategy == "omega":
        card_value = {2: 1, 3: 1, 7: 1, 4: 2, 5: 2, 6: 2, 9: -1, 10: -2, "J": -2, "Q": -2, "K": -2, "A": -2, 8: 0}
    elif strategy == "wong":
        card_value = {3: 1, 4: 1, 6: 1, 2: 0.5, 7: 0.5, 5: 1.5, 8: 0, 9:-0.5, 10: -1, "J": -1, "Q": -1, "K": -1, "A": -1}
    running_count += card_value.get(card[0], 0)


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
        #print("PUSH")
        return 0
    elif blackjackCheck(dealerHand):
        #print("Dealer wins, Blackjack")
        return -1
    elif blackjackCheck(playerHand):
        #print("Player wins 3/2 payout")
        return 1.5
    else:
        playerHand = mimic_the_dealer(playerHand, shuffledDeck)
        if handValue(playerHand) > 21:
            #print("Player bust")
            return -1
        #print("ONE", len(shuffledDeck))
        dealerPlayCountless(dealerHand, shuffledDeck)
        #print("TWO", len(shuffledDeck))
        #print(f"Player hand: {playerHand} \n Dealer hand: {dealerHand}")
        if handValue(dealerHand) > 21:
            #print("Dealer bust")
            return 1
        elif handValue(dealerHand) == handValue(playerHand):
            #print("PUSH")
            return 0
        elif handValue(dealerHand) > handValue(playerHand):
            #print("DEALER WIN")
            return -1
        else:
            #print("PLAYER WIN")
            return 1

def never_bust_blackjack(playerHand, dealerHand, shuffledDeck):
    if blackjackCheck(dealerHand) == True and blackjackCheck(playerHand) == True:
        #print("PUSH")
        return 0
    elif blackjackCheck(dealerHand):
        #print("Dealer wins, Blackjack")
        return -1
    elif blackjackCheck(playerHand):
        #print("Player wins 3/2 payout")
        return 1.5
    else:
        playerHand = never_bust(playerHand, shuffledDeck)
        if handValue(playerHand) > 21:
            #print("Player bust")
            return -1
        #print("ONE", len(shuffledDeck))
        dealerPlayCountless(dealerHand, shuffledDeck)
        #print("TWO", len(shuffledDeck))
        #print(f"Player hand: {playerHand} \n Dealer hand: {dealerHand}")
        if handValue(dealerHand) > 21:
            #print("Dealer bust")
            return 1
        elif handValue(dealerHand) == handValue(playerHand):
            #print("PUSH")
            return 0
        elif handValue(dealerHand) > handValue(playerHand):
            #print("DEALER WIN")
            return -1
        else:
            #print("PLAYER WIN")
            return 1
        
def bs_blackjack(playerHand, dealerHand, shuffledDeck, strategy):
    hasSplit = False
    #print(f"Player hand: {playerHand}")
    #print(f"Dealer card: {dealerHand[0]}")
    if blackjackCheck(dealerHand) == True and blackjackCheck(playerHand) == True:
        #print("PUSH")
        return 0
    elif blackjackCheck(dealerHand):
        #print("Dealer wins, Blackjack")
        return -1
    elif blackjackCheck(playerHand):
        #print("Player wins 3/2 payout")
        return 1.5
    else:
        playerHand, mult = basic_strategy(playerHand, dealerHand, shuffledDeck, hasSplit, strategy)
        if playerHand == "split":
            return mult
        if mult < 0:
            #print("Player bust")
            return -1
        dealerPlay(dealerHand, shuffledDeck, strategy)
        #print(calculateCount(playerHand, dealerHand))
        #print(f"Player hand: {playerHand} \n Dealer hand: {dealerHand}")
        if handValue(dealerHand) > 21:
            #print("Dealer bust")
            return 1*mult
        elif handValue(dealerHand) == handValue(playerHand):
            #print("PUSH")
            return 0
        elif handValue(dealerHand) > handValue(playerHand):
            #print("DEALER WIN")
            return -1*mult
        else:
            #print("PLAYER WIN")
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
                #print(f"Player Hand: {playerHand}")
                #print(f"Player hand value: {handValue(playerHand)}")
                if handValue(playerHand) > 21:
                    #print("Bust!")
                    return 1
            elif action.lower() == "stand":
                return 1
            elif action.lower() == "double":
                counter += 1
                playerHand.append(shuffledDeck.pop())
                #print(f"Player Hand: {playerHand}")
                if handValue(playerHand) > 21:
                    #print("Bust!")
                    return -2
                else:
                    return 2
        elif counter != 0:
            action = input("Hit or Stand? ")
            if action.lower() == "hit":
                playerHand.append(shuffledDeck.pop())
                #print(f"Player Hand: {playerHand}")
                #print(f"Player hand value: {handValue(playerHand)}")
                if handValue(playerHand) > 21:
                    #print("Bust!")
                    return -1
            elif action.lower() == "stand":
                return 1
            
def dealerPlay(dealerHand, shuffledDeck, strategy):
    global running_count
    #print(f"Dealers hand: {dealerHand}")
    while handValue(dealerHand) < 17:
        card = shuffledDeck.pop()
        
        dealerHand.append(card)
        update_count(card, strategy)
        #print(f"Dealers hand: {dealerHand}")

def dealerPlayCountless(dealerHand, shuffledDeck):
    while handValue(dealerHand) < 17:
        card = shuffledDeck.pop()
        dealerHand.append(card)

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
    #print("FIRST", playerHand)
    while handValue(playerHand) < 17:
        #print("MIMIC VALUE:", handValue(playerHand))
        playerHand.append(shuffledDeck.pop())
        #print(playerHand)
    return playerHand

def never_bust(playerHand, shuffledDeck):
    while handValue(playerHand) < 12:
        # hit on 11 and below
        #print(f"Never bust value: {handValue(playerHand)}")
        playerHand.append(shuffledDeck.pop())
        #print(playerHand)
    return playerHand
    
def basic_strategy(playerHand, dealerHand, shuffledDeck, hasSplit, strategy):
    global running_count
    count = 0
    if dealerHand[0][0] in ['J', 'Q', 'K']:
        dealerCard = 10
    elif dealerHand[0][0] == 'A':
        dealerCard = 11
    else:
        dealerCard = int(dealerHand[0][0])
    hardHands2 = {
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
        11: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        10: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        9: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        8: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        7: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        6: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        5: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        4: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        3: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        2: {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"}
      }
    
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

    softHands2 = {
        ('A', 10): {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        ('A', 9): {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        ('A', 8): {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Hit", 7: "Stand", 8: "Stand", 9: "Stand", 10: "Stand", 11: "Stand"},
        ('A', 7): {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Stand", 8: "Stand", 9: "Hit", 10: "Hit", 11: "Hit"},
        ('A', 6): {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        ('A', 5): {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        ('A', 4): {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        ('A', 3): {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        ('A', 2): {2: "Hit", 3: "Hit", 4: "Hit", 5: "Hit", 6: "Hit", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"}
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
        if hasSplit != True and playerHand[0][0] == playerHand[1][0]:   
            #print("PAIR")
            #print(playerHand)
            action = pairSplit.get((playerHand[0][0], playerHand[1][0])).get(dealerCard, "dk")
            #print(action)
            if action == "dk":
                #print(f"DK ERROR: {playerHand} and {dealerCard}")
                break
            if action == "Yes":
                #print("SPLITTT")
                counter += 1
                return "split", bs_split(playerHand, dealerHand, shuffledDeck, strategy)
            counter += 1
        if handType(playerHand) == "soft" and playerHand[0][0] == 'A' or playerHand[1][0] == 'A' and playerHand[0][0] != playerHand[1][0]:
            #print("SOFT")
            #print(handType(playerHand))
            temp = ""
            for i in range(len(playerHand)):
                #print(len(playerHand))
                if playerHand[i][0] == 'A':
                    #print("YEP")
                    temp = playerHand.pop(i)
                    #print(temp, playerHand)
                    break
            playerHand.insert(0, temp)
            action = softHands.get((playerHand[0][0], handValue(playerHand[1:])), {}).get(dealerCard, "dk")
            #action = softHands2.get((playerHand[0][0], handValue(playerHand[1:])), {}).get(dealerCard, "dk")
            # action = softHands.get(handValue(playerHand), {}).get(dealerCard, "dk")
            if action == "dk":
                #print(f"DK ERROR: {playerHand} and {dealerCard}")
                break
            #print(action)
            if action == "Hit":
                card = shuffledDeck.pop()
                playerHand.append(card)
                update_count(card, strategy)
                #print(f"AFTER HIT: {playerHand}")
            elif action == "Double":
                card = shuffledDeck.pop()

                playerHand.append(card)
                update_count(card, strategy)
                completed = True
                return playerHand, 2
            elif action == "Stand":
                completed = True
                #print("STAND")
                #print(playerHand, "STANDING")
                return playerHand, 1
        else:
            #print("HARD")
            action = hardHands.get(handValue(playerHand), {}).get(dealerCard, "dk")
            if action == "dk":
                #print(f"DK ERROR: {playerHand} and {dealerCard}")
                break
            #print(action)
            if action == "Hit":
                card = shuffledDeck.pop()
                playerHand.append(card)
                update_count(card, strategy)
                #print(f"AFTER HIT: {playerHand}")
            elif action == "Double":
                card = shuffledDeck.pop()
                playerHand.append(card)
                update_count(card, strategy)
                #print(f"AFTER DOUBLE: {playerHand}")
                completed = True
                return playerHand, 2
            elif action == "Stand":
                #print(f"AFTER STAND: {playerHand}")

                completed = True
                return playerHand, 1

def bs_split(playerHand, dealerHand, shuffledDeck, strategy):


    hasSplit = True
    # print("SPLIT AND CALLING FUNCTIONS")
    card1 = shuffledDeck.pop()
    card2 = shuffledDeck.pop()
    update_count(card1, strategy)
    update_count(card2, strategy)

    playerHand2 = [playerHand.pop()]
    playerHand.append(card1)
    playerHand2.append(card2)
    if blackjackCheck(playerHand):
        result1 = 1.5
    else:
        hand1, result1 = basic_strategy(playerHand, dealerHand, shuffledDeck, hasSplit, strategy)
    if blackjackCheck(playerHand2):
        result2 = 1.5
    else:
        hand2, result2 = basic_strategy(playerHand2, dealerHand, shuffledDeck, hasSplit, strategy)

    if result1 < 0 and result2 < 0:
        return result1 + result2
    dealerPlay(dealerHand, shuffledDeck, strategy)

    if result1 >= 0:
        if handValue(dealerHand) > 21:
            result1 = abs(result1)
        elif blackjackCheck(playerHand):
            pass  # Keep blackjack payout
        elif handValue(dealerHand) > handValue(playerHand):
            result1 = -1 * abs(result1)
        elif handValue(dealerHand) < handValue(playerHand):
            result1 = abs(result1)
        else:
            result1 = 0  # Push
    
    # Evaluate second hand result if it didn't bust
    if result2 >= 0:
        if handValue(dealerHand) > 21:
            result2 = abs(result2)
        elif blackjackCheck(playerHand2):
            pass  # Keep blackjack payout
        elif handValue(dealerHand) > handValue(playerHand2):
            result2 = -1 * abs(result2)
        elif handValue(dealerHand) < handValue(playerHand2):
            result2 = abs(result2)
        else:
            result2 = 0

    total = result1 + result2

    return total

    
def handType(hand):
    total = 0
    ace = 0
    for i in range(len(hand)):
        if hand[i][0] == "J" or hand[i][0] == "Q" or hand[i][0] == "K":
            total += 10
        elif hand[i][0] == "A":
            total += 11
            ace += 1
        else:
            total += int(hand[i][0])
    
    if total > 21 and ace > 0:
        return "hard"
    elif ace > 0:
        return "soft"
    else:
        return "hard"

def calculateCount(playerHand, dealerHand):
    count = 0
    for hands in [playerHand, dealerHand]:
        for card in hands:
            if card[0] in (2, 3, 4, 5, 6):
                count += 1
            elif card[0] in (7, 8, 9):
                count += 0
            else: 
                count -= 1
    return count

def averageRows(rows, decks):
    averageR = 0 
    avgRow = []
    y = []
    for j in range(len(rows[0])):
        for i in range(len(rows)):
            averageR += rows[i][j]  
        averageR /= len(rows)
        avgRow.append(averageR)
        y.append(j)
    plt.cla()
    plt.plot(y, avgRow, label = "Average Line")
    plt.ylim(-5, 5)
    plt.xlabel("Hand #")
    plt.ylabel("Result")
    plt.title("Average of 100 hands and 10000 games")
    plt.axhline(y = 0, color = 'r', linestyle = '-') 
    plt.savefig(f"wongtest{decks}")



def main_mimic():
    winnings = 0
    win = 0
    push = 0
    loss = 0 
    
    results = []
    num = 100#int(input("How many hands: "))
    rows = []
    for k in range(10000):
        pot = 0
        row = []
        y = []
        for i in range(num):
            deck = shuffleDeck(createDeck())
            #print(f"Hand number: {i}")
            if len(deck) <= 13:
                
                deck = shuffleDeck(createDeck())
            playerHand = []
            dealerHand = []
            for j in range(2):
                playerHand.append(deck.pop())
                dealerHand.append(deck.pop())
            result = mimic_blackjack(playerHand, dealerHand, deck)
            pot += result
            # row.append(result)
            row.append(pot)
            if result == 0:
                push += 1
            elif result > 0:
                winnings += result
                win += 1
            elif result < 0:
                loss += 1
            y.append(i)
        plt.plot(y, row)

        rows.append(row)
    plt.xlabel('Hand Number')
    plt.ylabel('Pot')
    plt.title('Pot Progression: Mimic the Dealer')

    plt.tight_layout()

    # Keep the final plot displayed
    # plt.show()
    # averageRows(rows)
    array = []
    for row in rows:
        array.append(sum(row)/100)
    avgprofitperhand = (sum(array)/10000)
    print(f"Average profit per hand: {avgprofitperhand}")
    # print(f"Win rate: {win/10000} \n Push rate: {push/10000} \n Loss rate: {loss/10000}")
    # print(f"Avg. Profit per Hand: {(winnings-1000000)/1000000}")

    return win/10000, push/1000000, loss/10000, (winnings-1000000)/1000000


def main_never_bust():
    winnings = 0
    win = 0
    push = 0
    loss = 0 
    rows =[]
    deck = shuffleDeck(createDeck())
    results = []
    num = 100#int(input("How many hands: "))
    for k in range(10000):
        pot = 0
        row = []
        y = []
        for i in range(num):
            deck = shuffleDeck(createDeck())

            #print(f"Hand number: {i}")
            if len(deck) <= 13:
                #print("Reshuffling deck")
                deck = shuffleDeck(createDeck())
            playerHand = []
            dealerHand = []
            for j in range(2):
                playerHand.append(deck.pop())
                dealerHand.append(deck.pop())
            result = never_bust_blackjack(playerHand, dealerHand, deck)
            
            pot += result
            if result == 0:
                push += 1
            elif result > 0:
                winnings += result
                win += 1
            elif result < 0:
                loss += 1
            row.append(pot)
            y.append(i)
        plt.plot(y, row)
        rows.append(row)
    plt.xlabel('Hand Number')
    plt.ylabel('Pot')
    plt.title('Pot Progression: Mimic the Dealer')

    plt.tight_layout()
    # plt.show()
    # averageRows(rows)
    array = []
    for row in rows:
        array.append(sum(row)/100)
    avgprofitperhand = (sum(array)/10000)
    print(f"Average profit per hand: {avgprofitperhand}")

    # print(f"Win rate: {win/10000} \n Push rate: {push/10000} \n Loss rate: {loss/10000}")
    # print(f"Avg. Profit per Hand: {(winnings-1000000)/1000000}")

    #print(results)
    return win/10000, push/1000000, loss/10000, (winnings-1000000)/1000000


def get_bet(running_count, bet_type, deck):
    decks_remaining = len(deck)/52

    true_count = running_count/decks_remaining if decks_remaining > 0 else 0
    if bet_type == 0:
        return 1, true_count
    if bet_type == 1:
        if true_count <= 0:
            return 1, true_count
        elif true_count <= 1:
            return 2, true_count
        elif true_count <=2:
            return 4, true_count
        elif true_count <= 3:
            return 6, true_count
        else:
            return 8, true_count
    elif bet_type == 2:
        if true_count <= 0:
            return 1, true_count
        elif true_count <= 1:
            return 3, true_count
        elif true_count <=2:
            return 6, true_count
        elif true_count <= 3:
            return 9, true_count
        else:
            return 12, true_count
    elif bet_type == 3:
        if true_count <= 0:
            return 1, true_count
        elif true_count <= 1:
            return 4, true_count
        elif true_count <=2:
            return 8, true_count
        elif true_count <= 3:
            return 12, true_count
        else:
            return 16, true_count
    
def create_multiple_decks(numDeck):
    deck_all = []
    for i in range(numDeck):
        deck_all.append(createDeck())

    flat_list = [item for sublist in deck_all for item in sublist]
    return flat_list

    
    deck2 = random.shuffle(flat_list)
def basic_strategy_main(bet_type, strategy, decks):
    global running_count
    truecountseen = []
    # decks = 6
    money = 0
    day_change = []
    deck_all = []
    results = []
    bankrolls = []
    hand_results = []
    rows = []
    potss = []
    # results = []
    winnings = 0
    win = 0
    push = 0
    loss = 0 
    ruin_count = 0
    penetration = 0.75
    cut_card = decks*52*penetration
    num = 100#int(input("How many hands: "))
    avgprofitperhand = 0
    for k in range(10000):
        pots = []
        ruined = False
        #money -= 100

        #print(k)
        hasSplit = False
        pot = 0
        row = []
        y = []
        
        # deck = shuffleDeck(createDeck())
        deck = create_multiple_decks(decks)
        random.shuffle(deck)
        running_count = 0
        for i in range(num):
            
            #print(f"Hand number: {i}")
            if len(deck) <= cut_card:
                #print("Reshuffling deck")
                # deck = shuffleDeck(createDeck())
                deck = create_multiple_decks(decks)
                random.shuffle(deck)

                running_count = 0
            bet, true_count = get_bet(running_count, bet_type, deck)
            truecountseen.append([bet, true_count])
            playerHand = []
            dealerHand = []
            for j in range(2):
                card = deck.pop()
                playerHand.append(card)
                update_count(card, strategy)  

                card = deck.pop()
                dealerHand.append(card)
                update_count(card, strategy)  

            #print(f"CARDS LEFT: {len(deck)}")
            result = bs_blackjack(playerHand, dealerHand, deck, strategy) * bet
            # bankroll += result
            pot += result
            pots.append(pot)
            row.append(result)
            
            money += result
            if result == 0:
                push += 1
            elif result > 0:
                winnings += result
                win += 1
            elif result < 0:
                loss += 1
            y.append(i)
        # plt.plot(y, pots)
                
        # if ruined:
        #     ruin_count += 1
        day_change.append(money)

        results.append(pot)
        # bankrolls.append(bankroll)
        #print("Game DONE")
        #print(row)
        potss.append(pots)
        rows.append(row)
        # print(k, row)
    # plt.xlabel('Hand Number')
    # plt.ylabel('Pot')
    # plt.title('Pot Progression for Each 100-Hand Game (10,000 Games)')
    # plt.grid(True)
    # plt.tight_layout()

    # Keep the final plot displayed
    # plt.show()
    avg_results = [r/100 for r in results]

    mean = sum(avg_results)/len(avg_results)

    squared_difference = [(r-mean)**2 for r in avg_results]
    standard_dev = (sum(squared_difference)/len(avg_results))**0.5
    # averageRows(potss, bet_type)
    mean = sum(results)/10000
    array = []
    for row in rows:
        array.append(sum(row)/100)
    avgprofitperhand = (sum(array)/10000)
    print(f"Average profit per hand: {avgprofitperhand}")
    #print(mean)
    #print(min(results))
    #print(max(results))

    print(f"Standard deviation:{standard_dev}")
    #print(f"Amount ruined: {ruin_count}")
    #print(f"Final money: {money}")
    
    # plt.boxplot(results, vert=False, patch_artist=False)
    # plt.show()

    # plt.hist(results, bins=50, edgecolor='black')
    # plt.xlabel('Profit per Game')
    # plt.ylabel('Frequency')
    # plt.title('Distribution of Blackjack Game Results')
    # plt.show()

    # plt.plot(range(10000), bankrolls)
    # plt.xlabel("Game number")
    # plt.ylabel("Bankroll")
    # plt.title("Bankroll after each Game")
    # plt.show()
        

    #     plt.plot(y, row, label = f"Line {k}")

    # plt.xlabel("Hand #")
    # plt.ylabel("Result")
    # plt.title("1000 Games of 100 hands")
    # plt.axhline(y = 0, color = 'r', linestyle = '-') 
    # plt.show()
    # averageRows(rows)
    # return hand_results
    print(max(truecountseen))
    bet_values = [bet for bet, _ in truecountseen]
    true_count_values = [true_count for _, true_count in truecountseen]
    # averageRows(rows)

    # Plotting
    # plt.figure(figsize=(10, 6))
    # plt.scatter(bet_values, true_count_values, color='blue', alpha=0.5)
    # plt.title('True Count vs Bet Value')
    # plt.xlabel('Bet Value')
    # plt.ylabel('True Count')
    # plt.grid(True)
    # plt.show()
    
    # print(f"Win rate: {win/10000} \n Push rate: {push/10000} \n Loss rate: {loss/10000}")
    # print(f"Avg. Profit per Hand: {(winnings-1000000)/1000000}")
    print(win / 10000, push / 10000, loss / 10000)
    print(truecountseen[0])
    return( win / 1000000, push / 1000000, loss / 1000000, avgprofitperhand, standard_dev, day_change, truecountseen)

def plot_avgprofit_comparison(avgprofit_list, strategies):
    betting_labels = ["Betting 1", "Betting 2", "Betting 3", "Betting 4"]
    num_bets = len(betting_labels)
    num_strats = len(strategies)
    bar_width = 0.2

    # X-axis positions for each group of bars
    x = np.arange(num_bets)

    # Create a bar for each strategy
    plt.figure(figsize=(12, 6))
    for i, (avgprofits, strategy) in enumerate(zip(avgprofit_list, strategies)):
        offset = (i - (num_strats - 1)/2) * bar_width  # centers the bars
        plt.bar(x + offset, avgprofits, width=bar_width, label=strategy)

    plt.xlabel("Betting Strategies")
    plt.ylabel("Average Profit")
    plt.title("Average Profit Comparison Across Card Counting and Betting Strategies")
    plt.xticks(x, betting_labels)
    plt.legend(title="Card Counting Strategy")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def loop_hist(decks):
    betting_labels = ["Betting 1", "Betting 2", "Betting 3"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # Create 1 row, 3 columns of subplots

    for subplot_index, strategy_index in enumerate(range(1, 4)):
        _, _, _, _, _, _, truecountseen = basic_strategy_main(strategy_index, "hilo", decks)
        bets = [pair[0] for pair in truecountseen]
        axes[subplot_index].hist(bets, bins=20, edgecolor='black', width=0.8)
        axes[subplot_index].set_title(betting_labels[subplot_index])
        axes[subplot_index].set_xlabel("Bet Value")
        axes[subplot_index].set_ylabel("Frequency")
        axes[subplot_index].set_xticks([1, 2, 3, 5, 6, 8, 12, 16])
        axes[subplot_index].set_ylim(0, 650000)

    plt.tight_layout()
    plt.savefig(f"betting_histograms{decks}.png")

    

    
def loop_basic():
    
    strategies = ["hilo", "omega", "wong"]
    betting_labels = ["Betting 1", "Betting 2", "Betting 3"]
    bar_width = 0.25
    
    # Set up the figure with appropriate size
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    titles = ["Win Rates", "Push Rates", "Loss Rates"]

    win_rates = []
    push_rates = []
    loss_rates = []
    avgprofit_list = []
    rateruin_list = []
    day_changes_all = []


    for strategy in strategies:
        wins = []
        pushes = []
        losses = []
        avgprofit = []
        rateruin = []
        day_changes = []
        for i in range(0, 4, 1):
            print(i)
            basic_wr, basic_pr, basic_lr, basic_avgprofit, basic_ruin, day_change = basic_strategy_main(i, strategy)
            #print(basic_wr, basic_pr, basic_lr, basic_avgprofit)
            avgprofit.append(basic_avgprofit)
            rateruin.append(basic_ruin)
            wins.append(basic_wr)
            pushes.append(basic_pr)
            losses.append(basic_lr)
            day_changes.append(day_change)
    
        win_rates.append(wins)
        push_rates.append(pushes)
        loss_rates.append(losses)
        avgprofit_list.append(avgprofit)
        rateruin_list.append(rateruin)
        day_changes_all.append(day_changes)


        formatted = [f"{x:.6f}" for x in rateruin]
        print(f"Strategy: {strategy} \n Rate of ruin: {formatted}")

    # Create a more informative visualization
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Stacked bar chart showing win/push/loss composition for each strategy-betting combo
    ax = axs[0, 0]
    
    
    labels = []
    for s in strategies:
        for b in betting_labels:
            labels.append(f"{s}\n{b}")
    
    bottoms = np.zeros(len(strategies) * len(betting_labels))
    win_data = []
    push_data = []
    loss_data = []
    
    for i, strat in enumerate(strategies):
        for j, bet in enumerate(betting_labels):
            idx = i * len(betting_labels) + j
            win_data.append(win_rates[i][j])
            push_data.append(push_rates[i][j])
            loss_data.append(loss_rates[i][j])
            day_change = day_changes_all[i][j]
            days = np.arange(len(day_change))
            ax.plot(days, day_change, label=f"{strat}-{bet}")
    
    plot_avgprofit_comparison(avgprofit_list, strategies)
    
    ax.set_title('Daily Money Changes Over Time')
    ax.set_xlabel('Day')
    ax.set_ylabel('Money Won/Lost')
    ax.axhline(y=0, color='r', linestyle='-', alpha=0.3)  # Zero line
    ax.legend()
    
    # 2. Heatmap of win rates
    ax = axs[0, 1]
    win_array = np.array(win_rates)
    im = ax.imshow(win_array, cmap='YlGn')
    
    # Add labels
    ax.set_xticks(np.arange(len(betting_labels)))
    ax.set_yticks(np.arange(len(strategies)))
    ax.set_xticklabels(betting_labels)
    ax.set_yticklabels(strategies)
    ax.set_title('Win Rate Heatmap')
    
    # Add colorbar
    ax.figure.colorbar(im, ax=ax)
    
    # 3. Average profit comparison
    ax = axs[1, 0]
    x = np.arange(len(betting_labels))
    width = 0.25
    
    
    # 4. Ruin rate comparison
    ax = axs[1, 1]
    x = np.arange(len(betting_labels))
    width = 0.25
    
    for i, strategy in enumerate(strategies):
        ax.bar(x + (i-1)*width, rateruin_list[i], width, label=strategy)
    
    ax.set_title('Ruin Rate by Strategy and Betting Method')
    ax.set_xticks(x)
    ax.set_xticklabels(betting_labels)
    ax.set_ylabel('Ruin Rate')
    ax.legend()
    
    plt.tight_layout()
    plt.show()
    
    
    # Find and print the best and worst combinations
    win_array = np.array(win_rates)
    loss_array = np.array(loss_rates)
    profit_array = np.array(avgprofit_list)
    ruin_array = np.array(rateruin_list)
    
    best_win_idx = np.unravel_index(win_array.argmax(), win_array.shape)
    worst_loss_idx = np.unravel_index(loss_array.argmax(), loss_array.shape)
    best_profit_idx = np.unravel_index(profit_array.argmax(), profit_array.shape)
    lowest_ruin_idx = np.unravel_index(ruin_array.argmin(), ruin_array.shape)
    
    print(f"Best win rate: {strategies[best_win_idx[0]]} with {betting_labels[best_win_idx[1]]} - {win_array[best_win_idx]:.5f}")
    print(f"Worst loss rate: {strategies[worst_loss_idx[0]]} with {betting_labels[worst_loss_idx[1]]} - {loss_array[worst_loss_idx]:.5f}")
    print(f"Best profit: {strategies[best_profit_idx[0]]} with {betting_labels[best_profit_idx[1]]} - {profit_array[best_profit_idx]:.5f}")
    print(f"Lowest ruin rate: {strategies[lowest_ruin_idx[0]]} with {betting_labels[lowest_ruin_idx[1]]} - {ruin_array[lowest_ruin_idx]:.5f}")

    plot_avgprofit_comparison(avgprofit_list, strategies)
    


def loop_strategy():
    mimic_wr, mimic_pr, mimic_lr, mimic_avgprofit = main_mimic()
    neverb_wr, neverb_pr, neverb_lr, neverb_avgprofit = main_never_bust()
    basic_wr, basic_pr, basic_lr, basic_avgprofit, temp, temp2, _ = basic_strategy_main(0, "hilo", 1)
    print(f"mimic pr: {mimic_pr}\nneverb pr: {neverb_pr}\nbasic pr: {basic_pr}")
    strategies = ["Mimic", "Never Bust", "Basic Strategy"]
    metrics = ["Win rate", "Loss rate"]

    data = np.array([
        [mimic_wr, mimic_lr],
        [neverb_wr,  neverb_lr],
        [basic_wr*100,  basic_lr*100]
    ])

    df = pd.DataFrame(data, index=strategies, columns=metrics)
    plt.figure(figsize=(9, 6))
    sns.heatmap(df, annot=True, cmap="YlGnBu", fmt=".3f", linewidths=.5)
    
    plt.title('Blackjack Strategy Comparison', fontsize=16)
    plt.tight_layout()
    plt.show()

    basic_data = {"Win rate": [basic_wr],
                  "Push rate": [basic_pr],
                  "Loss rate": [basic_lr],
                  "Profit p hand": [basic_avgprofit]}
    # data = {
    #     "Strategy": ["Mimic the Dealer", "Never Bust", "Basic Strategy"],
    #     "Win rate": [mimic_wr, neverb_wr, basic_wr],
    #     "Push rate": [mimic_pr, neverb_pr, basic_pr],
    #     "Loss rate": [mimic_lr, neverb_lr, basic_lr],
    #     "Avg Profit per Hand": [mimic_avgprofit, neverb_avgprofit, basic_avgprofit]
    # }
    # df = pd.DataFrame(data)
    BSdf = pd.DataFrame(basic_data)
    print(BSdf)

def plotting():
    deck_counts = [1, 2, 4, 6]

    hilo = [0.015229, -0.0002, -0.0043555, -0.0058785]
    omega = [0.0163035, 0.002053, -0.00625, -0.007078]
    wong = [0.0140545, -0.001257, -0.00671, -0.006901]
    plt.figure(figsize=(10, 6))

    plt.plot(deck_counts, hilo, marker="o", label= "Hi-Lo")
    plt.plot(deck_counts, omega, marker="s", label= "Omega II")
    plt.plot(deck_counts, wong, marker="^", label= "Wong Halves")
    plt.xlabel("Number of Decks")
    plt.ylabel("Average Profit")
    plt.title("Performance of Card Count Strategies by Deck Count")
    plt.legend()
    plt.tight_layout()
    plt.show()



choice = input("Normal, Mimic The Dealer, Never Bust or Basic Strategy? ")
if choice.lower() == "mimic":
    main_mimic()
elif choice.lower() == "never":
    main_never_bust()
elif choice.lower() == "basic":
    avgprofits = []
    standarddevs = []
    
    for j in ["hilo", "omega", "wong"]:
        avgp = []
        std = []
        for i in [1, 2, 3]:
            hand_results = basic_strategy_main(i, j, 6)
            avgp.append(hand_results[-4])
            std.append(hand_results[-3])
        avgprofits.append(avgp)
        standarddevs.append(std)
    print(avgprofits)
    print(standarddevs)

elif choice.lower() == "normal":
    blackjack()
elif choice.lower() == "loop":
    loop_strategy()
elif choice.lower() == "loopb":
    loop_basic()
elif choice.lower() == "hist":
    loop_hist(1)
elif choice.lower() == "plot":
    plotting()