# HomeGame
bare-bones poker game built around pokerlib... leave behind the inconvenience of heavy chips, card decks and tedious counting and dealing exercises for a simple game that gets people together.

plans:
- build
- host on AWS EC2
- front-end
- stats for hand rankings and strategies

FIXES NEEDED:
- ability to straddle and change the order of the game
- minimum capacity of 3 players to start a round

FIXED:
- entering a bet of '' does not work
- folding and raising does not have the correct order after.
- starting a second round doesnt work when players have folded in a previous round: need to reset order
- can still bet even if player will incur negative balance
