"""
An Introduction to Interactive Programming in Python (by Coursera and Rice
University). Week 2 programming assignment: "Guess the number".
Link to the code in CodeSculptor: http://www.codeskulptor.org/#user42_a38E0BHpjo_23.py
"""

import simplegui
import random
import math

secret_number = 0
num_of_guesses = 0
guesses_max = 0
num_range = 100

def new_game():
    '''Starts and restarts the game in proper range.'''

    global secret_number
    global num_range
    global guesses_max
    global num_of_guesses
    num_of_guesses = 0
    secret_number = random.randrange(0, num_range)

    if num_range == 100:
        guesses_max = int(math.ceil(math.log(100, 2)))
    else:
        guesses_max = int(math.ceil(math.log(1000,2)))
    print '''
    New Game
    Range is from 0 to %d.
    You have %d gusses
    ''' % (num_range, guesses_max)

    return guesses_max, num_of_guesses, secret_number

def range100():
    '''Changes the range to [0,100) and restarts a new game'''

    global num_range
    num_range = 100
    new_game()

def range1000():
    '''Changes the range to [0,1000) and starts a new game'''

    global num_range
    num_range = 1000
    new_game()

def input_guess(guess):
    '''Evaluates players guesses against computer generated numbers'''

    global num_of_guesses
    global guesses_max
    global num_range

    try:
        guess = int(guess)
    except ValueError:
        guess = random.randrange (0, num_range)
        print '''
        Only integers are allowed.
        You've lost one turn.
        We guess for you.
        Our choice is %d.
        ''' % guess
    print '\nGuess was', guess

    if guess == secret_number:
        print 'Correct'
        new_game()
    elif guess < secret_number:
        print 'Higher'
        num_of_guesses += 1
    else:
        print 'Lower'
        num_of_guesses += 1

    if num_of_guesses > 0 and num_of_guesses < guesses_max:
        print 'Only', guesses_max - num_of_guesses, 'guesses left.'

    if num_of_guesses == guesses_max:
        print '''
        You've run out of guesses. The secret number was %d
        Let's start New Game! Good luck!
              ''' % secret_number
        new_game()

frame = simplegui.create_frame('Guss the number', 200, 200)
frame.add_button('Range 1-100', range100, 100)
frame.add_button('Range 1-1000', range1000, 100)
frame.add_input('Guss', input_guess, 50)
frame.start()

new_game()
