import time
import random
from binary_search_treemap import TreeMap
from avl_treemap import AVLTreeMap
from splay_tree_map import SplayTreeMap

# Test the construction times of three different map implementations:
#   - Normal binary search tree
#   - AVL Tree
#   - Splay Tree

# Get a list of numbers
keys = range(0, 5000)
random.shuffle(keys)
# These will be our keys, use 0 for every value.

# Construction:

start = time.time()
binary_tree = TreeMap()
for key in keys:
    binary_tree[key] = 0
end = time.time()
print "Binary Search Tree construction took: " + str((end - start))

start = time.time()
avl_tree = AVLTreeMap()
for key in keys:
    avl_tree[key] = 0
end = time.time()
print "AVL Tree construction took: " + str((end - start))

start = time.time()
splay_tree = SplayTreeMap()
for key in keys:
    splay_tree[key] = 0
end = time.time()
print "Splay Tree construction took: " + str((end - start))

# shuffle keys again
random.shuffle(keys)

# Deconstruction:

start = time.time()
for key in keys:
    pos = binary_tree.find_position(key)
    binary_tree.delete(pos)
end = time.time()
print 'Binary Search Tree deconstruction took: ' + str((end - start))

start = time.time()
for key in keys:
    pos = avl_tree.find_position(key)
    avl_tree.delete(pos)
end = time.time()
print 'AVL Tree deconstruction took: ' + str((end - start))

start = time.time()
for key in keys:
    # pos = splay_tree.find_position(key)
    # splay_tree.delete(pos)
    del splay_tree[key]
end = time.time()
print 'Splay Tree deconstruction took: ' + str((end - start))
