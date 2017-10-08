"""
Principles of Computing (by Coursera and Rice
University). Week 4 programming assignment: "Planner for Yahtzee".
Simplifications:  only allow discard and roll, only score against upper level.
Link to code in CodeSculptor: http://www.codeskulptor.org/#user42_osAHQP9buT_58.py
"""

# Used to increase the timeout, if necessary
import codeskulptor
import random
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """

    scores_keys = [dummy for dummy in set(hand)]
    scores_values = [0 for dummy in range(1, len(hand) + 1)]
    scores = dict(zip(scores_keys, scores_values))
    for dummy_value in hand:
        scores[dummy_value] += dummy_value
    for dummy_value in scores.values():
        best_score = max(scores.values())
    return best_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    total_score = 0
    outcomes = [dummy for dummy in range
                (1, num_die_sides + 1)]
    for dummy_enumeration in gen_all_sequences(outcomes, num_free_dice):
        hand = sorted((held_dice)+ dummy_enumeration)
        total_score += score(hand)
    e_v = float(total_score)/(num_die_sides**num_free_dice)
    return e_v


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    subsets_lst = [[]]
    if len(hand) == 0:
        subset = set([()])
    else:
         for dummy_die in hand:
            subset_1_lst = subsets_lst[:]
            subset_1 = set([tuple(sorted(dummy)) for dummy in subset_1_lst])
            subset_2_lst = subsets_lst[:]
            subset_2 = set([()])
            for element in subset_2_lst:
                element.append(dummy_die)
            subset_2 = set([tuple(sorted(dummy)) for dummy in subset_2_lst])
            subset = subset_2.union(subset_1)
            subsets_lst = list(subset)
            subsets_lst = [list(dummy) for dummy in subsets_lst]
    return subset


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """

    all_expected_vals = []
    all_dice_holds = []
    for dummy_hold in gen_all_holds(hand):
        all_dice_holds.append(dummy_hold)
        e_v =  expected_value(dummy_hold, num_die_sides,
                              len(hand) - len(dummy_hold))
        all_expected_vals.append(e_v)
    best_e_v_lst = [max(all_expected_vals)]

    for dummy_e_v in best_e_v_lst:
        ind_of_corr_vals = all_expected_vals.index(dummy_e_v)
        dice_to_hold = [all_dice_holds[ind_of_corr_vals]]
    results = [(best_e_v, dice)
               for best_e_v in best_e_v_lst
               for dice in dice_to_hold]

    return random.choice(results)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score



#run_example()

#test.run_suite_score(score)
#test.run_suite_expected_value(expected_value)

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
