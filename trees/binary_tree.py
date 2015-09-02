from tree import Tree

# Author: Matt Ankerson
# Date: 29 August 2015
# This class represents an array based binary tree.
# node = { 'index': 0, 'element': None }

class BinaryTree(Tree):
    
    def __init__(self):
        Tree.__init__(self)
        self._n_nodes = 0
        self._nodes = []    # _nodes is a list of dictionaries.
        
    def _create_node(self, e, index):
        # Create a node dictionary with the input and return it.
        return {'index': index, 'element': e }
    
    def root(self):
        # Return the root node of this tree.
        return self._nodes[0]
        
    def parent(self, node):
        # Return the parent of the given node.
        if node['index'] == self.root():  # If this is the parent:
            return None
        else:
            parent_index = (node['index'] - 1) / 2
            return self._nodes[parent_index]
        
    def num_children(self, node):
        # Return the number of children that node has.
        count = 0
        for child in self.children(node):
            count += 1
        return count
        
    def children(self, node):
        # Generate an iteration of nodes representing node's children
        if self.left(node) is not None:
            yield self.left(node)
        if self.right(node) is not None:
            yield self.right(node)
        
    def __len__(self):
        # Return total number of nodes in tree
        return self._n_nodes
        
    def left(self, node):
        # Return the node that represents the left child of the 
        # given node. Return None if no left child.
        left_index = (node['index'] * 2) + 1    # will throw indexerror if greater than size of array
        if left_index >= self.__len__():
            return None
        else:
            return self._nodes[left_index]
        
    def right(self, node):
        # Return the node that represents the right child of the
        # given node. Return None if no right child.
        right_index = (node['index'] * 2) + 2   # will throw indexerror if greater than size of array
        if right_index >= self.__len__():
            return None
        else:
            return self._nodes[right_node]
        
    def sibling(self, node):
        # Return the node that represents the sibling of the 
        # given node. Return None if no sibling.
        parent = self.parent(node)
        if parent is None:      # node must be the root (has no parent)
            return None
        else:
            if node == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)
                
    def add_root(self, e):
        # Create root for an empty tree. Error occurs if the tree is non empty.
        # Return the newly created node.
        if self.__len__() > 0:
            raise Exception('Tree is non empty')
        else:
            self._nodes[0] = self._create_node(0, e)
        
    def add_left(self, node, e):
        # Create a new node for storing element e as the left child of the given node.
        # Return the resulting new node.
        # An error occurs if the node already has a left child.
        if self.left(node) is not None:
            raise Exception('Node already has left child.')
        else:
            new_index = (node['index'] * 2) + 1
            new_node = self._create_node(e, new_index)
            self._nodes[new_index] = new_node
            return new_node
        
    def add_right(self, node, e):
        # Create a new node for storing element e as the right child of the given node.
        # Return the resulting new node.
        # An error occurs if the node already has a right child.
        if self.right(node) is not None:
            raise Exception('Node already has right child.')
        else:
            new_index = (node['index'] * 2) + 2
            new_node = self._create_node(e, new_index)
            self._nodes[new_index] = new_node
            return new_node
        
    def replace(self, node, e):
        # Replace the element stored in the given node with element e, and return the 
        # previously stored element.
        old_element = node['element']
        self._nodes[node['index']]['element'] = e
        return old_element
        
    def delete(self, node):
        # Remove the given node, replace it with it's child (if any).
        # Return the element that was held by the old node.
        # An error occurs if the node has two children.
        pass
        
    def attach(self, node, t1, t2):
        # Attach the structure of trees t1 and t2 as the left and right subtrees
        # of the given node, respectively.
        # Reset t1 and t2 to empty trees. 
        # An error occurs if the given node is not a leaf.
        pass