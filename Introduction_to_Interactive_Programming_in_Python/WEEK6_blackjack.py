"""
An Introduction to Interactive Programming in Python (by Coursera and Rice
University). Week 6 programming assignment: "Blackjack".
Link to code in CodeSculptor: http://www.codeskulptor.org/#user42_GG0kYQcbBU_21.py
"""

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

in_play = False
outcome = ""
score = 0
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10,
          'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)

class Hand:
    def __init__(self):
        self.list_of_cards = []
        self.readable_list_of_cards = ''
        for x in range(len(self.list_of_cards)):
            self.readable_list_of_cards += str(self.list_of_cards[x]) + ' '

    def __str__(self):
        return 'Hand contains %s' % self.readable_list_of_cards

    def add_card(self, card):
        self.list_of_cards.append(card)
        return self.list_of_cards

    def get_value(self):
        self.hand_value = 0
        for card in self.list_of_cards:
            self.key = card.get_rank()
            self.card_value = VALUES[self.key]
            self.hand_value += self.card_value
        if 'A' not in self.readable_list_of_cards:
            return self.hand_value

        else:
            if self.hand_value + 10 <= 21:
                return self.hand_value + 10
            else:
                return self.hand_value


    def draw(self, canvas, pos):
        for card in self.list_of_cards:
            card.draw(canvas,
                      [CARD_SIZE[0] + ((pos[0] + CARD_SIZE[0] + CARD_CENTER[0]) * list(self.list_of_cards).index(card)),
                       pos[1]])

class Deck:
    def __init__(self):
        self.list_of_decks = [Card(suit, rank) for suit in SUITS
                              for rank in RANKS]

    def shuffle(self):
        return random.shuffle(self.list_of_decks)

    def deal_card(self):
        return self.list_of_decks.pop()

    def __str__(self):
        self.readable_list_of_decks = ''
        for x in range(len(self.list_of_decks)):
            self.readable_list_of_decks += str(self.list_of_decks[x]) + ' '
        return 'Deck contains %s' % self.readable_list_of_decks

def deal():
    '''Starts a new round, deals cards to the players.'''

    global outcome, in_play, deck, player_hand, dealer_hand, outcome, score
    outcome = ''
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    for num in range(2):
        player_card = deck.deal_card()
        dealer_card = deck.deal_card()
        player_hand.add_card(player_card)
        dealer_hand.add_card(dealer_card)
    if in_play:
        outcome = "You've lost your round."
        score -= 1
    else:
        in_play = True

def hit():
    '''Hits the player where appropriate, updates messages, in_play & score.'''

    global deck, player_hand, in_play, outcome, score
    if in_play and player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = 'You\'ve busted and lost.'
            in_play = False
            score -= 1

def stand():
    '''Hits the dealer where appropriate, updates messages, in_play & score.'''

    global deck, player_hand, dealer_hand, in_play, outcome, score
    if player_hand.get_value() > 21:
        outcome = 'You\'ve already busted and lost.'
    else:
        while dealer_hand.get_value() < 17 and in_play:
            dealer_hand.add_card(deck.deal_card())
        in_play = False
        if dealer_hand.get_value() > 21 and not in_play and outcome == '':
            outcome = 'Dealer busts. You win.'
            score += 1
        elif (dealer_hand.get_value() >= player_hand.get_value()
              and not in_play and outcome == ''):
            outcome = 'Dealer wins.'
            score -= 1
        elif (dealer_hand.get_value() < player_hand.get_value()
              and not in_play and outcome == ''):
            outcome = 'Player wins.'
            score += 1

def draw(canvas):
    '''Draws everything into the canvas.'''

    global player_hand, dealer_hand, outcome, in_play, card_back, score
    dealer_hand_pos = [0, 200]
    player_hand_pos = [0, 400]
    dealer_hand.draw(canvas, dealer_hand_pos)
    player_hand.draw(canvas, player_hand_pos)
    canvas.draw_text('Blackjack', [25, 50], 50, 'Black', 'sans-serif')
    result = 'Score %s' % score
    canvas.draw_text(result, [400, 120], 30, 'Black', 'sans-serif')
    canvas.draw_text('Dealer', [CARD_SIZE[0] + dealer_hand_pos[0],
                     dealer_hand_pos[1] - CARD_CENTER[1] + 15],
                     20, 'Black', 'sans-serif')
    canvas.draw_text('Player', [CARD_SIZE[0] + player_hand_pos[0],
                     player_hand_pos[1] - CARD_CENTER[1] + 15],
                     20, 'Black', 'sans-serif')
    canvas.draw_text(outcome, [CARD_SIZE[0] + dealer_hand_pos[0] + 150,
                     dealer_hand_pos[1] - CARD_CENTER[1] + 15],
                     20, 'Blue', 'sans-serif')
    if in_play:
        canvas.draw_text('Hit or stand?', [CARD_SIZE[0] + player_hand_pos[0] + 150,
                         player_hand_pos[1] - CARD_CENTER[1] + 15],
                         20, 'Black', 'sans-serif')
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * 0,
                    CARD_CENTER[1] + CARD_SIZE[1] * 0)
        canvas.draw_image(card_back, card_loc, CARD_SIZE,
                         [CARD_SIZE[0] + dealer_hand_pos[0] + CARD_CENTER[0],
                          dealer_hand_pos[1] + CARD_CENTER[1]], CARD_SIZE)
    else:
        canvas.draw_text('New deal?', [CARD_SIZE[0] + player_hand_pos[0] + 150,
                         player_hand_pos[1] - CARD_CENTER[1] + 15],
                         20, 'Black', 'sans-serif')

frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
deal()
frame.start()
