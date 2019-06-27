#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   L7bonusKF.py
#--------------------------------------------

def find_duplicates(my_list, num):
    count = 0
    for i in range(len(my_list)):
        if my_list[i] == num:
            count += 1
    print(num, "Occurred", count, "times.")