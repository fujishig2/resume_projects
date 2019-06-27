#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   L7Q3KF.py
#--------------------------------------------

# Using the sorting function found in sorts.py, modify it so it sorts
# a list of numbers from largest to smallest. Count how many times it 
# performs an exchange and a comparison. List each pass and each runs
# comparisons and exchanges as well.

def selection_sort_rev(a_list):    
    print("\nOriginal list:", a_list)
    n = len(a_list)
    pass_count = 0
    total_comp = 0
    total_exs = 0
    for end in range(n, 1, -1):      # Each pass starts here
        comparisons = 0
        exchanges = 0                
        # --- Search for Smallest ---
        max_position = 0
        for i in range(1, end):
            comparisons += 1 
            if a_list[i] < a_list[max_position]:   # Perform comparison
                max_position = i        
        # --------------------------
        
    
        temp = a_list [end - 1] # Perform exchange
        exchanges += 1
        a_list [end - 1] = a_list [max_position]
        a_list [max_position] = temp
        
        pass_count += 1 
        total_comp += comparisons
        total_exs += exchanges
        print("\nPass", pass_count, ": Comparisons:", comparisons, "\t Exchanges:", exchanges)
        print("\t", a_list)
    print("\n\tTotal Comparisons:", total_comp, "\tTotal Exchanges:", total_exs)