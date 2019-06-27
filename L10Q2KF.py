#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   L10Q2KF.py
#--------------------------------------------

#Using PIL create a blank image and put 3 stripes in it.

from PIL import Image

#first stripe will set 40% of the height to a gradual increase in red
def first_stripe(img):
    width,height = img.size
    for x in range (width):
        for y in range(int(height * 0.4)):
            img.putpixel((x,y), (x,0,0))
            
#second stripe will set 40-60% of the height bright green
def second_stripe(img):
    width,height = img.size
    for x in range(width):
        for y in range((int(height * 0.4)), (int(height * 0.6))):
            img.putpixel((x,y), (0,255,0))
            
            
#third stripe will fill the last 40% and have a gradual decrease from 
#bright blue to black
def third_stripe(img):
    width,height = img.size
    for x in range(width):
        for y in range((int(height*0.6)), height):
            img.putpixel((x,y), (0,0,255-x))
            
            
#helper function that will create a blank image with a users inputted height
#It will then call all the other functions to change the blank picture
#depending on what function.
def draw_stripes():
    height = int(input("Please enter the overall height: "))
    img = Image.new("RGB",(256,height))
    first_stripe(img)
    second_stripe(img)
    third_stripe(img)
    img.show()