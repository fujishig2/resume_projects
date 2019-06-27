#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   L4Q1KF.py
#--------------------------------------------

#Purpose is to write a program using for loops that will count from 0
#to their number on a horizontal line. Then using an operator of their
#choosing, do that to the number they initially used for counting.


#gets the user to input a number greater than 1. If he doesn't get it right
#I used a while loop to loop until he puts in the right answer.
user_answer = int(input("Enter a number greater than 1: "))
while user_answer <= 0:
    user_answer = int(input("Too small! Try again: "))

#Prints numbers from 0 to users answer horizontally
print("\nCounting from 0 to", user_answer)
for i in range(0, user_answer+1):
    print(i, end="   ")

#Gets the user to input a math operation, and won't accept the answer until
#the right math operation is entered
math_operation = input("\n\nChoose a math operation (+, -, *): ")
while (math_operation != "+") and (math_operation != "-") and (math_operation != "*"):
    math_operation = input("Invalid input! Try again: ")

#prints a table of math operations using the users inputted number
#as well as the math operation they used
print("Table for", user_answer, "using " + math_operation + ":")
for i in range(1, user_answer+1):
    print (str(user_answer), math_operation, str(i), "=", eval(str(user_answer) + math_operation + str(i)))
