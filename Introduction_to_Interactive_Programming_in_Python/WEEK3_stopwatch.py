"""
An Introduction to Interactive Programming in Python (by Coursera and Rice
University). Week 3 programming assignment: "Stopwatch".
Link to the code in CodeSculptor: http://www.codeskulptor.org/#user42_KdtHCt2yVi_26.py
"""


import simplegui

clock = 0
all_stop_clicks = 0
good_reflex_clicks = 0


def format(tenths_of_secs):
    '''Converts time in tenths of secs into formatted string A:BC.D'''

    if tenths_of_secs in range(0, 10):
        return '0:00.%s' % tenths_of_secs

    elif tenths_of_secs in range (10, 600):
        if tenths_of_secs / 10 < 10:
            return '0:0%s.%s' % (tenths_of_secs / 10, tenths_of_secs % 10)
        else:
            return '0:%s.%s' % (tenths_of_secs / 10, tenths_of_secs % 10)

    elif tenths_of_secs in range(600, 6000):
        if tenths_of_secs % 600 < 10:
            last_digit = tenths_of_secs % 600
        else:
            last_digit = (tenths_of_secs % 600) % 10
        if (tenths_of_secs % 600)/10 < 10:
            return '%s:0%s.%s' % (tenths_of_secs / 600,
                                  (tenths_of_secs % 600) / 10,
                                  last_digit)
        else:
            return '%s:%s.%s' % (tenths_of_secs / 600,
                                 (tenths_of_secs % 600) / 10,
                                 last_digit)

def start():
    '''Starts the timer'''

    timer.start()

def stop():
    '''Stops the timer and counts total and successful number of stops'''

    global all_stop_clicks
    global good_reflex_clicks
    global clock
    if timer.is_running():
        timer.stop()
        all_stop_clicks += 1
        if clock % 10 == 0:
            good_reflex_clicks += 1

def reset():
    '''Resets the timer'''

    global clock
    global all_stop_clicks
    global good_reflex_clicks
    if timer.is_running():
        timer.stop()
    clock = 0
    all_stop_clicks = 0
    good_reflex_clicks = 0

def tick():
    '''Keeps track of the time in tenths of seconds.'''

    global clock
    clock += 1
    if clock == 6000:
        clock = 0

def draw_handler(canvas):
    '''Draws the time and number of clicks in canvas'''

    global clock
    global all_stop_clicks
    global good_reflex_clicks
    formatted_clock = format(clock)
    all_clicks = str(all_stop_clicks)
    good_reflex = str(good_reflex_clicks)
    clicks_ratio = '%s / %s' % (good_reflex, all_clicks)
    canvas.draw_text(formatted_clock, (60, 170), 65, 'White', 'sans-serif')
    canvas.draw_text(clicks_ratio, (197, 80), 40, 'Red', 'sans-serif')

frame = simplegui.create_frame("Stop Watch", 300, 300)
frame.set_draw_handler(draw_handler)
frame.add_button('Start', start, 150)
frame.add_button('Stop', stop, 150)
frame.add_button('Reset', reset, 150)
timer = simplegui.create_timer(100, tick)
frame.start()
