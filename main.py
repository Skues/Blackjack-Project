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
        else:
            return bet

def blackjack():
    global pot
    shuffledDeck = shuffleDeck(createDeck())
    play = "Y"
    while play.upper() == "Y": 
        bet = getBet()
        playerHand = [shuffledDeck.pop(), shuffledDeck.pop()]
        dealerHand = [shuffledDeck.pop(), shuffledDeck.pop()]
        print(f"Player Hand: {playerHand}")
        print(f"Dealer Hand: {dealerHand}")
        # print(f"Dealer Hand: {dealerHand[0]}, HIDDEN CARD")
        if blackjackCheck(dealerHand) == True and blackjackCheck(playerHand) == True:
            print("PUSH")
        elif blackjackCheck(dealerHand) == True:
            print("Dealer wins")
            pot -= bet
        elif blackjackCheck(playerHand) == True:
            print("Player wins 3/2 payout")
            pot += bet*1.5
        else:
            gameOver = False
            while gameOver == False:
                action = input("What would you like to do? ")
                if action.upper() == "H":
                    playerHand.append(shuffledDeck.pop())
                    print(f"Player Hand: {playerHand}")
                    print(f"Player hand value: {handValue(playerHand)}")
                    if handValue(playerHand) > 21:
                        print("Bust!")
                        pot -= bet
                        gameOver = True
                elif action.upper() == "S":
                    print("dealers turn")
                    print(f"DealerHand: {dealerHand}")
                    while handValue(dealerHand) < 17:
                        print("Dealer takes another card")
                        dealerHand.append(shuffledDeck.pop())
                        print(f"DealerHand: {dealerHand}")
                    if handValue(dealerHand) > 21:
                        print("Dealer bust")
                        pot += bet
                        gameOver = True
                    elif handValue(dealerHand) == handValue(playerHand):
                        print("PUSH")
                        gameOver = True
                    elif handValue(dealerHand) > handValue(playerHand):
                        print("DEALER WIN")
                        pot -= bet
                        gameOver = True
                    else:
                        print("PLAYER WIN")
                        pot += bet
                        gameOver = True
            print(f"Pot after hand: {pot}")
        play = input("Do you want to play? Y/N ")
    print(f"Pot after whole game: {pot}")
            

def handValue(hand):
    total = 0
    for i in range (len(hand)):
        if hand[i][0] == "J" or hand[i][0] == "Q" or hand[i][0] == "K":
            total += 10
        elif hand[i][0] == "A":
            total += 11
        else:
            total += int(hand[i][0])
    return total

def blackjackCheck(hand):
    if hand[0][0] == "J" or hand[0][0] == "Q" or hand[0][0] == "K":
        if hand[1][0] == "A":
            return True
    elif hand[0][0] == "A":
        if hand[0][0] == "J" or hand[0][0] == "Q" or hand[0][0] == "K":
            return True
    else:
        return False


blackjack()



