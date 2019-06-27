#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   L10bonusKF.py
#--------------------------------------------

#main function that asks for height and width, then creates a shape
#of number signs with the same width as inputted, and a + sign with
#the same width halfway inbetween the number signs
def draw_shape():
    width = int(input("Please enter the shape width: "))
    height = int(input("Please enter the shape height: "))
    for y in range(height+1):
        for x in range(width):
            if y == height//2:
                print("+", end = "")
            else:
                print("#", end = "")
        print()