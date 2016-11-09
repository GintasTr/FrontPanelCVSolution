from SimpleCV import *


# Class which handles all interaction with the display
class Display_Interface():
    def __init__(self, resolution):
        # Creating display object. SET THE RESOLUTION HERE
        self.disp = Display((resolution["width"], resolution["height"]))

    # Function to show image briefly
    def show_image_briefly(self, img):
        self.disp.checkEvents()
        # Show the image on Display
        img.save(self.disp)


    # Function to show image briefly and detect the key pressed
    def show_briefly_till_n(self, img):
        # Check if any button was pressed
        self.disp.checkEvents()
        # Show image on Display
        img.save(self.disp)                # Show the image on Display
        # Get the key which was pressed
        pressed = pg.key.get_pressed()
        # If N was pressed, then return False. Otherwise - True
        if (pressed[pg.K_n] == 1):         # If n pressed
            return False
        return True

    # Function to show image briefly and detect the mouse clicks
    def show_briefly_till_mouse(self, img):
        # Check if any button was pressed
        self.disp.checkEvents()
        # Show image on Display
        img.save(self.disp)                 # Show the image on Display
        # If mouse left was pressed
        if self.disp.mouseLeft:
            return "Left"
        if self.disp.mouseRight:
            return "Right"
        else:
            return "None"