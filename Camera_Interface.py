from SimpleCV import *


# Class which handles all interaction with the camera
class Camera_Interface():
    def __init__(self, resolution):
        # Creating camera object. SET THE RESOLUTION HERE
        self.cam = Camera(0, resolution)
        time.sleep(0.5)

    # Function to capture single frame
    def get_image(self):
        img = self.cam.getImage()
        # img = img.flipVertical()
        # img = img.flipHorizontal()
        return img
