#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   Lab3_KF.py
#--------------------------------------------

# Purpose:      Function that takes in a snake case string, and returns a camel case converted string.
# Syntax:       string_variable = to_camel_case(snake_case)
# Parameters:   snake_case: A string made in snake case.
# Return:       camel_case: A string converted from snake case to camel case.

def to_camel_case(snake_case):
    #splits the string by the "_"'s into a list, temp_list, while omitting the "_"'s.
    temp_list = snake_case.split("_")
    
    #adds the first part of temp_list as is to a string variable, then adds every other part of the list with a capitalized first character.
    camel_case = temp_list[0]
    for elem in temp_list[1:]:
        camel_case += elem.title()
        
    return camel_case







# Purpose:      Function that takes in a camal case string, and returns a snake case converted string.
# Syntax:       string_variable = to_snake_case(camel_case)
# Parameters:   camel_case: A string made in camel case.
# Return:       snake_case: A string converted from camel case to snake case.

def to_snake_case(camel_case):
    start = 0
    temp_list = []
    
    
    #if there's a capital letter, temp_list appends from the variable start until the next capital character found in the loop, and lowercases the segment appended.
    for i in range(len(camel_case)):
        if camel_case[i].isupper():
            temp_list.append(camel_case[start:i].lower())
            start = i
            
    #since there's no capital letter at the end, the temporary list needs append from the last capital letter found until the end of the string, also lowercasing the segment appended.       
    lst.append(camel_case[start:len(camel_case)].lower())    
    
    #joins the temporary list by "_" into a new string variable.
    snake_case = "_".join(lst)
    
    return snake_case
    
    
    
    
    
    
    
    
# Purpose:      Function that takes in a message, and returns the same message after each alphabetical character has been randomly transformed to either capital or lower case, without affecting punctuations or numbers.
# Syntax:       string_variable = to_ransom_case(message)
# Parameters:   message:    A string of characters
# Return:       new_string:  A string of randomly cased alphabetical characters.
    
def to_ransom_case(message):
    import random
    new_string = ""
    
    #loops through every character. If the rand_case = 0, character will be lower, if rand_case = 1, character will be upper. It won't affect punctuation or numbers.
    for ch in message:
        rand_case = random.randint(0,1)
        if rand_case == 0:
            new_string += ch.lower()
        else:
            new_string += ch.upper()
            
    return new_string






# Purpose:      Function that obscures only the lowercase characters by adding 13 to their numerical ascii values. If it goes above the value of z(122), it will loop back around to a(97).
# Syntax:       string_variable = rot13(message)
# Parameters:   message:     A string of characters
# Return:       new_string: A string of the lowercase characters added by 13, and everything else untouched.

def rot13(message):
    new_string = ""
    
    for ch in message:
        
        #if the character is lowercase it'll add 13 to its current ascii value and save it in the variable digit.
        if ch.islower():
            digit = ord(ch) + 13
            
            #if the variable digit has a value higher than 122 after 13 is added, it'll subtract 26 from the current value in digit.
            if digit > 122:
                digit -= 26
                
            #adds the new character at ascii value digit.
            new_string += chr(digit)
            
        else:
            #The character will be added to the string as is, if it isn't lowercase.
            new_string += ch
            
    return new_string