# function that takes a list of unsorted integers and returns the maximum value
def find_max(list):
    if len(list) == 1:  # base case
        return list[0]
    if list[0] < list[1]:   # if first element is smaller than the second
        list2 = list[1:]    # copy the list with first element removed
    else:
        list2 = [list[0]] + list[2:]    # keep the first element, append all from 3rd element to the tail.
    return find_max(list2)  # call function again, eventual result will propagate up
    
# function that takes a string representation of an integer, returns in integer form
def str_to_int(string):
    int_equivs = {'0': 0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9}
    if len(string) == 1:            # base case
        return int_equivs[string]
    else:
        return str_to_int(string[-1]) + (str_to_int(string[:-1]) * 10)