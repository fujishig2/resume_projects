#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   projectKF.py
#--------------------------------------------


#Description:   Main function used as a menu, and to get user input.
#Syntax:        menu(IDs, shapes)
#Parameters:    IDs - the dictionary of the routes and their corresponding shape IDs.
#               shapes - the dictionary of the lat/long co-ords of the shape IDs.
#Returns:       nothing
def menu(IDs, shapes):
    print("""
    
    
    Edmonton Transit System
--------------------------------
(1) Load shape IDs from GTFS file
(2) Load shapes from GTFS file

(4) Print shape IDs for a route
(5) Print points for a shape ID

(0) Quit
""")
    user_input = user_command()
    if user_input == "1":
        IDs = load_IDs()
        menu(IDs, shapes)
        
    elif user_input == "2":
        shapes = load_shapes()
        menu(IDs, shapes)
        
    elif user_input == "3":
        menu(IDs, shapes)
        
    elif user_input == "4":
        print_IDs(IDs)
        menu(IDs, shapes)   
        
    elif user_input == "5":
        print_shapes(shapes)
        menu(IDs, shapes)        
        
    elif user_input == "6":
        menu(IDs, shapes)
        
    elif user_input == "7":
        menu(IDs, shapes)  
        
    elif user_input == "8":
        menu(IDs, shapes)    
        
    elif user_input == "9":
        menu(IDs, shapes)            
        
    else:
        return

    
#Description:   Gets the user to input a value, and error checks it until it is a digit
#               and within the values of 0-9.
#Syntax:        user_input = user_command()
#Parameters:    nothing
#Returns:       user_input the users input that's been error checked.
def user_command():
    user_input = input("Enter command: ")
    while not user_input.isnumeric() or int(user_input) > 9 or int(user_input) < 0:
        user_input = input("Invalid command, enter a new command: ")
    return user_input

#Description:   Asks a user to input a file name. If blank, default is data/trips.txt.
#               It then loads the route numbers and their corresponding shape IDs
#               into a dictionary of sets.
#Syntax:        IDs = load_IDs()
#Parameters:    nothing
#Returns:       IDs - the dictionary of the routes and their corresponding shape IDs.
def load_IDs():
    try:
        filepath = input("Enter a file name [data/trips.txt]: ")
        if filepath == "":
            filepath = "data/trips.txt"
        trips_file = open(filepath)
        
        #the first line in the file is just the description, thus I omit it from the dictionary IDs.
        line = trips_file.readline()
        line = trips_file.readline()
        IDs = {}
        while line != "":
            temp = line.split(",")
            #creates a new key that is the corresponding route if the key doesn't exist
            if temp[0] not in IDs:
                IDs[temp[0]] = set([temp[-1].strip()])
            #if the key exists, it just adds the shape ID to the keys values of sets.
            else:
                IDs[temp[0]].add(temp[-1].strip())
            line = trips_file.readline()
        trips_file.close()
        return IDs
        
    except:
        print("\nCannot open file")
        return {}
    
    

#Description:   Asks a user to input a file name. If blank, default is data/shapes.txt.
#               It then loads the shape IDs and their corresponding lat/long co-ords
#               into a dictionary of sets.
#Syntax:        shapes = load_shapes()
#Parameters:    nothing
#Returns:       shapes - the dictionary of the lat/long co-ords of the shape IDs. 
def load_shapes():
    try:
        filepath = input("Enter a file name [data/shapes.txt]: ")
        if filepath == "":
            filepath = "data/shapes.txt"
        shape_file = open(filepath)
        
        #the first line in the file is just the description, thus I omit it from the dictionary shapes.
        line = shape_file.readline()
        line = shape_file.readline()
        shapes = {}
        while line != "":
            temp = line.strip().split(",")
            #creates a new key that is the corresponding shape ID if the key doesn't exist
            if temp[0] not in shapes:
                shapes[temp[0]] = [(float(temp[1]),float(temp[2]))]
            #if the key exists, it just adds the lat/long tuple to the keys values of tuples    
            else:
                shapes[temp[0]] += [(float(temp[1]),float(temp[2]))]
            line = shape_file.readline()
        shape_file.close()
        return shapes
    
    except:
        print("\nCannot open file")
        return {}
    
    
#Description:   Asks a user to input a route #. If it doesn't work, it will display an
#               error message without breaking the program. If it does work, it displays
#               all the corresponding shape values corresponding to the route # (key).
#Syntax:        print_IDs(IDs)
#Parameters:    IDs - the dictionary of the routes and their corresponding shape IDs.
#Returns:       Nothing  
def print_IDs(IDs):
    try:
        user_input = input("Route? ")
        print("\nShape IDs for " + user_input + ":")
        for elem in IDs[user_input]:
            print("\t", elem)
                
    except:
        print("\nInvalid option!")
        
        
#Description:   Asks a user to input a shape ID. If it doesn't work, it will display an
#               error message without breaking the program. If it does work, it displays
#               all the corresponding lat/long co-ords corresponding to the shape ID (key).
#Syntax:        print_shapes(shapes)
#Parameters:    shapes - the dictionary of the lat/long co-ords of the shape IDs.
#Returns:       Nothing          
def print_shapes(shapes):
    try:
        user_input = input("Shape ID? ")
        print("\nShape for " + user_input+":")
        for elem in shapes[user_input]:
            print("\t", elem)
            
    except:
        print("\nInvalid option!")
        

menu({},{})