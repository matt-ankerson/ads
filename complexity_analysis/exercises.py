# find the 10 largest elements in a sequence of size 'n'
def find_top_ten(list):
    dup_list = list[:]  # copy the list, so we don't destroy the original
    largest_ten = []
    for i in range(10):
        new_max = max(dup_list)
        largest_ten.append(new_max)
        dup_list.remove(new_max)
    return largest_ten
    
# find the missing integer in the given list of unique integers
def missing_int(list):
    n_elements = (len(list) + 1)
    for i in range(0, n_elements):
        if i not in list:
            return i