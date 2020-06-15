import random
import numpy as np
from functools import wraps

class Play2048:

    _WINING_NUM = 2048
    _DIMENSION = None
    _PROBABILITY = [2,2,2,2,2,2,2,2,2,4]

    def __repr__(self):
        return f'<Play2048 {self._DIMENSION}X{self._DIMENSION} board>'

    def __init__(self, dimension):
        print(f"Start playing {dimension}X{dimension} 2048")
        self._DIMENSION = dimension
        self.valid = True # still has valid moves
        self.ws = self._DIMENSION**2 # white spaces count
        self.valid_keys = ['w', 'a', 's', 'd']
        self.win = False

        self.board = np.full([self._DIMENSION, self._DIMENSION], 0)
        self.random_tile()
        self.random_tile()

    def print_board(self, msg=None):
        if msg:
            print(msg)
        print('*'*10)
        print(self.board)
        print('*'*10)

    def playing(self):
        while self.valid:
            k = input("choose w/s/a/d: ")
            if k not in self.valid_keys:
                print(f"Please choose from {self.valid_keys}")
                continue

            if k == 'w':
                self.move_up()
            elif k == 's':
                self.move_down()
            elif k == 'a':
                self.move_left()
            else:
                self.move_right()

            self.print_board()
            self.verify_valid_moves_exist()

        if self.win:
            print("You win")
        else:
            print("You lose")

    @staticmethod
    def rand_cell():
        return (random.randint(0, self._DIMENSION-1), random.randint(0, self._DIMENSION-1))

    def _decorator(rotate=0):
        def wrapper(func):
            @wraps(func)
            def move(self):
                if rotate > 0:
                    self.board = np.rot90(self.board, rotate)
                self.calc_new_state()
                self.random_tile()
                if rotate > 0:
                    self.board = np.rot90(self.board, 4 - rotate)
                self.is_winner()
            return move
        return wrapper

    @_decorator(1)
    def move_up(self):
        pass

    @_decorator(3)
    def move_down(self):
        pass

    @_decorator()
    def move_left(self):
        pass

    @_decorator(2)
    def move_right(self):
        pass


    def calc_new_state(self):
        '''
        all computations are done from right to left
        '''
        # TODO

        for i in range(self._DIMENSION):
            self.board[i] = self.calc_single(self.board[i])


    def pop_n(self, lst):
        ''' remove any None values'''
        while 0 in lst:
            lst.remove(0)

        return lst

    def compare(self, lst):
        ''' '''

        if len(lst) > 1:
            for i in range(len(lst)-1):
                if lst[i] == lst[i+1]:
                    lst[i] = lst[i]*2
                    lst[i+1] = 0
        lst = self.pop_n(lst)
        lst.extend([0]*(self._DIMENSION-len(lst)))
        return lst

    def calc_single(self, lst):

        if not any(lst): # all tiles equal None
            return lst

        return self.compare(self.pop_n(lst.tolist()))

    def is_winner(self):
        if self._WINING_NUM in self.board:
            self.win = True
            self.valid = False


    def random_val(self):
        return self._PROBABILITY[random.randint(0, len(self._PROBABILITY)-1)]

    def random_tile(self):
        empty_tiles = np.argwhere(self.board == 0)
        if len(empty_tiles) > 0: # no empty tiles left
            tile = empty_tiles[random.randint(0, len(empty_tiles)-1)].tolist()
            self.board[tile[0], tile[1]] = self.random_val()
            self.ws -= 1


    def verify_valid_moves_exist(self):
        _curr_board = self.board.copy()

        self.move_up()
        if (_curr_board - self.board).any():
            self.board = _curr_board
            return

        self.move_down()
        if (_curr_board - self.board).any():
            self.board = _curr_board
            return

        self.move_left()
        if (_curr_board - self.board).any():
            self.board = _curr_board
            return

        self.move_right()
        if (_curr_board - self.board).any():
            self.board = _curr_board
            return

        print("No more valid moves")
        self.valid = False
