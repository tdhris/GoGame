GoGame
======
## What is Go?

Go is one of the oldest board games in the world. It's played by two people placing black and white stones on the empty intersections of the board (called goban in Japanese). The goal of the game is to conquer a larger total area of the board than your opponent.

## Rules of Go

The game will enforce the Japanese rules:
* When a player passes his move and his opponent passes in succession, the game stops.
* During a game, a player may end the game by admitting defeat (resigning)
* A group of one or more stones belonging to one player exists on the board as long as it has a horizontally or vertically adjacent empty point, called a "liberty." No group of stones without a liberty can exist on the board.
* If, due to a player's move, one or more of his opponent's stones cannot exist on the board according to the preceding article, the player must remove all these opposing stones, which are called "prisoners." The captured stones are removed from the board.
* Empty points surrounded by the live stones of just one player are called "eye points." Other empty points are called "dame." Stones which are alive but possess dame are said to be in "seki." Eye points surrounded by stones that are alive but not in seki are called "territory," each eye point counting as one point of territory.
* A player's score is the sum of the number of empty points their stones surround (not counting "seki" points) and the number of their opponent's stones they've captured

Also, to allow players of different skills to compete fairly, handicaps and komi are used.

* Handicaps are given by allowing the weaker player to place a certain number of stones (usually the number is equal to the difference in the players' ranks) on the board before allowing the opponent to play. 
* Komi (Komidashi) are points added to the score of the player with the white stones as compensation for playing second. Black's first move advantage is generally considered to equal somewhere between 5 and 7 points by the end of the game. Standard komi is 6.5 points under the Japanese and Korean rules

## Game Functionality

* The game will enforce the rules of Go, count territory (according to the Japanese rules) and announce the winner at the end of the game. It has to: stop when a player resigns or both of the players pass in succession, recognize when a stone/group of stones is captured and remove it from the board, recognize seki points and territory points, keep score;
* The player will be able to change game options such as komi (set at 6.5 by default) and handicap (0 by default)
* GUI
* Sound (when a player places a stone on the board)

## Milestone 2

I'd like to have written most of the game logic by then.
