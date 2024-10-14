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
            var = pot - bet
            return bet

def blackjack():
    shuffledDeck = shuffleDeck(createDeck())
    bet = getBet()
    playerHand = [shuffledDeck.pop(), shuffledDeck.pop()]
    dealerHand = [shuffledDeck.pop(), shuffledDeck.pop()]
    print(f"Player Hand: {playerHand}")
    print(f"DealerHand: {dealerHand[0]}")
    # Check if dealers hand gives them blackjack
    gameOver = False
    while gameOver == False:
        action = input("What would you like to do? ")
        if action.upper() == "H":
            playerHand.append(shuffledDeck.pop())
            print(f"Player Hand: {playerHand}")
            print(f"Player hand value: {handValue(playerHand)}")
            # check if player hand value is greater than 21
        elif action.upper() == "S":
            print("dealers turn")
            #check if dealers hand is less than 17 then hit till 17 or above
            dealerHand.append(shuffledDeck.pop())
            print(f"DealerHand: {dealerHand}")

def handValue(hand):
    total = 0
    for i in range (len(hand)):
        if hand[i][0] == "J" or hand[i][0] == "Q" or hand[i][0] == "K":
            total += 10
            print(total)
        elif hand[i][0] == "A":
            total += 11
            print(total)
        else:
            total += int(hand[i][0])
            print(total)
    return total


blackjack()



