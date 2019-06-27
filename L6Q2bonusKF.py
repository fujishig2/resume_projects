#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   L6Q2bonusKF.py
#--------------------------------------------


#Purpose: Error check a users input to ensure they put in a numerical
#7 digit phone number. Swap out the first and last digits of the 
#phone number, and then add dashes to make it look like a phone number.
#Then spell the phone number out.


#Main function - Test all of the helper functions
def makePhoneNums():
    original = getNumber()
    phone_num = fixPhoneNum(original)
    printPhoneNums(original, phone_num)
    printWordForm(phone_num)


#Prompts the user for a 7 digit number, and error checks it until
#the user inputs a 7 digit number.
def getNumber():
    user_input = input("Please enter a 7-digit number: ")
    while not user_input.isdigit() or len(user_input) != 7:
        user_input = input("Error! Try again: ")
    return user_input


#rearranges the first and last numbers the user inputted, adds 780 to the
#front of the phone number, and adds hyphens to make it look like a 
#phone number. Returns a string.
def fixPhoneNum(original):
    num_list = list(original)
    temp = num_list[-1]
    num_list[-1] = num_list[0]
    num_list[0] = temp
    num_list.insert(0, "780")
    for i in range(1,7,4):
        num_list.insert(i, "-")
    return "".join(num_list)
    
    
#Prints out the original phone number, and the brand new phone number
def printPhoneNums(original, phone_num):
    print("\n"+ original + "\n" + phone_num)
    
    
#Turns the numerical number into the typed out words of each number.
def printWordForm(phone_num):
    phone_list = list(phone_num)
    words = ['zero ', 'one ', 'two ', 'three ', 'four ', 'five ', 'six ', 'seven ', 'eight ', 'nine ']
    word_form = ""
    for i in range(len(phone_list)):
        if phone_list[i].isdigit():
            word_form = word_form + words[int(phone_list[i])]
        else:
            word_form = word_form + "- "
    print(word_form)