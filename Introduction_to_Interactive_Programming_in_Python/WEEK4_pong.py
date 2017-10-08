"""
An Introduction to Interactive Programming in Python (by Coursera and Rice
University). Week 4 programming assignment: "Pong".
Link to code in CodeSculptor: http://www.codeskulptor.org/#user42_ufQH4SxId4_10.py
"""

# Implementation of classic arcade game Pong.

import simplegui
import random

# Initialize globals.
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [1, 1]
mysterious_num = random.randrange(0, 2)
paddle1_pos = HALF_PAD_HEIGHT
paddle2_pos = HALF_PAD_HEIGHT
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

def spawn_ball(direction):
    '''Initializes ball_pos and ball_vel for new bal in middle of table'''

    global ball_pos, ball_vel
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240)/120
        ball_vel[1] = -random.randrange(60, 80)/120
    elif direction == LEFT:
        ball_vel[0] = -random.randrange(120, 240)/120
        ball_vel[1] = -random.randrange(60, 80)/120

def new_game():
    '''Restarts the game'''

    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2, mysterious_num  # these are ints
    score1 = 0
    score2 = 0
    if mysterious_num == 0:
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)

def draw(canvas):
    '''Draws all elements of the game in the canvas'''

    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # Draws mid line and gutters.
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # Updates ball.
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[0] = ball_vel[0]
        ball_vel[1] = -ball_vel[1]

    if (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and not
    (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and
     ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and
     ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT + 1)):
        score1 += 1
        spawn_ball(RIGHT)
    if (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and
        ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and
        ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT + 1):
        ball_vel[0] = -ball_vel[0] * 1.1
        ball_vel[1] = ball_vel[1] * 1.1

    if (ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH) and not
    (ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH) and
     ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and
     ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT + 1)):
        score2 += 1
        spawn_ball(LEFT)
    if (ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH) and
        ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and
        ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT + 1):
        ball_vel[0] = -ball_vel[0] * 1.1
        ball_vel[1] = ball_vel[1] * 1.1

    # Draws ball.
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

    # Updates paddle's vertical position, keeps paddle on the screen.
    if paddle1_pos <= HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT + 1
    elif paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT - 1
    else:
        paddle1_pos += paddle1_vel

    if paddle2_pos <= HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT + 1
    elif paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT - 1
    else:
        paddle2_pos += paddle2_vel

    # Draws paddles.
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT],
                     [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],
                     8, 'Red')
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT],
                     [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT],
                     8, 'Red')

    # Draws scores.
    score1_s = str(score1)
    canvas.draw_text(score1_s, [WIDTH/2 + WIDTH/4, 48], 40, 'White')
    score2_s = str(score2)  # Score when right hit.
    canvas.draw_text(score2_s, [WIDTH/4, 48], 40, 'White')

def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 3
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc

def keyup(key):
    global paddle1_vel, paddle2_vel
    dcc = 3
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel += dcc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel -= dcc
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel += dcc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel -= dcc

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background("Green")
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', new_game, 100)
new_game()
frame.start()
