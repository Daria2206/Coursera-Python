"""
Principles of Computing (by Coursera and Rice
University). Week 3 programming assignment: "Monte Carlo Tic-Tac-Toe Player".
Link to code in CodeSculptor: http://www.codeskulptor.org/#user42_4hIXXhMML12joNR_14.py
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator

NTRIALS = 100        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

SCORES_VALS = {True:(SCORE_CURRENT, SCORE_OTHER),
               False:(SCORE_OTHER, SCORE_CURRENT)}


def mc_trial(board, player):
    '''Plays an entire TTT game starting with the given player.
    Modifies the input board.'''

    while board.check_win() == None:
        random_empty_square = random.choice(board.get_empty_squares())
        board.move(random_empty_square[0], random_empty_square[1], player)
        player = provided.switch_player(player)


def mc_update_scores(scores, board, player):
    '''Takes a grid of scores (of the same dimensions
    as the TTT board), a board from a completed game,
    and the machine player, scores the completed board
    and updates the scores grid.'''

    if (board.check_win() == provided.PLAYERO or
        board.check_win() == provided.PLAYERX):
        winner = board.check_win()
        winner_score = SCORES_VALS[player == winner][0]
        opponent_score = SCORES_VALS[player == winner][1]
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == winner:
                    scores[row][col] += winner_score
                elif board.square(row, col) == provided.EMPTY:
                    scores[row][col] += 0
                else:
                    scores[row][col] -= opponent_score


def get_best_move(board, scores):
    ''' Takes a current board and a grid of scores,
    finds all of the empty squares with the maximum score
    and randomly return one of them as a (row, column) tuple.'''

    maximum_scores_indices = []
    maximum_scores_to_remove = []
    largest = None
    if board.get_empty_squares():
        empty_idices_lst = board.get_empty_squares()
        for element in empty_idices_lst:
            if (largest is None or
                scores[element[0]][element[1]] >= largest):
                largest = scores[element[0]][element[1]]
            maximum_scores_indices.append(element)
        for element in maximum_scores_indices:
            if scores[element[0]][element[1]] < largest:
                maximum_scores_to_remove.append(element)
        for element in maximum_scores_to_remove:
            maximum_scores_indices.remove(element)

    if maximum_scores_indices:
        best_move = random.choice(maximum_scores_indices)
        return best_move


def mc_move(board, player, trials):
    '''Takes a current board, the machine player,
    and the number of trials to run. Uses the Monte Carlo
    simulation to return a move for the machine player
    in the form of a (row, column) tuple.'''

    scores = [[0 for dummy_row in range(board.get_dim())]
              for dummy_col in range(board.get_dim())]
    for dummy_num in range(trials):
        current_board = board.clone()
        mc_trial(current_board, player)
        mc_update_scores(scores, current_board, player)
    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
