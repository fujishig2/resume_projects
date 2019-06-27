#--------------------------------------------
# Name:      Demo file
# Program:   L7sorts.py
#--------------------------------------------
# Contains the 'Search for Largest', 'Selection sort', and 
# 'Insertion sort' functions students should use in the lab

my_list = [50, 60, 10, 40, 90, 20, 80, 70, 30]

def find_largest(a_list, n):
    max_position = 0
    for i in range(1, n):
        if a_list[i] > a_list[max_position]:
            max_position = i
    return max_position


def selection_sort(a_list):    
    n = len(a_list)
    for end in range(n, 1, -1):      # Each pass starts here
        
        # --- Search for Largest ---
        max_position = 0
        for i in range(1, end):
            if a_list[i] > a_list[max_position]:   # Perform comparison
                max_position = i        
        # --------------------------
        
        temp = a_list [end - 1]        # Perform exchange
        a_list [end - 1] = a_list [max_position]
        a_list [max_position] = temp        
    return a_list


def insertion_sort(a_list):
    n = len(a_list)
    for end in range(1, n):        # Each pass starts here
        new = a_list [end]
        ins_pt = end
        while (ins_pt > 0 and a_list [ins_pt-1] > new):
            a_list [ins_pt] = a_list [ins_pt - 1]
            ins_pt = ins_pt - 1
        a_list [ins_pt] = new
    return a_list
