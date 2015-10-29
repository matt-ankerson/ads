import benchmarking
import random
import time
# This file runs a series of benchmarking tests on implementations of
# merge sort and quick sort to determine which one is superior.

n_values = 100000

# ------------------------
# Merge sort a list of random values
values = range(n_values)
random.shuffle(values)
start = time.time()
benchmarking.merge_sort(values)
end = time.time()
print 'Merge sorting random values took ' + \
    str(end - start)

# Merge sort a list of partially sorted numbers
values = range(n_values)
benchmarking.partial_shuffle(values, 10)
start = time.time()
benchmarking.merge_sort(values)
end = time.time()
print 'Merge sorting almost sorted values took ' + \
    str(end - start)

# ------------------------
# Quick sort a list of random values
values = range(n_values)
random.shuffle(values)
start = time.time()
benchmarking.quick_sort(values)
end = time.time()
print 'Quick sorting random values took ' + str(end - start)

# Quick sort a list of partially sorted numbers
values = range(n_values)
benchmarking.partial_shuffle(values, 10)
start = time.time()
benchmarking.quick_sort(values)
end = time.time()
print 'Quick sorting almost sorted values took ' + str(end - start)
