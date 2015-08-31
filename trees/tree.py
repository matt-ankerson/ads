# Author: Matt Ankerson
# Date: 29 August 2015

class Tree():
    # 'Abstract' base class representing a tree.
    
    def __init__(self):
        pass
        
    def root(self):
        # Return the root node of this tree.
        raise NotImplementedError('Must be implemented by subclass.')
        
    def is_root(self, node):
        # Return true if 'node' repreesents the root of the tree.
        return self.root() == node
        
    def parent(self, node):
        # Return the parent of the given node.
        raise NotImplementedError('Must be implemented by subclass.')
        
    def num_children(self, node):
        # Return the number of children that node has.
        raise NotImplementedError('Must be implemented by subclass.')
        
    def children(self, node):
        # Generate an iteration of nodes representing node's children
        raise NotImplementedError('Must be implemented by subclass.')
        
    def is_leaf(self, node):
        # Return true if the given node does not have any children
        return self.num_children(node) == 0
        
    def __len__(self):
        # Return total number of elements in tree
        raise NotImplementedError('Must be implemented by subclass.')
        
    def is_empty(self):
        # Return true if the tree is empty.
        return len(self) == 0