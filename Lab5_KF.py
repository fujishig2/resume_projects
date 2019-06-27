#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   Lab5_KF.py
#--------------------------------------------

#this main window (win) never changes, including the reset button at the top right.
from graphics import *
win = GraphWin("Kyle Fujishige's house", 500,500)
win.setBackground(color_rgb(255,255,255))
reset = Rectangle(Point(400,10), Point(490, 50))
reset.setFill(color_rgb(255,0,0))
reset.draw(win)
text = Text(Point(445, 30), "Reset")
text.draw(win)

#Description:   Main function used to call the other functions. If called, the entire 
#               sequence will start over.
#Syntax:        main(win)
#Parameters:    win - the graphWin object wuth 500x500 dimensions called at the beginning
#Returns:       nothing
def main(win):
    try:
        #objects holds all the different things drawn, this is useful if the user wants to
        #restart the program.
        objects = []
        pt1 = get_pt(win, objects)
        objects.append(body_pt1(win, pt1))
        
        pt2 = get_pt(win, objects)
        objects.append(body_pt2(win, pt2))
        
        body = house_body(win, pt1, pt2)
        objects.append(body)
        
        entry = door(win, body[0], get_pt(win, objects))
        objects.append(entry)
        
        objects.append(window(win, entry[0], get_pt(win, objects)))
        
        objects.append(roof(win, body[0], get_pt(win, objects)))
        
        pt = get_pt(win, objects)
        win.close()
        
    except:
        None



#Description:   Waits for the user to click on a point. Then checks to see if the point was
#               on the restart button. If it is on the restart, everything gets erased, and main
#               is called again, restarting the sequence. If the user didn't click on the
#               restart button, then it returns the point clicked by the user.
#Syntax:        pt = get_pt(win,objects)
#Parameters:    win    - the graphWin object with 500x500 dimensions called at the beginning
#              objects - all the stored shapes and objects drawn
#Returns:       pt     - the mouse point location clicked by the user

def get_pt(win, objects):
    pt = win.getMouse()
    if pt.x >= 400 and pt.x < 490 and pt.y >= 10 and pt.y < 50 and objects != []:
        for elem in objects:
            for obj in elem:
                obj.undraw()
        main(win)
    elif pt.x >= 400 and pt.x < 490 and pt.y >= 10 and pt.y < 50 and objects == []:
        main(win)
    else: 
        return pt

#Description:   Mark a point with a red circle of 3 pixel radius, and label it as "1"
#Syntax:        objects.append(body_pt1(win, pt1))
#Parameters:    win    - the graphWin object with 500x500 dimensions called at the beginning
#               pt1    - the mouse point location clicked by the user
#Returns: [circle, text] - the circle child class used at location pt1 with a radius of 3 pixels
#                          and the text child class used to mark the circle with a "1" in a list
def body_pt1(win, pt1):
    circle = Circle(pt1, 3)
    circle.setFill(color_rgb(255,0,0))
    circle.draw(win)
    
    pt1_text = Point(pt1.x-10,pt1.y)
    text = Text(pt1_text, "1")
    text.draw(win)   
    return [circle, text]
    

#Description:   Mark a point with a red circle of 3 pixel radius, and label it as "2"
#Syntax:        objects.append(body_pt2(win, pt2))
#Parameters:    win    - the graphWin object wuth 500x500 dimensions called at the beginning
#               pt2    - the mouse point location clicked by the user
#Returns: [circle, text] - the circle child class used at location pt1 with a radius of 3 pixels
#                          and the text child class used to mark the circle with a "2" in a list
def body_pt2(win, pt2):
    circle = Circle(pt2, 3)
    circle.setFill(color_rgb(255,0,0))
    circle.draw(win)
    
    pt2_text = Point(pt2.x+10,pt2.y)
    text = Text(pt2_text, "2")
    text.draw(win)       
    return [circle, text]
    

#Description:   Make a rectangle with opposing corners starting at pt1 and ending at pt2
#Syntax:        body = house_body(win, pt1, pt2)
#Parameters:    win    - the graphWin object with 500x500 dimensions called at the beginning
#               pt1    - the mouse point location returned from get_pt(win, objects)
#               pt2    - the mouse point location returned from get_pt(win, objects)
#Returns:       [body]   - the rectangle child drawn starting from pt1 and ending at pt2 in a list
def house_body(win, pt1, pt2):
    body = Rectangle(pt1,pt2)
    body.draw(win)
    return [body]


#Description:   Make a door(rectangle) where the top is centered in the point clicked. 
#               The width of the door is 1/5 the size of the width of the house, 
#               and the length is from pt1 to the bottom of the house body.
#Syntax:        entry = door(win, body, pt1)
#Parameters:    win    - the graphWin object with 500x500 dimensions called at the beginning
#               pt1    - the mouse point location returned from get_pt(win, objects)
#               body   - the rectangle returned from house_body(win, pt1, pt2)
#Returns:      [entry, - the rectangle child drawn where the top is centered at pt1 and the width is 1/5 the
#                        size  of the width of the house, and the length is from pt1 to the bottom of the body
#              circle, - the circle child class used at location pt1 with a radius of 3 pixels
#               text]  - the text child class used to mark the circle with a "3"  
def door(win, body, pt1):
    #circle drawn:
    circle = Circle(pt1, 3)
    circle.setFill(color_rgb(255,0,0))
    circle.draw(win)
    
    #text drawn:
    pt1_text = Point(pt1.x,pt1.y-10)
    text = Text(pt1_text, "3")
    text.draw(win)    
    door_width = (body.getP2().x - body.getP1().x) // 5
    
    #if point 1 of the house body is further down than point 2, use point 1 as the base of the door.
    if body.getP1().y > body.getP2().y:
        pt2 = Point(pt1.x + door_width, body.getP1().y)
    #otherwise use point 2.
    else:
        pt2 = Point(pt1.x + door_width, body.getP2().y)
        
    #door drawn, and moved over to the left by half the size of the width.    
    entry = Rectangle(pt1, pt2)
    entry.move(-door_width//2, 0)
    entry.draw(win)
    return [entry, text, circle]


#Description:   Make a window(square) where the point clicked is the center of the window.
#               The width of the window must be half the width of the door
#Syntax:        objects.append(window(win, entry, pt))
#Parameters:    win    - the graphWin object with 500x500 dimensions called at the beginning
#               pt     - the mouse point location returned from get_pt(win, objects)
#               entry  - the rectangle returned from door(win, body, pt1)
#Returns:     [window, - the rectangle child drawn at the center of pt that is half the width of
#                        the door
#              circle, - the circle child class used at location pt with a radius of 3 pixels
#               text]  - the text child class used to mark the circle with a "4"
def window(win, entry, pt):
    #circle drawn:
    circle = Circle(pt, 3)
    circle.setFill(color_rgb(255,0,0))
    circle.draw(win)    
    
    #gets the distance from the center of the window to the edges by taking the 
    #absolute value of the doors width divided by 4.
    dimension = abs((entry.getP1().x - entry.getP2().x)//4)
    
    #now it just subtracts/adds the dimension from the point inputted to get the point in the centre
    #the window.
    pt1 = Point(pt.x - dimension, pt.y - dimension)
    pt2 = Point(pt.x + dimension, pt.y + dimension)
    
    #window drawn:
    window = Rectangle(pt1, pt2)
    window.draw(win)
    
    #text drawn:
    pt_text = Point(pt1.x + dimension, pt1.y - 10)
    text = Text(pt_text, "4")
    text.draw(win)
    return [window, circle, text]


#Description:   Make a roof(polygon) where the top left and right points of the houses body connect with
#               the point inputted.
#Syntax:        objects.append(window(win, body, pt))
#Parameters:    win    - the graphWin object with 500x500 dimensions called at the beginning
#               body   - the rectangle returned from house_body(win, pt1, pt2)
#               pt     - the mouse point location returned from get_pt(win, objects)
#Returns:      [roof,  - the polygon child drawn where the top left and right points of the body connect
#                        with the point inputted.
#              circle, - the circle child class used at location pt with a radius of 3 pixels
#               text]  - the text child class used to mark the circle with a "4"
def roof(win, body, pt):
    #circle drawn:
    circle = Circle(pt, 3)
    circle.setFill(color_rgb(255,0,0))
    circle.draw(win)        
    
    #text drawn:
    pt_text = Point(pt.x,pt.y-10)
    text = Text(pt_text, "5")
    text.draw(win)    
    
    #if the bodies first point height is greater than the 2nd, use 1st points y value for the polygon
    if body.getP1().y > body.getP2().y:
        y = body.getP2().y
    #else use the 2nd points y value for the polygon.
    else:
        y = body.getP1().y
        
    #roof drawn:
    point_list = [pt, Point(body.getP1().x, y), Point(body.getP2().x, y)] # different x values, same y value
    roof = Polygon(point_list)
    roof.draw(win)
    return [roof, circle, text]



main(win)