from linked_tree import LinkedTree
from gamestate import GameState     # Class to represent the element of our nodes.
import random
import os

# Author: Matt Ankerson
# Date: 2 September 2015
# This class represents the game tree for tic tac toe.

class TicTacToe(object):
    
    def __init__(self):
        self.game_tree = LinkedTree()               # game_tree is instance of a LinkedTree
        start_state = GameState()                   # Create an empty GameState for the root.
        self.game_tree.add_root(start_state)        # Add the root.
        self.position = self.game_tree.get_root()   # Keep track of our game's position in the tree
        self.populate_tree()                        # Populate the whole tree.
        self.game_over = False
        
    def populate_tree(self, node=None):
        '''Beginning with root, populate the whole tree with GameStates'''
        if node is None:
            node = self.game_tree.get_root()    # If node is None, make the root our starting point.
        for game_state in self.game_tree.element(node).direct_derivatives():    # get all possible game_states from this state.
            child = self.game_tree.add_child(node, game_state)    # Add the game state as a child to the node
            self.populate_tree(child)           # recur on the child returned.
            
    def computer_play(self):
        '''Select the best child to move to from the current position.'''
        eligible = []
        for child in self.game_tree.children(self.position):
            #***print('Possible Child:\n' + str(self.game_tree.element(child)))
            # Assess if it's a win for the computer, a loss, or just another move.
            score = self.game_tree.element(child).score()
            if score == 0:
                eligible.append(child)      # add to our list of eligible options.
                self.position = child
            elif score == 1:
                self.position = child       # Take the win.
                self.game_over = True
                break
        if self.game_over == False and len(eligible) > 0:     # If we had any eligible options.
            index = random.randint(0, len(eligible) - 1)
            self.position = eligible[index]  # randomly select an option.
        else:
            self.game_over = True               # The human won.
        
    def user_play(self, row, col):
        '''The user selects a spot'''
        new_gs = self.game_tree.element(self.position)  # Create a new GameState to accomodate the user's move.
        new_gs.board[row][col] = 'X'
        # Compare the new GameState with the possible GameStates. (children of the current position)
        found = False
        for child in self.game_tree.children(self.position):
            if self.game_tree.element(child) == new_gs:
                self.position = child
                found = True
                break
        if not found:
            raise LookupError('Not a valid play.')
        
if __name__ == '__main__':
    print('Tic Tac Toe')
    print('Building Game Tree...')
    game = TicTacToe()
    os.system('clear')
    
    # Game loop:
    while not game.game_over:
        print(game.game_tree.element(game.position))
        row = input('Which row? (eg. 2): ')
        col = input('Which col? (eg. 3): ')
        game.user_play(row, col)
        game.computer_play()
        #os.system('clear')
    print('Game Over.')
    
    
    
    
    
    
    
    