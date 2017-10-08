"""
An Introduction to Interactive Programming in Python (by Coursera and Rice
University). Week 5 programming assignment: "Memory".
Link to code in CodeSculptor: http://www.codeskulptor.org/#user42_cc7neB7AGd_25.py
"""

# implementation of card game - Memory

import simplegui
import random

LINE_SIZE = 16
NUMBERS_DISTANCE = 25
CARD_DECKS = map(str, [x for x in range(8)]*2)

def new_game():
    '''Helper function to initialize globals'''

    global CARD_DECKS, exposed, state, first_card, second_card, test_cases, turns_counter, text_for_label
    random.shuffle(CARD_DECKS)
    exposed = [False] * 16
    state = 0
    first_card = None
    second_card = None
    test_cases = []
    turns_counter = 0
    text_for_label = 'Turns = %s' % turns_counter
    label.set_text(text_for_label)

def mouseclick(pos):
    '''Flips and unflips cards when appropriate and draws turns'''

    global state, first_card, second_card, test_cases, turns_counter, text_for_label
    x = int(pos[0]//50)
    if x not in test_cases:
        test_cases.append(x)
        exposed[x] = True
        if state == 0:
            first_card = x
            turns_counter += 1
            state = 1
        elif state == 1:
            second_card = x
            state = 2
        elif state == 2:
            if (CARD_DECKS[first_card] != CARD_DECKS[second_card]):
                exposed[first_card] = False
                exposed[second_card] = False
                test_cases.pop(-2)
                test_cases.pop(-2)
            first_card = x
            turns_counter += 1
            state = 1

        text_for_label = 'Turns = %s' % turns_counter
        label.set_text(text_for_label)

def draw(canvas):
    '''Draws flipped and unflipped cards in the canvas'''

    for card in CARD_DECKS:
        for x in range(LINE_SIZE):
            canvas.draw_polygon([[x * 2 * NUMBERS_DISTANCE, 0],
                                 [x * 2 * NUMBERS_DISTANCE + 2 * NUMBERS_DISTANCE, 0],
                                 [x * 2 * NUMBERS_DISTANCE + 2 * NUMBERS_DISTANCE, 100],
                                 [x * 2 * NUMBERS_DISTANCE, 100]],
                                1, 'Red', 'Green')
            if exposed[x]:
                canvas.draw_polygon([[x * 2 * NUMBERS_DISTANCE, 0],
                                 [x * 2 * NUMBERS_DISTANCE + 2 * NUMBERS_DISTANCE, 0],
                                 [x * 2 * NUMBERS_DISTANCE + 2 * NUMBERS_DISTANCE, 100],
                                 [x * 2 * NUMBERS_DISTANCE, 100]],
                                1, 'White', 'White')
                canvas.draw_text(CARD_DECKS[x], [2 * NUMBERS_DISTANCE * x + NUMBERS_DISTANCE, 50], 20, "Red")

frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label('Turns = 0')
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
new_game()
frame.start()
