#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   L11Q1KF.py
#--------------------------------------------

#Purpose: using PIL and its helper functions, create a picture

from PIL import Image, ImageDraw


#when called, this function will draw the background of the image, the ground, and a road
def draw_background(img):
    #draws the sky
    for x in range (img.width):
        for y in range (int(img.height*0.75)):
            img.putpixel((x,y),(0,0,50))    
            
    #draws the grass       
    for x in range (img.width):
        for y in range (int(img.height*0.75), img.height):
            img.putpixel((x,y),(0,125,0))  
            
    #draws the grey road       
    for x in range(img.width):
        for y in range(int(img.height*0.77), int(img.height*0.9)):
            img.putpixel((x,y),(50,50,50))
    
    #draws the lines in the road
    for x in range(int(img.width*0.1),(int(img.width*0.3))):
        for y in range(int(img.height*0.815), int(img.height*0.848)):
            img.putpixel((x,y),(255,255,255))  
    for x in range(int(img.width*0.4),(int(img.width*0.6))):
        for y in range(int(img.height*0.815), int(img.height*0.848)):
            img.putpixel((x,y),(255,255,255))
    for x in range(int(img.width*0.7),(int(img.width*0.9))):
        for y in range(int(img.height*0.815), int(img.height*0.848)):
            img.putpixel((x,y),(255,255,255))       
            
            
            
            
#When called, this function will draw a mountain with a snow capped peak
def draw_mountain(img):
    draw = ImageDraw.Draw(img)
    
    #draws a large green mountain
    draw.polygon([(int(img.width*0.1),int(img.height*0.749)),(int(img.width*0.9),int(img.height*0.749)), (int(img.width * 0.5), int(img.height * 0.1))], (0,100,0), (0,0,50))
    
    #draws the snow on the peak, covering the top of the large green mountain
    draw.polygon([(int(img.width* 0.379),int(img.height*0.3)),(int(img.width*0.622),int(img.height*0.3)),(int(img.width* 0.5), int(img.height*0.1))], (255,255,255), (0,0,50))
            
            
            
#When called, this function will draw a moon in the upper left area of the image            
def draw_moon(img):
    draw = ImageDraw.Draw(img)
    draw.ellipse([(int(img.width*0.1),int(img.height*0.1)),(int(img.width*0.22),int(img.height*0.22))], (255,255,255),(0,0,50))
    
    
    
    
    
#When called, this function will draw the wheels of the car    
def draw_wheels(img):
    draw = ImageDraw.Draw(img)
    #left wheel
    draw.ellipse([(int(img.width*0.35),int(img.height*0.7)),(int(img.width*0.45),int(img.height*0.8))], (0,0,0),(50,50,50))   
    
    #right wheel
    draw.ellipse([(int(img.width*0.65),int(img.height*0.7)),(int(img.width*0.75),int(img.height*0.8))], (0,0,0),(50,50,50))
    
    
    
    
    
#When called this function will draw the body of the car, the head and
#tail lights, the windows, and some fancy body lines
def draw_body(img):
    draw = ImageDraw.Draw(img)   
    #draws the windshield
    draw.ellipse([(int(img.width*0.385),int(img.height*0.54)),(int(img.width*0.5),int(img.height*0.7))], (0,0,0),(0,100,0))
    
    #draws the taillight
    draw.ellipse([(int(img.width*0.7),int(img.height*0.62)),(int(img.width*0.82),int(img.height*0.7))], (250,0,0),(0,100,0))
    
    #draws the headlight
    draw.ellipse([(int(img.width*0.28),int(img.height*0.62)),(int(img.width*0.4),int(img.height*0.7))], (200,200,0),(0,100,0))
    
    #draws the bottom part of the body, covering parts of the head and tailights, as well as the windshield
    for x in range (int(img.width*0.3), int(img.width*0.8)):
        for y in range (int(img.height*0.62), int(img.height*0.7)):
            img.putpixel((x,y),(200,0,0))
    
    #draws 2 fancy lines down the body        
    draw.line([(int(img.width*0.3),int(img.height*0.64)), (int(img.width*0.8),int(img.height*0.64))], (0,0,0), 2)
    draw.line([(int(img.width*0.3),int(img.height*0.675)), (int(img.width*0.8),int(img.height*0.675))], (0,0,0), 2)
    
    #draws the upper part of the body, covering part of the circle drawn for
    #the windshield
    for x in range (int(img.width*0.42), int(img.width*0.68)):
        for y in range (int(img.height*0.53), int(img.height*0.62)):
            img.putpixel((x,y),(200,0,0))    
    
    #draws the side windows
    for x in range (int(img.width*0.45), int(img.width*0.65)):
        for y in range (int(img.height*0.55), int(img.height*0.62)):
            img.putpixel((x,y),(0,0,0))    
            
    #seperates the side windows        
    draw.line([(int(img.width*0.55),int(img.height*0.55)), (int(img.width*0.55),int(img.height*0.62))], (200,0,0), 4)
            
    
#when called, this function draws the title located near the bottom of the screen            
def draw_title(img):
    draw = ImageDraw.Draw(img)
    draw.text((int(img.width*0.05),int(img.height*0.95)), "Night time driving through the mountains", (0,0,0))
    

#Helper function that calls all of the other functions, as well as creates the
#image. Since everything is drawn by percentages, you can easily change
#the dimensions of the image, and still produce the same image.
def draw_picture():
    img = Image.new("RGB",(500,500))
    draw_background(img)
    draw_mountain(img)
    draw_moon(img)
    draw_wheels(img)
    draw_body(img)
    draw_title(img)
    img.show()