"""
Principles of Computing (by Coursera and Rice
University). Week 5 programming assignment: "Cookie Clicker Simulator".
Link to code in CodeSculptor: http://www.codeskulptor.org/#user42_fHIoOjJhDq_16.py
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

#SIM_TIME = 2500.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._cookies_total_num = 0.0
        self._cookies_current_num = 0.0
        self._current_cps = 1.0
        self._current_time = 0.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def get_game_state(self):
        """
        Return state of game
        """

        return self._cookies_total_num, self._cookies_current_num, self._current_time, self._current_cps

    def __str__(self):
        """
        Return human readable state
        """
        self._clicker_state_read = '''
*total number of cookies: %s
*current number of cookies: %s
*current time: %s
*current CPS: %s''' % (self._cookies_total_num,
                       self._cookies_current_num,
                       self._current_time,
                       self._current_cps)

        return self._clicker_state_read


    def get_total_cookies(self):
        """
        Return total number of cookies
        """
        return self._cookies_total_num

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._cookies_current_num



    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        self._history_copy = self._history[:]
        return self._history_copy

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._cookies_current_num < cookies:
            self._cookies_time = math.ceil((cookies -  self._cookies_current_num)
                                       /self.get_cps())
        else:
            self._cookies_time = 0.0

        return self._cookies_time


    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._current_time += time
            self._cookies_current_num += time * self._current_cps
            self._cookies_total_num += time * self._current_cps


    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        #print item_name
        if  self._cookies_current_num >= cost:
            self._current_cps += additional_cps
            self._cookies_current_num -= cost
            #in self hist necessery to check if item bought
            #if note
            self._history.append((self.get_time(),
                                  item_name,
                                  cost,
                                  self.get_total_cookies()))



def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    items_shop_info = build_info.clone()
    state_of_game = ClickerState()

    while duration > 0:
        if state_of_game.get_time() > duration:
            break
        num_of_cookies = state_of_game.get_cookies()
        production_ratio = state_of_game.get_cps()
        game_history = state_of_game.get_history()
        production_time = duration - state_of_game.get_time()

        next_to_buy = strategy(num_of_cookies, production_ratio,
                               game_history, production_time, items_shop_info)
        if next_to_buy == None:
            state_of_game.wait(production_time)
            break
        time_to_wait = state_of_game.time_until(items_shop_info.get_cost(next_to_buy))
        if time_to_wait > production_time:
            state_of_game.wait(production_time)
            duration = 0
        else:
            state_of_game.wait(time_to_wait)
            state_of_game.buy_item(next_to_buy,
                                   items_shop_info.get_cost(next_to_buy),
                                   items_shop_info.get_cps(next_to_buy))
            items_shop_info.update_item(next_to_buy)


    return state_of_game



def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """


    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    production_output = (time_left * cps) + cookies
    production_methods = {}
    for method in build_info.build_items():
        production_methods[build_info.get_cost(method)] = method
    if production_output >= sorted(list(production_methods.keys()))[0]:
        return production_methods[sorted(list(production_methods.keys()))[0]]
    else:
        return None


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    production_output = (time_left * cps) + cookies
    production_methods = {}
    for method in build_info.build_items():
        production_methods[build_info.get_cost(method)] = method
    for cost in sorted(list(production_methods.keys()), reverse = True):
        if production_output >= cost:
            return  production_methods[cost]
    else:
        return None


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    production_output = (time_left * cps) + cookies
    production_methods = {}
    lucky_go = []
    for method in build_info.build_items():
        production_methods[build_info.get_cost(method)] = method
    lucky_go = [cost for cost in sorted(list(production_methods.keys()))
                if production_output >= cost]
    #print 'i am lucky list', lucky_go
    if lucky_go:
        return production_methods[random.choice(lucky_go)]
    else:
        return None



def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state


    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    #run_strategy("Cursor", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

#run()

#cookies = 123456789.0
#cps = 1.0
#history = 1
#time_left = 1
#build_info = provided.BuildInfo()

#print strategy_cheap(cookies, cps, history, time_left, build_info)


# 123456789.0: 'Time Machine', 3999999999.0: 'Antimatter Condenser

#print strategy_expensive(cookies, cps, history, time_left, build_info)
