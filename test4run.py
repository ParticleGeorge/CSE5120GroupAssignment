import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random

mode = "player_vs_ai" # default mode for playing the game (player vs AI)

class RandomBoardTicTacToe:
    def __init__(self, size=(600, 600)):
        self.size = self.width, self.height = size
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (93, 214, 227)
        self.CIRCLE_COLOR = (227, 140, 93)
        self.CROSS_COLOR = (227, 140, 93)
        self.BUTTON_COLOR = (107, 237, 139)  # Color of the button
        self.BUTTON_HOVER_COLOR = (93, 207, 121)  # Color of the button when hovered
        # Grid Size
        self.GRID_SIZE = 4  
        self.OFFSET = 5
        self.TopMargin = 100
        self.SideMargin = 50
        self.MARGIN = 5

        # init the choice and symbol
        self.ai_choice = "minimax"  # Default AI algorithm
        self.ai_symbol = "O"  # Default AI plays as 'O'

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = (self.size[0] - self.SideMargin) / self.GRID_SIZE - self.OFFSET
        self.HEIGHT = (self.size[1] - self.TopMargin) / self.GRID_SIZE - self.OFFSET

        # Initialize pygame
        pygame.init()

        self.screen = pygame.display.set_mode(self.size)  # Initialize the display once
        pygame.display.set_caption("Tic Tac Toe")

        # Initialize scores will have to be linked to gamestatus place holder for now
        self.score_X = 0
        self.score_O = 0

        self.game_reset()  

    def draw_game(self):
        """ Draw the Tic Tac Toe grid and the current game state. """
        self.screen.fill(self.BLUE)  # Fill the background

        # Draw the grid
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                pygame.draw.rect(self.screen, self.WHITE, 
                                 (self.SideMargin + col * self.WIDTH, self.TopMargin + row * self.HEIGHT, 
                                  self.WIDTH, self.HEIGHT), 3)

        # Draw the circles and crosses for the board state using the provided code
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                if self.board[x][y] == 1:  # Circle (O)
                    self.draw_circle(x, y)
                elif self.board[x][y] == -1:  # Cross (X)
                    self.draw_cross(x, y)

        self.draw_start_button()
        self.draw_score_counter()
        self.draw_board_size_buttons()
        self.draw_player_symbol_X()
        self.draw_player_symbol_Y()

        pygame.display.update()

    def change_turn(self):

        if(self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")

    def draw_circle(self, x, y):
   
        center_x = self.SideMargin + y * (self.WIDTH + self.OFFSET) + self.WIDTH / 2
        center_y = self.TopMargin + x * (self.HEIGHT + self.OFFSET) + self.HEIGHT / 2
        radius = min(self.WIDTH, self.HEIGHT) / 2.5  # Radius scaled to fit inside the cell
        pygame.draw.circle(self.screen, self.CIRCLE_COLOR, (center_x, center_y), radius, 3)

    def draw_cross(self, x, y):
    
        start_x = self.SideMargin + y * (self.WIDTH + self.OFFSET)
        start_y = self.TopMargin + x * (self.HEIGHT + self.OFFSET)

    # Calculate the size of the cross relative to the cell size
        cross_size = min(self.WIDTH, self.HEIGHT) * 0.9  # 70% of the width/height to fit nicely inside the cell

    # Define the end points for the two lines of the cross
        end_x = start_x + cross_size
        end_y = start_y + cross_size

    # Draw two diagonal lines for the "X"
        pygame.draw.line(self.screen, self.CROSS_COLOR, (start_x, start_y), (end_x, end_y), 3)
        pygame.draw.line(self.screen, self.CROSS_COLOR, (start_x, end_y), (end_x, start_y), 3)

#
#
#check this and fix
#
#
#
    def is_game_over(self):

        """
        YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
        FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)
            
        YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME
        """
        # fixxxx
        if sum(row.count(0) for row in self.game_state.board_state) == self.GRID_SIZE ** 2:
            return 
        
        if not self.game_state.is_terminal():
            return 
        
        font = pygame.font.Font(None, 50)
        winner_text = f"Winner: {self.game_state.winner}"  
        text = font.render(winner_text, True, self.WHITE)  
        text_rect = text.get_rect(center=(self.size[0] // 2, self.size[1] // 2))  

        self.screen.fill(self.BLUE)  
        self.screen.blit(text, text_rect)  
        pygame.display.update()  

            

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)
    
    def play_ai(self):
        """
        YOUR CODE HERE TO CALL MINIMAX OR NEGAMAX DEPENDEING ON WHICH ALGORITHM SELECTED FROM THE GUI
        ONCE THE ALGORITHM RETURNS THE BEST MOVE TO BE SELECTED, YOU SHOULD DRAW THE NOUGHT (OR CIRCLE DEPENDING
        ON WHICH SYMBOL YOU SELECTED FOR THE AI PLAYER)
        
        THE RETURN VALUES FROM YOUR MINIMAX/NEGAMAX ALGORITHM SHOULD BE THE SCORE, MOVE WHERE SCORE IS AN INTEGER
        NUMBER AND MOVE IS AN X,Y LOCATION RETURNED BY THE AGENT
        """
       
        empty_cells = sum(x.count(0) for x in self.game_state.board_state)
      
        if empty_cells > 16:
            depth = 4  # Large boards with many empty cells
        else:
            depth = 6  # Increase depth as the board fills

        if self.ai_choice == 'minimax':
            eval_score, move = minimax(self.game_state, depth=depth, maximizingPlayer=(self.ai_symbol == 'O'))
        elif self.ai_choice == 'negamax':
            color = 1 if self.ai_symbol == 'O' else -1
            eval_score, move = negamax(self.game_state, depth=depth, color=color)
        else:
            raise ValueError("Invalid Choice.")
        
      

        if move is not None:
            x, y = move
            
            self.game_state.board_state[x][y] = 1 if self.ai_symbol == 'O' else -1
            if self.ai_symbol == 'O':
                self.draw_circle(x, y)
            else:
                self.draw_cross(x, y)
            if self.is_game_over():
                self.display_winner()
                pygame.time.wait(5000)
                self.game_reset()
            else:
                self.change_turn()
        else:
            print("No moves left!")
            


    def game_reset(self):
        """
        YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
        BOARD STATE
        """
        """ Initialize the game state. """
        self.board = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)] 
        self.turn_O = True  
        self.score_X = 0 
        self.score_O = 0  

        self.WIDTH = (self.size[0] - self.SideMargin) / self.GRID_SIZE - self.OFFSET
        self.HEIGHT = (self.size[1] - self.TopMargin) / self.GRID_SIZE - self.OFFSET

        if self.WIDTH < 50 or self.HEIGHT < 50:
            self.WIDTH = 50
            self.HEIGHT = 50

        # make sure state is init
        self.game_state = GameStatus(self.board, self.turn_O)
        
        self.draw_game()
        pygame.display.update()

    def draw_start_button(self):
        """ Draw the 'Start Game' button. """
        button_width = 100
        button_height = 25
        button_x = 450  
        button_y = 10  

        pygame.draw.rect(self.screen, self.BUTTON_COLOR, (button_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 25)
        text = font.render("Start Game", True, self.WHITE)
        text_rect = text.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
        self.screen.blit(text, text_rect)

    def draw_score_counter(self):
        """ Draw the score counter. """
        font = pygame.font.Font(None, 30)
        score_text = f"X: {self.score_X} | O: {self.score_O}"
        text = font.render(score_text, True, self.WHITE)
        text_rect = text.get_rect(topright=(self.size[0]-10, 45))  # Top-right corner with some padding
        self.screen.blit(text, text_rect)

    def draw_board_size_buttons(self):
        """ Draw buttons for selecting the grid size. """
        button_width = 70
        button_height = 30
        spacing = 10  
        button_x = 10
        button_y = 10  

        font = pygame.font.Font(None, 25)

        sizes = [3, 4, 5]  # Available grid sizes
        for size in sizes:
            if button_x <= pygame.mouse.get_pos()[0] <= button_x + button_width and button_y <= pygame.mouse.get_pos()[1] <= button_y + button_height:
                pygame.draw.rect(self.screen, self.BUTTON_HOVER_COLOR, (button_x, button_y, button_width, button_height))
                if pygame.mouse.get_pressed()[0]:  # Left mouse button click
                    self.change_grid_size(size)
            else:
                pygame.draw.rect(self.screen, self.BUTTON_COLOR, (button_x, button_y, button_width, button_height))

            text = font.render(f"{size}x{size}", True, self.WHITE)
            text_rect = text.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
            self.screen.blit(text, text_rect)
            button_x += button_width + spacing

    def change_grid_size(self, new_size):
        """ Change the grid size based on button click. """
        if new_size != self.GRID_SIZE:
            self.GRID_SIZE = new_size
            self.game_reset()  # Reset the game to apply the new grid size

    def draw_player_symbol_X(self):
        """ Draw the 'Play as X' button. """
        button_width = 100
        button_height = 25
        button_x = 10  
        button_y = 50

        pygame.draw.rect(self.screen, self.BUTTON_COLOR, (button_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 25)
        text = font.render("Play as X", True, self.WHITE)
        text_rect = text.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
        self.screen.blit(text, text_rect)

    def draw_player_symbol_Y(self):
        """ Draw the 'Play as Y' button. """
        button_width = 100
        button_height = 25
        button_x = 120  
        button_y = 50

        pygame.draw.rect(self.screen, self.BUTTON_COLOR, (button_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 25)
        text = font.render("Play as Y", True, self.WHITE)
        text_rect = text.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
        self.screen.blit(text, text_rect)

    def get_cell_at_pos(self, pos):
        """ Convert mouse position to grid cell. """
        x, y = pos
        row = int((y - self.TopMargin) // (self.HEIGHT + self.OFFSET))
        col = int((x - self.SideMargin) // (self.WIDTH + self.OFFSET))

        if row >= self.GRID_SIZE or col >= self.GRID_SIZE:
            return None  # Out of bounds

        return row, col

    def handle_click(self, pos):
        """ Handle a mouse click at the specified position. """
        row, col = self.get_cell_at_pos(pos)
        if row is not None and col is not None and self.board[row][col] == 0:
            if self.turn_O:
                self.board[row][col] = 1  # O's turn
            else:
                self.board[row][col] = -1  # X's turn
            self.turn_O = not self.turn_O  # Toggle turn
            self.draw_game()  # Redraw the game state
            self.play_ai() 

    def play_game(self):
        """ Main game loop. """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            pygame.display.update()
        
        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = RandomBoardTicTacToe()
    game.play_game()
