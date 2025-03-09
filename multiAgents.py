from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
	terminal = game_state.is_terminal()
	if (depth==0) or (terminal):
		newScores = game_state.get_scores(terminal)
		return newScores, None

	"""
    YOUR CODE HERE TO FIRST CHECK WHICH PLAYER HAS CALLED THIS FUNCTION (MAXIMIZING OR MINIMIZING PLAYER)
    YOU SHOULD THEN IMPLEMENT MINIMAX WITH ALPHA-BETA PRUNING AND RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE
    
    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    """
	# this algorithm will be for decision making where MAX is human and MIN is AI
	# first we will store the best move forward
	best_move = None
    
    # now determine if MAX called or if MIN called
	# first if MAX
	if maximizingPlayer:
		# determine lowest score    
		value = float('-inf')
		
        # determine all possible moves
		for move in game_state.get_moves():
			# get new game move and use recursion for minimax to decrease depth
			newState = game_state.get_new_state(move)
			currentScore, _ = minimax(newState, depth - 1, False, alpha, beta)
			
            # check current score and see if it is better and update move
			if currentScore > value:
				value = currentScore
				best_move = move
				
            # now we do alpha beta pruning
			alpha = max(alpha, value)
			if beta <= alpha:
				# we break so that no more time if wasted
				break
	# now we check for MIN with else
	else: 
		# this is pretty much exactly the same with some minor changes
		# determine highest score    
		value = float('inf')
		
        # determine all possible moves
		for move in game_state.get_moves():
			# get new game move and use recursion for minimax to decrease depth
			newState = game_state.get_new_state(move)
			# change to true to switch player for recursive call
			currentScore, _ = minimax(newState, depth - 1, True, alpha, beta)
			
            # check current score and see if it is better and update move
			# check lower now 
			if currentScore < value:
				value = currentScore
				best_move = move
				
            # now we do alpha beta pruning
			# this time we are doing it for beta and min
			beta = min(beta, value)
			if beta <= alpha:
				# we break so that no more time if wasted
				break
			
	return value, best_move

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
	terminal = game_status.is_terminal()
	if (depth==0) or (terminal):
		scores = game_status.get_negamax_scores(terminal)
		return scores, None

	"""
    YOUR CODE HERE TO CALL NEGAMAX FUNCTION. REMEMBER THE RETURN OF THE NEGAMAX SHOULD BE THE OPPOSITE OF THE CALLING
    PLAYER WHICH CAN BE DONE USING -NEGAMAX(). THE REST OF YOUR CODE SHOULD BE THE SAME AS MINIMAX FUNCTION.
    YOU ALSO DO NOT NEED TO TRACK WHICH PLAYER HAS CALLED THE FUNCTION AND SHOULD NOT CHECK IF THE CURRENT MOVE
    IS FOR MINIMAX PLAYER OR NEGAMAX PLAYER
    RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE
    
    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    
    """
	availableMoves = [] #Create list of available moves to store

	
	for i in range(len(game_state.board_state)): #Loop through each row of the board
		for j in range(len(game_state.board_state[i])): #Loop through each column of the i row
			if game_state.board_state[i][j] == 0: # If space is "empty" (0), then available move
				availableMoves.append((i,j)) #Add empty space to list
	value = alpha
	best_move = None

	
	for space in availableMoves: #Loop through the list
		new_game_status = game_state.get_new_state(space) #Obtain new game state after making move
		neg_value, nega_move = negamax(new_game_status, depth - 1, -turn_multiplier, -beta, -alpha) #Utilize negamax algorithm to find best move

		if -nega_value > value: #Update value and best move if better move is found
			value = -nega_value
			best_move = space

		alpha = max(alpha, value) #Update alpha with max value

		if alpha >= beta: #Stop searching if alpha is greater then or equal to beta
			break
	
    	#return value, best_move
	return value, best_move
