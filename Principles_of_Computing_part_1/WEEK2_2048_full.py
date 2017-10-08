"""
Principles of Computing (by Coursera and Rice
University). Week 2 programming assignment: "Clone of 2048 game.".
Link to code in CodeSculptor: http://www.codeskulptor.org/#user42_HyQbBQj2pb_7.py
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

LIST_OF_TILES = [2] * 9 + [4]

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """

    output = [x for x in line if x != 0]

    for num in range(1, len(output)):
        if len(output) > num:
            key = output[num]
            prev = num - 1

            if output[prev] == key:
                output[prev + 1] = output[prev] * 2
                output[prev:prev + 1] = []

    num_of_zeros_to_fill = len(line) - len(output)
    output += [0] * num_of_zeros_to_fill

    return output

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):

        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self._start_tiles = {UP: [(0, col)
                            for col in
                            range(self._grid_width)],
                            DOWN: [(self._grid_height - 1, col)
                            for col in
                            range(self._grid_width)],
                            LEFT: [(row, 0)
                            for row in
                            range(self._grid_height)],
                            RIGHT: [(row, self._grid_width  - 1)
                            for row in
                            range(self._grid_height)]}


    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """

        self._grid = [[0 for dummy_col in range(self._grid_width)]
                     for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()


    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """

        self._display = ''
        for row in self._grid:
            self._display += str(row) + '\n'
        return 'This is our grid: \n%s' % self._display


    def get_grid_height(self):
        """
        Get the height of the board.
        """

        return self._grid_height


    def get_grid_width(self):
        """
        Get the width of the board.
        """

        return self._grid_width


    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        self._moved_flag = False
        self._temp_lst = []
        self._direction = OFFSETS[direction]

        self._num_steps = self._grid_width
        if direction == UP or direction == DOWN:
            self._num_steps = self._grid_height

        for dummy_element in range(len(self._start_tiles[direction])):
            self._start_cell = self._start_tiles[direction][dummy_element]
            for dummy_step in range(self._num_steps):
                self._row = self._start_cell[0] + dummy_step * self._direction[0]
                self._col = self._start_cell[1] + dummy_step * self._direction[1]

                if len(self._temp_lst) < self._num_steps:
                    self._temp_lst.append(self._grid[self._row][self._col])

                if len(self._temp_lst) == self._num_steps:
                    self._temp_lst_merged = merge(self._temp_lst)

                    if self._temp_lst_merged != self._temp_lst:
                        self._moved_flag = True
                        for dummy_step in range(self._num_steps):
                            self._row = self._start_cell[0] + dummy_step * self._direction[0]
                            self._col = self._start_cell[1] + dummy_step * self._direction[1]
                            self.set_tile(self._row, self._col, self._temp_lst_merged[dummy_step])
                    self._temp_lst = []
                    continue

        if self._moved_flag:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """

        self._empty_squers_indices = [(row, col)
                                     for row in range(self._grid_height)
                                     for col in range(self._grid_width)
                                     if self.get_tile(row, col) == 0]
        if self._empty_squers_indices:
            self._row, self._col = random.choice(self._empty_squers_indices)
            self.set_tile(self._row, self._col, random.choice(LIST_OF_TILES))


    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """

        self._grid[row][col] = value


    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """

        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
