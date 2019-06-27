#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   Lab2_KF.py
#--------------------------------------------

# Purpose:      Print the indices starting from 20 up to 32 by units of 3
# Syntax:       part_a()
# Parameters:   None
# Return:       None
def part_a():
    for i in range(20,35,3):
        print(i)

# Purpose:      Print the indices starting from 7 down to -1 by units of -2
# Syntax:       part_b()
# Parameters:   None
# Return:       None
def part_b():
    for i in range(7,-3,-2):
        print(i)
        
#Purpose:      Asks the user to enter 5 integers, calculates and prints the average of those 
#              numbers, and then prints the numbers entered that are greater than the average
#Syntax:       calculate_average()
#Parameters:   None
#Return:       None
def calculate_average():
    user_list = []
    overall = 0
    for i in range(5):
        user_list.append(int(input("Please enter an integer: ")))
        overall+=user_list[i]
    average = overall/len(user_list)
    print("\nThe average is:", average)
    print("The numbers greater than the average are:")
    for elem in user_list:
        if average < elem:
            print(elem, end = "   ")
            
#Purpose:      Takes an alphabetic string and prints out the number of times each letter
#              (uppercase or lowercase) is in the string
# Syntax:      letter_counter(string)
# Parameters:  string:  A string of only alphabetic characters
# Return:      None
def letter_counter(string):
    values = []
    for char in string:
        if values.count(char.lower()) == 0:
            count = string.lower().count(char.lower())
            values.append(char.lower())
            print("The letter", char, "is in", string, count, "time(s)")
        