"""
An Introduction to Interactive Programming in Python (by Coursera and Rice
University). Week 1 programming assignment: Rock-paper-scissors-lizard-Spock.
Link to the code in CodeSculptor: http://www.codeskulptor.org/#user42_fPE95VowZK_0.py
"""

import random

def name_to_number(name):
    '''Converts names used in the game to numbers.'''

    if name == 'rock':
        return 0
    if name == 'Spock':
        return 1
    if name == 'paper':
        return 2
    if name == 'lizard':
        return 3
    if name == 'scissors':
        return 4
    else:
        print "Your's input is bizzare. I'll choose 'rock' instead."
        return 0

def number_to_name(number):
    '''Converts numbers to names used in the game.'''

    if number == 0:
        return 'rock'
    if number == 1:
        return 'Spock'
    if number == 2:
        return 'paper'
    if number == 3:
        return 'lizard'
    if number == 4:
        return 'scissors'
    else:
        print "Your's input is bizzare. I'll choose 'rock' instead."
        return 'rock'

def rpsls(player_choice):
    '''Selects the winner of the game.'''

    print ''
    print 'Player chooses', player_choice
    player_number = name_to_number(player_choice)
    comp_number = random.randrange(0,5)
    comp_choice = number_to_name(comp_number)
    print 'Comupter chooses', comp_choice
    result = (comp_number - player_number) % 5
    if result == 1 or result == 2:
        print 'Computer wins!'
    elif result == 3 or result == 4:
        print 'Player wins!'
    else:
        print 'Tie'

rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
