from tree import Tree

# Author: Matt Ankerson
# Date: 2 Sepetember 2015
# This class represents a linked tree, supporting an arbitrary number of children.
# node = { 'parent': ref, 'children': [], 'element': ref }

class LinkedTree(Tree):
    
    def __init__(self):
        Tree.__init__(self)
        self.root = None        # Set up the tree with no root
        self._n_nodes = 0
        
    def _create_node(self, parent, children, element):
        return { 'parent': parent, 'children': children, 'element': element }
        
    def add_root(self, element):
        self.root = self._create_node(None, [], element)
        
    def root(self):
        # Return the root node of this tree.
        return self.root
        
    def parent(self, node):
        # Return the parent of the given node.
        return node['parent']
        
    def num_children(self, node):
        # Return the number of children that node has.
        len(node['children'])
        
    def children(self, node):
        # Generate an iteration of nodes representing node's children
        for c in node['children']:
            yield c
            
    def add_child(self, node, element):
        # Add a child node to the given node, using the element also given.
        # Return the newly created node
        child = self._create_node(node, [], element)
        node['children'].append(child)
        return child
        
    def replace(self, node, new_element):
        # replace the element in the given node, return the old element.
        old_element = node['element']
        node['element'] = new_element
        return old_element
        
    def __len__(self):
        # Return total number of elements in tree
        return self._n_nodes

