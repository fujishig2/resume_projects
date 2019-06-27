#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   L10Q1KF.py
#--------------------------------------------

#Using PIL play with the bird.jpg image by swapping green and red,
#reducing the blue by 50%, and change the left half of the screen to grey

from PIL import Image 

#swapping the green and red of every single pixel
def swap_GR(picture):
    width,height = picture.size
    for x in range(width):
        for y in range(height):
            r,g,b = picture.getpixel((x,y))
            temp = r
            r = g
            g = temp
            picture.putpixel((x,y), (r,g,b))

#reduces the blue in every pixel by the amount inputted divided by 100
#(as a percentage)
def change_blue(picture, amount):
    width,height = picture.size
    for x in range(width):
        for y in range(height):
            r,g,b = picture.getpixel((x,y))
            b = int(b * (amount/100))
            picture.putpixel((x,y),(r,g,b))
            
#Makes the left half of the picture grey
def greyscale(picture):
    width,height = picture.size
    for x in range(width//2):
        for y in range(height):
            r,g,b = picture.getpixel((x,y))
            avg = (r+g+b)//3
            picture.putpixel((x,y),(avg,avg,avg))
            
            

#Opens the file path of bird.jpg, then calls all the other functions
#shows the final result after all the helper functions have been called
def color_picture():
    path=r'C:\Users\User\Downloads\bird.jpg'
    img = Image.open(path)
    swap_GR(img)
    change_blue(img, 50)    
    greyscale(img)
    img.show()