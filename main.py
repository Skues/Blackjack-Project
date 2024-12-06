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

def blackjack():
    global pot
    shuffledDeck = shuffleDeck(createDeck())
    play = "Y"
    while play.upper() == "Y": 
        bet = getBet()
        playerHand = []
        dealerHand = []
        # playerHand = [shuffledDeck.pop(), shuffledDeck.pop()]
        # dealerHand = [shuffledDeck.pop(), shuffledDeck.pop()]
        for i in range(2):
            playerHand.append(shuffledDeck.pop())
            dealerHand.append(shuffledDeck.pop())
        playerHand = [['4', 'of', 'Club'], ['4', 'of', 'Spade']]
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
                    
                    if handValue(dealerHand) > 21:
                        print("Dealer bust")
                        pot += bet*result
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
        #     gameOver = False
        #     while gameOver == False:
        #         if playerHand[0][0] == playerHand[1][0]:
        #             action = input("Hit, Stand, Split or Double? ")
        #         else:
        #             action = input("Hit, Stand or Double")
        #         if action.lower() == "hit":
        #             playerHand.append(shuffledDeck.pop())
        #             print(f"Player Hand: {playerHand}")
        #             print(f"Player hand value: {handValue(playerHand)}")
        #             if handValue(playerHand) > 21:
        #                 print("Bust!")
        #                 pot -= bet
        #                 gameOver = True
        #         elif action.lower() == "stand":
        #             print("dealers turn")
        #             print(f"DealerHand: {dealerHand}")
        #             while handValue(dealerHand) < 17:
        #                 print("Dealer takes another card")
        #                 dealerHand.append(shuffledDeck.pop())
        #                 print(f"DealerHand: {dealerHand}")
        #             if handValue(dealerHand) > 21:
        #                 print("Dealer bust")
        #                 pot += bet
        #                 gameOver = True
        #             elif handValue(dealerHand) == handValue(playerHand):
        #                 print("PUSH")
        #                 gameOver = True
        #             elif handValue(dealerHand) > handValue(playerHand):
        #                 print("DEALER WIN")
        #                 pot -= bet
        #                 gameOver = True
        #             else:
        #                 print("PLAYER WIN")
        #                 pot += bet
        #                 gameOver = True
        #         elif action.lower() == "double":
        #             playerHand.append(shuffledDeck.pop())
        #             print(f"Player Hand: {playerHand}")
        #             if handValue(playerHand) > 21:
        #                 print("Bust!")
        #                 pot -= bet*2
        #                 gameOver = True
        #             else:
        #                 print("dealers turn")
        #                 print(f"DealerHand: {dealerHand}")
        #                 while handValue(dealerHand) < 17:
        #                     print("Dealer takes another card")
        #                     dealerHand.append(shuffledDeck.pop())
        #                     print(f"DealerHand: {dealerHand}")
        #                 if handValue(dealerHand) > 21:
        #                     print("Dealer bust")
        #                     pot += bet*2
        #                     gameOver = True
        #                 elif handValue(dealerHand) == handValue(playerHand):
        #                     print("PUSH")
        #                     gameOver = True
        #                 elif handValue(dealerHand) > handValue(playerHand):
        #                     print("DEALER WIN")
        #                     pot -= bet*2
        #                     gameOver = True
        #                 else:
        #                     print("PLAYER WIN")
        #                     pot += bet*2
        #                     gameOver = True
        #         elif action.lower() == "split":
        #             print("SPLIT")
        #             playerHand2 = [playerHand.pop()]
        #             playerHand.append(shuffledDeck.pop())
        #             print(f"Player Hand: {playerHand}")
        #             playerHand2.append(shuffledDeck.pop())
        #             print(f"Split Player Hand: {playerHand2}")
        #             # create new player hand variable that gets second card appended to it
        #             # deal cards to split hands and play the game like normal for both hands
        #     print(f"Pot after hand: {pot}")
        # if pot > 0:
        #     play = input("Do you want to play? Y/N ")
        # else:
        #     print("Ran out of money")
        #     play = "N"
            

def handValue(hand):
    total = 0
    for i in range (len(hand)):
        if hand[i][0] == "J" or hand[i][0] == "Q" or hand[i][0] == "K":
            total += 10
        elif hand[i][0] == "A":
            if total+11 > 21:
                total += 1
            else:
                total += 11
        else:
            for j in range(len(hand)):
                if hand[j][0] == "A" and total+int(hand[i][0]) > 21:
                    total += int(hand[i][0])-10
            total += int(hand[i][0])
    print(total)
    return total

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
                    return -1
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


def runHand(playerHand, dealerHand, shuffledDeck):
    print(f"player hand = {playerHand}, dealer hand = {dealerHand}")
    if blackjackCheck(dealerHand) == True and blackjackCheck(playerHand) == True:
            print("PUSH")
            return 0
    elif blackjackCheck(dealerHand):
        print("Dealer wins")
        return -1
    elif blackjackCheck(playerHand):
        print("Player wins 3/2 payout")
        return 1.5
    else:
        gameOver = False
        while gameOver == False:
            if playerHand[0][0] == playerHand[1][0]:
                action = input("Hit, Stand, Split or Double? ")
            else:
                action = input("Hit, Stand or Double? ")
            if action.lower() == "hit":
                playerHand.append(shuffledDeck.pop())
                print(f"Player Hand: {playerHand}")
                print(f"Player hand value: {handValue(playerHand)}")
                if handValue(playerHand) > 21:
                    print("Bust!")
                    return -1
            elif action.lower() == "stand":
                print("dealers turn")
                print(f"DealerHand: {dealerHand}")
                while handValue(dealerHand) < 17:
                    print("Dealer takes another card")
                    dealerHand.append(shuffledDeck.pop())
                    print(f"DealerHand: {dealerHand}")
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
            elif action.lower() == "double":
                playerHand.append(shuffledDeck.pop())
                print(f"Player Hand: {playerHand}")
                if handValue(playerHand) > 21:
                    print("Bust!")
                    return -2
                else:
                    print("dealers turn")
                    print(f"DealerHand: {dealerHand}")
                    while handValue(dealerHand) < 17:
                        print("Dealer takes another card")
                        dealerHand.append(shuffledDeck.pop())
                        print(f"DealerHand: {dealerHand}")
                    if handValue(dealerHand) > 21:
                        print("Dealer bust")
                        return 2
                    elif handValue(dealerHand) == handValue(playerHand):
                        print("PUSH")
                        return 0
                    elif handValue(dealerHand) > handValue(playerHand):
                        print("DEALER WIN")
                        return -2
                    else:
                        print("PLAYER WIN")
                        return 2
            elif action.lower() == "split":
                    return splitFunction(playerHand, shuffledDeck, dealerHand)

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

blackjack()



