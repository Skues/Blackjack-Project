----------- READ ME----------

main.py will run when all necessary libraries are imported, such as matplotpib, pandas, seaborn and numpy.

When running the main.py file you will get asked what strategy you want to use. Normal will play a basic version of Blackjack that was implemented at the start of the project.

However, other inputs include "Mimic", "Never", "Basic" which will run the 10,000 game simulation on which strategy you input.

Additionally, if you want to use card counting, there is a line: basic_strategy_main(0, "hilo", 6, True, True, "Null")
Where the first parameter is the betting method (0 = Flat betting and 1, 2, 3 are more aggressive betting spreads.
The second parameter is the card counting method you wish to use which include "hilo", "omega" and "wong".
The third parameter is the amount of decks you wish to use which has no limit.
The forth and fifth parameters are used for the Basic Strategy variations and allow splitting and doubling depending on the bool variable.
The final variable is not necessary to change.
---------------------------------