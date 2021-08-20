# Blackjack Simulator

This is a small Python application that is designed to simulate the popular Blackjack card game. For the rules and a concise introduction to the game, see https://bicyclecards.com/how-to-play/blackjack/.

### Emulates real play

Blackjack Simulator allows the user to double down, split pairs, and ask for insurance. Despite it being developed as a learning exercise, the house's rules have been designed to resemble those of actual casinos as much as possible. 

### Multiplayer mode

The game has been adapted to include up to 8 players in the table. This limit, however, is based upon physical limitations in actual casino tables; it can easily be modified to include as many players as desired.

### Performance rating

At the end of the game, a ranking is displayed to show how much each player has won/lost based on their starting balance.

### Potential updates
_Note: this list is revised after every commit_

Besides from improving the code's readability and general maintenance, it might be interesting to implement some (or all) of the following:

* Store the ranking's results at the end of every execution in a local database and use that to display an 'all-time' ranking based on players' performance.
* Develop an user interface (GUI) to make the program more user-friendly
* Allow for multiplayer mode in multiple terminals
