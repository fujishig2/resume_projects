#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   L11Q2bonusKF.py
#--------------------------------------------

#Purpose is to make a collage! Using a single image, play with them and put them
#into 4 different quadrents
from PIL import Image, ImageDraw
from PIL import ImageFont


#chnages the bottom half of an image to have 50% increased red. Returns the new image
def change_red(file_name):
    new_img = file_name
    draw = ImageDraw.Draw(new_img)
    for x in range(new_img.width):
        for y in range(int(new_img.height*0.5), new_img.height):
            r,g,b = new_img.getpixel((x,y))
            r = int(r*1.5)
            new_img.putpixel((x,y),(r,g,b))
    draw.text((int(new_img.width*0.15),int(new_img.height*0.15)), "Change red", (255,0,0))
    return new_img
    
#user has a choice to either zoom (1) or rotate (2) the image. Returns the new image
def zoom_or_rotate(file_name):
    choice = input("Enter (1) zoom or (2) rotate: ")
    if choice == "1":
        double_img = file_name.resize((int(file_name.width*2), int(file_name.height*2)))
        new_img = double_img.crop((int(file_name.width*0.5),int(file_name.height*0.5),int(file_name.width*1.5),int(file_name.height*1.5)))
        draw = ImageDraw.Draw(new_img)
        draw.text((int(new_img.width*0.15),int(new_img.height*0.15)), "Zoom", (255,0,255))
    elif choice == "2":
        new_img = file_name.transpose(Image.ROTATE_180)
        draw = ImageDraw.Draw(new_img)
        draw.text((int(new_img.width*0.15),int(new_img.height*0.15)), "Rotate", (255,0,255))
    return new_img
        
#takes 4 equal rectangles, and rearranges them from bottom-top. Returns the new image
def make_puzzle(file_name):
    top = file_name.crop((0,0,file_name.width,file_name.height//4))
    top_mid = file_name.crop((0,file_name.height//4,file_name.width,file_name.height//2))
    bottom_mid = file_name.crop((0,file_name.height//2,file_name.width,int(file_name.height*(3/4))))
    bottom = file_name.crop((0,int(file_name.height*(3/4)),file_name.width,file_name.height))
    new_img = Image.new("RGB", (file_name.size))
    new_img.paste(bottom, (0,0))
    new_img.paste(bottom_mid, (0,file_name.height//4))
    new_img.paste(top_mid, (0,file_name.height//2))
    new_img.paste(top, (0,int(file_name.height*(3/4))))
    draw = ImageDraw.Draw(new_img)
    draw.text((int(new_img.width*0.15),int(new_img.height*0.15)), "Puzzle", (0,0,255))
    return new_img


#bonus, makes a border that's 3 pixels wide on all 4 sides
def make_border(collage):
    for x in range (collage.width):
        for y in range (3):
            collage.putpixel((x,y),(255,0,0))
    
    for x in range (3):
        for y in range (collage.height):
            collage.putpixel((x,y),(255,0,0))
            
    for x in range (collage.width):
        for y in range (collage.height - 3, collage.height):
            collage.putpixel((x,y),(255,0,0))
    
    for x in range (collage.width - 3, collage.width):
        for y in range (collage.height):
            collage.putpixel((x,y),(255,0,0))


#main function that calls all the other functions. Then puts them all into
#4 different quadrents to create a collage. The top left will have
#the change red, top right will be either zoomed or rotated. Bottom
#left will have the puzzle, and the bottom right will be the original.
def make_collage(file_name):
    img = Image.open(file_name)
    top_left = change_red(img)
    img = Image.open(file_name)    
    top_right = zoom_or_rotate(img)
    img = Image.open(file_name)    
    bottom_left = make_puzzle(img)
    img = Image.open(file_name)    
    bottom_right = img
    draw = ImageDraw.Draw(bottom_right)
    draw.text((int(bottom_right.width*0.15),int(bottom_right.height*0.15)), "Original", (0,0,0))
    collage = Image.new("RGB", (int(img.width * 2), int(img.height * 2)))
    collage.paste(top_left, (0,0))
    collage.paste(top_right, (img.width, 0))
    collage.paste(bottom_left, (0, img.height))
    collage.paste(bottom_right, (img.width, img.height))
    draw = ImageDraw.Draw(collage)
    #had to open the arial font manually. Might need to be changed for you.
    font = ImageFont.truetype("C:\Windows\Fonts\Arial.ttf", 32)
    draw.text((int(collage.width * 0.35), int(collage.height*0.465)), "Kyle's Collage", (255,255,255), font)
    make_border(collage)
    
    
    collage.show()