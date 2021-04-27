import time, math, pygame
from copy import deepcopy
from pygame import draw, display, font
from S2 import SudokuBoard

# SET VARIABLES
WIDTH = 700
HEIGHT = 800
RED = (255,0,0)
GREEN = (0,159,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (10,30,160)
LBLUE = (15, 175, 255)

"""
Integrates SudokuBoard class to create new puzzles and sets up window for drawing widgets.
Manages needed click moves, key values enetered, resets board, checks board, and sets time.
"""
class Sudoku:  # Game class

    def __init__(self, window, font): #sets : window / font / board
        self._window = window
        self.font = font
        self.board = SudokuBoard()

        self.main() #call to initiate main game

    #runs main game 
    def main(self):
        """
        Start game by resetting needed variables, running main loop, setting timer widget, and drawing window.
        """
        self.reset_game()

        run = True
        clock = pygame.time.Clock()
        starting_t = 0

        while run:
            clock.tick(10)
            #manages timer start and stop 
            if not self.paused:
                self.timer = (time.time() - starting_t)

            #draws screen 
            self.draw_screen()  

            #manages clicks and keys
            for event in pygame.event.get():
                self.key = None
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    if 560<pos[0]<640 and 20<pos[1]<60 and not self.start_time:
                        self.start_time = True
                        starting_t = time.time()
                    if 560<pos[0]<640 and 70<pos[1]<110:
                        self.check()

                    position = (math.floor((pos[0]-35)/70),math.floor((pos[1]-135)/70))
                    if position[0] in (0,1,2,3,4,5,6,7,8) and position[1] in (0,1,2,3,4,5,6,7,8):
                        self.clicked = position
                        self.key = self.board[position[1]][position[0]]
                        self.onClick()
                    else:
                        self.clicked = None
                   

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        self.board.board = self.board.solution
                        self.paused = True
                        self.solved = True
                    
                    if event.key == pygame.K_TAB:
                        self.reset_game()
                        continue

                    if event.key == pygame.K_s:
                        self.print_solution()

                    if event.key == pygame.K_p:
                        self.print_board()
                    
                    if self.clicked is None: #bottom can only be called when there's a clicked slot
                        continue

                    if event.key == pygame.K_RETURN:
                        self.valueInput()                   
                    
                    if event.key == pygame.K_DELETE or event.key == 8:
                        self.delInput()

                    if event.key == pygame.K_UP:
                        match = self.board[position[1]][position[0]]
                        self.key = match+1 if match<9  else 9
                        self.onClick()

                    if event.key == pygame.K_DOWN:
                        match = self.board[position[1]][position[0]]
                        self.key = match-1 if match>1  else 1
                        self.onClick()

                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        self.key = 1
                        self.onClick()
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        self.key = 2
                        self.onClick()
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        self.key = 3
                        self.onClick()
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        self.key = 4
                        self.onClick()
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        self.key = 5
                        self.onClick()
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        self.key = 6
                        self.onClick()
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        self.key = 7
                        self.onClick()
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        self.key = 8
                        self.onClick()
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        self.key = 9
                        self.onClick()


    def reset_game(self): 
        """
        Create a new board using the create_new method and reset the needed attributes.
        """
        print("reset game")
        self.board.create_new()                        #stores puzzle to interact
        self.original = deepcopy(self.board.board)     #stores puzzle to print black numbes
        #reset needed attributes for checking
        self.solved = False             #used for making numbers RED if asked to solve
        self.passed = False             #used for making numbers GREEN is solved
        self.start_time = False         #used to start timer
        self.clicked = None             #used to store clicked pos
        self.timer = 0                  #used to store time elapsed
        self.paused = False             #used to stop timer and not allow CHECK nor change values
        self.key = None                 #used to store key pressed


          
    def onClick(self): #only determines what to do when slot is clicked 
        """
        Set new number for clicked slot.
        """
        pos = self.clicked

        if self.paused or not self.start_time: # checks if playing 
            return
        if self.original[pos[1]][pos[0]]!=0: # must be playing and slot cannot be a non-zero slot in original 
            self.clicked = None
            return
        if self.clicked is None: #cant manage click if there's no clicked slot
            return

        # pos will be an open slot
        if self.key is None or self.key ==0:
            self.key = 9

        self.board[pos[1]][pos[0]] = self.key #sets slot to selected key else 9 if no stored value
        

    def valueInput(self): # for ENTER key purposes
        """
        Unclick selected slot.
        """
        print("return")
        if self.paused and not self.start_time:
            return
        
        #To unclick slot, reset key entered and saved click.
        self.key = None
        self.clicked = None


    def delInput(self): # for ENTER key purposes
        """
        Remove set number and set slot to be 0.
        """
        print("delete")
        pos = self.clicked

        if self.paused or not self.start_time: # checks if playing 
            return
        if self.original[pos[1]][pos[0]]!=0: # must be playing and slot cannot be a non-zero slot in original 
            self.clicked = None
            return

        self.board[pos[1]][pos[0]] = 0


    def check(self): # CHECK button : will check is position are correcct
        """
        Check if board is solved. If solved pause timer.
        """
        self.passed = self.board.ftest(self.board) and not self.solved
        if self.passed:
            print("passed")
            self.paused = True #stops timer
        else:
            print("not passed")

    def draw_screen(self):
        """
        Draw widgets and board on window.
        """
        #draws white screen and rectangles
        self._window.fill(WHITE)
        draw.rect(self._window, (110,110, 110), (30,130, 640,640), 10,1)
        draw.rect(self._window, RED, (560,70, 80,40))
        #draws timer : start_time is True if START button is pressed else False
        if self.start_time:
            self.font = pygame.font.SysFont("Comic Sans", 25)
            timer_text = self.font.render(("Timer:"), True, "black")
            self._window.blit(timer_text, (565,20))

            min = str(int(self.timer//60))
            sec = str(int(self.timer-(float(min)*60)))
            stringe = f"{min:0>2}:{sec:0>2}".format(min, sec)
            time_display = self.font.render((stringe), True, "black")
            self._window.blit(time_display, (565,45))
        else:
            draw.rect(self._window, GREEN, (560,20, 80,40))
            self.font = pygame.font.SysFont("Comic Sans", 30)
            b_text = self.font.render("START", 100, WHITE)
            self._window.blit(b_text, (565, 30))


        #draws lines
        for i in range(1, 10, 3):
            draw.line(self._window, (0, 0, 0), (i*70+35, 140), (i * 70+35, 760), 2)
            draw.line(self._window, (0, 0, 0), (i*70+105, 140), (i*70+105, 760), 2)
            draw.line(self._window, (0, 0, 0), (40, i*70+135), (660, i*70+135),  2)
            draw.line(self._window, (0, 0, 0), (40, i*70+205), (660, i*70+205),  2)
        
        for b in range(2,6,3):
            pygame.draw.line(self._window, (110, 110, 110), (b*70+105, 140), (b*70+105, 760), 5)
            pygame.draw.line(self._window, (110, 110, 110), (40, b*70+205), (660, b*70+205), 5)
        
        #draws letters
        self.font = pygame.font.SysFont("Comic Sans", 110)
        title = self.font.render("SUDOKU", 100, GREEN)
        self._window.blit(title, (170, 30))
        self.font = pygame.font.SysFont("Comic Sans", 30)
        b_text = self.font.render("CHECK", 100, WHITE)
        self._window.blit(b_text, (565, 80))
        #SECRET KEYS; key('p') will print current state of board, key('s') will print out solution to board
        self.font = pygame.font.SysFont("Comic Sans", 20)
        tab = self.font.render("TAB : Reset Game", 100, BLACK)
        self._window.blit(tab, (30, 5))
        enter = self.font.render("ENTER : Unclick", 100, BLACK)
        self._window.blit(enter, (30, 23))
        space = self.font.render("SPACE : Give Up", 100, BLACK)
        self._window.blit(space, (30, 41))
        delete = self.font.render("DELETE : Reset Slot", 100, BLACK)
        self._window.blit(delete, (30, 59))
        tup= self.font.render("UP : Increase number", 100, BLACK)
        self._window.blit(tup, (30, 77))
        tdown = self.font.render("Down : Decrease number", 100, BLACK)
        self._window.blit(tdown, (30, 95))
        numb = self.font.render("1-9 : Sets number", 100, BLACK)
        self._window.blit(numb, (30, 113))

        #draws numbers in board
        self.font = pygame.font.SysFont("Somic Sans MS", 50)

        for row in range(9):
            for col in range(9):

                #draws original numbers in BLACK to represent puzzle clues
                if self.original[row][col] != 0:
                    text = self.font.render(str(self.original[row][col]), 25, BLACK)
                    self._window.blit(text, (col*70+60, row*70+160))

                #draws based on color:  GREEN : if solved correctly  ,  BLUE : input numbers  ,  RED : if asked for solution
                if self.passed or self.solved:
                    color = GREEN if self.passed else RED
                    if self.original[row][col] == 0:
                        text = self.font.render(str(self.board.solution[row][col]), 25, color)
                        self._window.blit(text, (col*70+60, row*70+160))
                else:
                    scolor = BLUE
                    if self.clicked==(col,row):
                        scolor = LBLUE
                    if self.board[row][col] != 0 and self.original[row][col] == 0:
                        text = self.font.render(str(self.board[row][col]), 25, scolor)
                        self._window.blit(text, (col*70+60, row*70+160))

        display.update()


    def print_solution(self):
        """Print solution to board on terminal"""
        for row in self.board.solution:
            print(row)


    def print_board(self):
        """Print board on terminal"""
        print(self.board)


if __name__ == "__main__":
    #sets standards and window using pygame
    pygame.init()
    #sets window size, intial font, and window title
    screen = display.set_mode((WIDTH, HEIGHT))
    font = font.SysFont("Somic Sans MS", 30)
    display.set_caption('Sudoku')
    ### SETS GAME and STARTS
    main_game = Sudoku(screen, font)
