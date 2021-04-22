from copy import deepcopy
import random

"""
SudokuBoard is a class that creates random puzzles with a solution to the board.
Also used to solve any puzzle (9x9).

Static Methods: 
-'SudokuBoard.solve_game(param: game = "board, any 9x9 board")' will solve param board, will modify that board, will return True if solved else False.
-'SudokuBoard.find_next_empty(param: game = "board, any 9x9 board")' will find next 0 in board, used for solve_game method, return: (x,y ) or (None, None) if full
-'SudokuBoard.is_valid(params: game = "board, any 9x9 board", num = "attempted number to place", pos = "position to place attempt")' will check if num is valid to place in board based on position, return: True/False
"""
class SudokuBoard:

    #will modify board and return True if solved, or False if not 
    @staticmethod
    def solve_game(game): #lists are mutable, will be modified
        x, y = SudokuBoard.find_next_empty(game)

        if x is None:
            return True

        for atmpt in range(1, 10): #inclusive since its valid num from 1-9
            if SudokuBoard.is_valid(game, atmpt, (x,y)):
                game[y][x] = atmpt

                if SudokuBoard.solve_game(game):
                    return True
            
                game[y][x] = 0 

        return False

    #used for solve_game to find slots in board with a 0
    @staticmethod
    def find_next_empty(game): 
        
        for y in range(9):
            for x in range (9):
                if game[y][x] == 0:
                    return x, y

        return None, None

    # method to figure if position is valid, num is number to check, pos is position '(col, row)' attempted
    @staticmethod 
    def is_valid(game, num, pos:tuple):

        for i in range(9):
            if game[pos[1]][i] == num or game[i][pos[0]] == num:
                return False
        
        #Inner Box
        for y in range(3*(pos[1]//3), 3*(pos[1]//3)+3):
            for x in range(3*(pos[0]//3), 3*(pos[0]//3)+3):
                if game[y][x] == num and (x,y) != pos:
                    return False
        
        return True


    def __init__(self, board=None): #sets board
        if not board: self.solution = [[0 for i in range(9)] for _ in range(9)]
        else: self.solution = board
        SudokuBoard.solve_game(self.solution)

        self.board = deepcopy(self.solution)
        self.remove_numbers(self.board)


    def ftest(self, board):
        """
        Test if board is correctly solved.
        """
        #test horizontal 
        for row in board:
            test = [x for x in range(1,10)]
            for i in range(9): test.remove(row[i]) if row[i] in test else i
            if test !=[]: return False
        #test vertical
        for i in range(9):
            test = [x for x in range(1,10)]
            for row in board: test.remove(row[i]) if row[i] in test else i
            if test !=[]: return False
        
        return True

    def stest(self, game):
        """
        Test if board can be solved. Will not modify board.
        """
        board_copy = deepcopy(game)
        return SudokuBoard.solve_game(board_copy)


    def new_board(self, game):
        """
        Create a new board using random. Only solution board will be created.
        """

        number_list = random.sample([1,2,3,4,5,6,7,8,9], 9)

        x, y = SudokuBoard.find_next_empty(game)

        if x is None:
            return True

        
        for atmpt in number_list: 
            if SudokuBoard.is_valid(game, atmpt, (x,y)):
                game[y][x] = atmpt

                if self.new_board(game):
                    return True
            
                game[y][x] = 0 

        return False
    
    def create_new(self):
        """
        Create new puzzle by creating new board solution and removing numbers. 
        """
        self.solution = [[0 for i in range(9)] for _ in range(9)]
        self.new_board(self.solution)
        self.board = deepcopy(self.solution)
        self.remove_numbers(self.board)

    def remove_numbers(self, game=None):
        """
        Randomly remove numbers from board. Clues left are random and there will only be one solution to board.
        """
        game = game if game is not None else self.board
        origin = deepcopy(game) 

        while True and game!=[[0 for _ in range(9)] for _ in range(9)]: 
            x,y = (random.randint(0,8),random.randint(0,8))
            if game[y][x] != 0:

                game[y][x] = 0
                check = deepcopy(game)
                SudokuBoard.solve_game(check)

                if check != origin:
                    break


    def __str__(self):
        """Print out board (puzzle) when object is printed."""
        return "".join(str(row)+'\n' for row in self.board)

    def __getitem__(self, index): #returns self.solution[]
        """Return board (puzzle) row when object needs to use index."""
        if type(index) is int: return self.board[index]
        else: NotImplemented
