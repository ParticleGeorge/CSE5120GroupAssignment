# -*- coding: utf-8 -*-
import copy


class GameStatus:


	def __init__(self, board_state, turn_O):

		self.board_state = board_state
		self.turn_O = turn_O
		self.oldScores = 0

		self.winner = ""


	def is_terminal(self):
		"""
        YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
        THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
        """
		# check if someone has won
		scores = self.get_scores(terminal=True)
		if scores == float('inf'):
			self.winner = "O"
			# x wins
			return True  
		elif scores == float('-inf'):
			self.winner = "X"
			# o wins
			return True  

		# check if board is full 
		for row in self.board_state:
			if 0 in row:
				# game still on
				return False

		self.winner = "Draw"
		return True 


	def get_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        
        """        
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point = 3 if len(self.board_state) == 3 else 4
		
		# check rows
		for row in range(rows):
			for col in range(cols - check_point + 1):
				window = self.board_state[row][col:col + check_point]
				if all(cell == 1 for cell in window): 
					# max win
					return float('inf')  # Max win
				elif all(cell == -1 for cell in window):  
					# min win
					return float('-inf')  # Min win

		# check cols
		for col in range(cols):
			for row in range(rows - check_point + 1):
				window = [self.board_state[row + i][col] for i in range(check_point)]
				if all(cell == 1 for cell in window):
					return float('inf')
				elif all(cell == -1 for cell in window):
					return float('-inf')

		# check diag top left bot right
		for row in range(rows - check_point + 1):
			for col in range(cols - check_point + 1):
				window = [self.board_state[row + i][col + i] for i in range(check_point)]
				if all(cell == 1 for cell in window):
					return float('inf')
				elif all(cell == -1 for cell in window):
					return float('-inf')

		# Check diag bot left top right
		for row in range(check_point - 1, rows):
			for col in range(cols - check_point + 1):
				window = [self.board_state[row - i][col + i] for i in range(check_point)]
				if all(cell == 1 for cell in window):
					return float('inf')
				elif all(cell == -1 for cell in window):
					return float('-inf')

		# if scores + then x wins
		# if scores - then o wins
		return scores  # Positive = X wins, Negative = O wins, 0 = tie
	    

	def get_negamax_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point = 3 if terminal else 2

		# determine rows
		for row in range(rows):
			for col in range(cols - check_point + 1):
				window = self.board_state[row][col:col + check_point]
				if window == [1] * check_point:
					scores += 100  
				elif window == [-1] * check_point:
					scores -= 100  

		# determine cols
		for col in range(cols):
			for row in range(rows - check_point + 1):
				window = [self.board_state[row + i][col] for i in range(check_point)]
				if window == [1] * check_point:
					scores += 100
				elif window == [-1] * check_point:
					scores -= 100

		# diag top left bot right
		for row in range(rows - check_point + 1):
			for col in range(cols - check_point + 1):
				window = [self.board_state[row + i][col + i] for i in range(check_point)]
				if window == [1] * check_point:
					scores += 100
				elif window == [-1] * check_point:
					scores -= 100

		# # diag bot left top right
		for row in range(check_point - 1, rows):
			for col in range(cols - check_point + 1):
				window = [self.board_state[row - i][col + i] for i in range(check_point)]
				if window == [1] * check_point:
					scores += 100
				elif window == [-1] * check_point:
					scores -= 100

		return scores * (-1 if self.turn_O else 1)  



	def get_moves(self):
		moves = []  
		"""
        YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
        MINIMAX OR NEGAMAX FUNCTIONS
        """

		# loop through rows
		for i in range(len(self.board_state)):  
			# loop through cols
			for j in range(len(self.board_state[i])):  
				# is it empty?
				if self.board_state[i][j] == 0:  
					moves.append((i, j))  

		return moves 

	def get_new_state(self, move):
		new_board_state = copy.deepcopy(self.board_state)
		x, y = move

		symbol = 1 if self.turn_O else -1  
		new_board_state[x][y] = symbol  
		return GameStatus(new_board_state, not 	self.turn_O)
