class GameState(object):
        
    def __init__(self):
        # The GameState class has a 2d array to represent the board.
        # Thea agreed format is: [ row0, row1, row2 ]
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
            
    def direct_derivatives(self):
        # Yield an iteration of all possible direct game states that could
        # be derived from the board held by this instance. (return GameState objects)
        player = self.determine_turn()
        # return an iterator of all possible positions.
        return self._possible_positions(player)
            
    def _possible_positions(self, player):
        '''Generate an iteration of each possible next gamestate'''
        if self.score() == 0:                       # If this is not a leaf:
            board_cp = self.board                   # Copy the main board
            for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    if board_cp[r][c] == '-':      # the player could go here.
                        board_cp[r][c] = player
                        new_gs = GameState()
                        new_gs.board = board_cp
                        yield new_gs
                        board_cp[r][c] = '-'
            
    def determine_turn(self): 
        # Find out who's turn it is.
        Os = 0
        Xs = 0
        for row in self.board:
            for col in row:
                if col == 'X':
                    Xs += 1
                elif col == 'O':
                    Os += 1
        if Xs > Os:
            return 'O'
        else:
            return 'X'   # if even, X will be returned. This is the behaviour we want.
            
    def score(self):
        # Compute and return a value (0, 1, or 2) to indicate if this board is unfinished,
        #   a win, or a loss. (respectively)
        state = self._three_in_a_line()
        if state == '-':
            return 0    # unfinished
        elif state == 'O':
            return 1    # win
        elif state == 'X':
            return 2    # loss  
        else:
            raise ValueError('Invalid return type.')          
            
    def _three_in_a_line(self):
        # Assess whether or not somebody has won.
        for row in self.board:  # check all the rows
            if all(x == row[0] for x in row):
                return row[0]
        for k in range(len(self.board)): # now check all the cols
            col = [row[k] for row in self.board]
            if all(x == col[0] for x in col):
                return col[0]
        # now check the diagonals
        diag1 = [row[i] for i, row in enumerate(self.board)]
        if all(x == diag1[0] for x in diag1):
            return diag1[0]
        diag2 = [row[-i - 1] for i, row in enumerate(self.board)]
        if all(x == diag2[0] for x in diag2):
            return diag2[0]
        return '-'   # if nothing was returned already, this is not a finished game.
        
    def __eq__(self, other):
        return self.board == other.board
        
    def __repr__(self):
        line = '    0    1    2\n'
        line += '0 ' + str(self.board[0]) + '\n'
        line += '1 ' + str(self.board[1]) + '\n'
        line += '2 ' + str(self.board[2]) + '\n'
        return line