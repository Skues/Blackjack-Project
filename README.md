# Third Year Final Project - Blackjack Card Counting 🃏

This project was my chosen dissertation and, along with the code, has a [40 page report](https://github.com/Skues/Blackjack-Project/blob/main/Blackjack%20Report.pdf)
on my findings and evaluation. The aim of this project was to create a Blackjack simulation that investigates
the effectiveness of various strategies within games of Blackjack.
Each strategy was simulated over 10,000 games to generate reliable long-term results.

## Blackjack Simulation 🤖
The simulation took inspiration of real-life rules of Blackjack to mimic a casino experience.
This was done through:
- Creating and randomly shuffling a standard 52-card deck
- Dealing two cards each to the player and the dealer
- Allowing the player to hit, stand, double or split
- Winning, losing and pushing all integrated
- Tracks the player balance after each hand and game

## Gameplay Strategies 🕹
After the initial simulation environment was created, gameplay strategies were then implemented.
These consisted of:
- **Mimic the Dealer** - Strategy were the player follows the dealers rules (stand on 17)
- **Never Bust** - Conservative strategy aimed at not having a hand value of over 21 (bust) so the player will stand on most high values
- **Basic Strategy** - Statistically optimal strategy which depicts the best option for the player against every possible hand
[Basic Strategy table](https://www.blackjackapprenticeship.com/wp-content/uploads/2018/10/mini-blackjack-strategy-chart.png)

## Card Counting Strategies 🧠
Having the most optimal gameplay strategy will reduce the house's edge to 0.5% over the long-term but to get profitablity, more advanced strategies were implemented. 
Card counting is a technique to track the proportion of high-to-low cards. If the player knows when there are more high cards in the deck, they will be in a more advantageous position. More high cards will create more Blackjack situations for the player and cause the dealer to bust more while low cards are disadvantageous.
Three card counting strategies were implemeted:
1. Hi-Lo - Basic, simple and popular card counting strategy
2. Omega II - More advanced card counting strategy which has a higher range of count values compared to Hi-Lo
3. Wong Halves - Most advanced strategy out of the three as it involves halves in the count which is hard to track.

### Further Information
More information, graphs and results are all in my paper which is on this repository.

