import sys

def inspect_list_sizing(n):
    data = []
    prev_size = 0
    for k in range(n):
        length = len(data)
        actual_size = sys.getsizeof(data)
        if actual_size != prev_size:
            print('Length: {0:3d}; Size in bytes: {1:4d}'.format(length, actual_size))
            prev_size = actual_size
        data.append(None)
        
inspect_list_sizing(200)