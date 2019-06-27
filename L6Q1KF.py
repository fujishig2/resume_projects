#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   L6Q1KF.py
#--------------------------------------------

#Purpose is to get a list of random grades, print them in rows of 4,
#count how often a user inputted number is found, append their input
#and count how many 2-digit values there are. All done using functions.

#Main function - Test all of the helper functions
def testGrades():
    grade_list = createGrades(11)
    printRows(grade_list)
    addGrade(grade_list)
    printRows(grade_list)
    print("\nAmount of 2-digit values =", countGrades(grade_list))
    
    
#creates a list whose size is equal to the amount inputted, comprised of
#random numbers from 0 to 100 qll converted into strings.
def createGrades(amount):
    import random
    class_list = []
    for i in range (amount):
        class_list.append(str(random.randint(0,100)))
    return class_list
    
    
#Prints out the list with 4 numbers on the same line, then goes to the next line
#and prints out the next 4 numbers. The last line may not have 4 numbers in it.
def printRows(grade_list):
    print()
    for i in range (1, len(grade_list)+1):
        if i % 4 == 0:
            print(grade_list[i-1])
        else:
            print(grade_list[i-1], end = "   ")
        
#Gets the user to input a number between 0 and 100, then counts
#how often that number occurs. Then it will add the number inputted
#to the end of the list.
def addGrade(grade_list):
    user_input = input("\n\nEnter a number between 0 and 100: ")
    count = 0
    for i in range(len(grade_list)):
        for j in range(len(grade_list[i])):
            if grade_list[i][j] == user_input:
                count = count + 1
        if grade_list[i] == user_input and len(grade_list[i]) > 1:
            count = count + 1
    print(user_input, "occurs", count, "times.")
    grade_list.append(user_input)

    
#Counts how many 2 digit numbers there are in the list.
def countGrades(grade_list):
    count = 0
    for i in range(len(grade_list)):
        if len(grade_list[i]) == 2:
            count = count + 1
    return count