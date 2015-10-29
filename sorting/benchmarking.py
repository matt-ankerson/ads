import random


def merge(s1, s2, s):
    '''Sub routine for merge sort algorithm.'''
    i = j = 0
    while i + j < len(s):
        if j == len(s2) or (i < len(s1) and s1[i] < s2[j]):
            s[i + j] = s1[i]    # Copy ith element of s1 as next element of s.
            i += 1
        else:
            s[i + j] = s2[j]    # Copy jth element of s2 as next element of s.
            j += 1


def merge_sort(s):
    '''Sort the elements of a python list using merge sort.'''
    n = len(s)
    if n < 2:
        return  # List is already sorted, this is our base case.
    # Divide
    mid = n // 2
    s1 = s[0:mid]
    s2 = s[mid:n]
    # Conquer
    merge_sort(s1)
    merge_sort(s2)
    # Merge results
    merge(s1, s2, s)    # Merge sorted halves back into s.


def quick_sort_inplace(s, a, b):
    '''Sort the list from s[a] to s[b] inclusive'''
    if a >= b:
        return                  # range is trivially sorted
    pivot = s[b]                # last element of range is pivot
    left = a                    # will scan rightward
    right = b - 1               # will scan leftward
    while left <= right:
        # scan until reacjing value >= pivot (or right marker)
        while left <= right and s[left] < pivot:
            left += 1
        # scan until reaching value <= pivot (or left marker)
        while left <= right and pivot < s[right]:
            right -= 1
        if left <= right:       # scans did not strictly cross
            s[left], s[right] = s[right], s[left]   # swap values
            left, right = left + 1, right - 1       # shrink range
    # put pivot into its final place, currently marked by left index.
    s[left], s[b] = s[b], s[left]
    # make recursive calls
    quick_sort_inplace(s, a, left - 1)
    quick_sort_inplace(s, left + 1, b)


def quick_sort(s):
    quick_sort_inplace(s, 0, len(s) - 1)


def partial_shuffle(arr, shuffle_size):
    '''Shuffles small sections of a sorted list.'''
    for i in xrange(0, len(arr) - 1, shuffle_size):
        if i + shuffle_size >= len(arr):
            shuffle_size = (len(arr) - 1)
        if i % shuffle_size == 0:
            for j in xrange(i, i + shuffle_size):
                # Pick random element to swap in this small section.
                k = random.randint(i, (i + shuffle_size) - 1)
                temp = arr[k]
                arr[k] = arr[j]
                arr[j] = temp
