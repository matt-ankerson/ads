from queue import Queue

# Author: Matt Ankerson
# Date: 29 August 2015

class Tree():
    # 'Abstract' base class representing a tree.
    
    def __init__(self):
        pass
        
    def get_root(self):
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
        
    def depth(self, node):
        # Return the number of levels separating the root from the given node.
        if self.is_root(node):
            return 0
        else:
            return 1 + self.depth(self.parent(node))
            
    def _height_at_node(self, node):
        # Return the height of the tree rooted at node.
        if self.is_leaf(node):
            return 0
        else:
            return 1 + max(self._height_at_node(c) for c in self.children(node))
            
    def height(self, node=None):
        # Return the height of the subtree rooted at the given node.
        if node is None:
            node = self.root()
        return self._height_at_index(node)
        
    def nodes(self):
        # Generate an iteration of all nodes in the tree.
        return self.preorder()
        
    def _subtree_preorder(self, node):
        # Generate a preorder iteration of positions rooted at the given node.
        yield node      # visit this node first.
        for child in self.children(node):
            for other in self._subtree_preorder(child):
                yield other
                
    def preorder(self):
        # Generate a preorder iteration of the nodes in the tree.
        if not self.is_empty():
            for node in self._subtree_preorder(self.root()):    # start recursion
                yield node
        
    def _subtree_postorder(self, node):
        # Generate a postorder iteration of all nodes rooted at the given node.
        for child in self.children(node):
            for other in self._subtree_postorder(child):
                yield other
        yield node      # visit node after all it's subtrees.
        
    def postorder(self):
        # Generate a postorder iteration of all nodes in the tree.
        if not self.is_empty():
            for node in self._subtree_postorder(self.root()):   # start recursion.
                yield node   
                
    def breadthfirst(self):
        # Generate a breadth first iteration of all nodes in the tree.
        if not self.is_empty():
            fringe = Queue()    # Known nodes not yet yielded.
            fringe.enqueue(self.root())     # start with the root.
            while not fringe.is_empty():
                node = fringe.dequeue()     # Remove node from start of the queue
                yield node                  # Return this node
                for child in self.children(node):
                    fringe.enqueue(child)   # Add children to the back of the queue
        
    def __iter__(self):
        # Generate an iteration of all the elements in the tree.
        for node in self.nodes():
            yield node['element']
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        