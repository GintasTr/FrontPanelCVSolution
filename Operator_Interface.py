from SimpleCV import *
from Display_Interface import Display_Interface
from Camera_Interface import Camera_Interface
from Display_Painter import Display_Painter
from Parts_Identification import Parts_Identification

# Class which communicates with operator
class Operator_Interface():
    def __init__(self, PANEL_PLACEMENT_LOCATION):
        # Localise the PANEL_PLACEMENT_LOCATION:
        self.PANEL_PLACEMENT_LOCATION = PANEL_PLACEMENT_LOCATION
        # Resolution of camera and display
        self.RESOLUTION = {"width": 1280, "height": 720}
        # Camera interface - to get the images
        self.cam = Camera_Interface(self.RESOLUTION)
        # Display interface - to show images on display
        self.disp = Display_Interface(self.RESOLUTION)
        # Painter interface - to draw on the images as required
        self.painter = Display_Painter()
        # Parts identifier interface - to determine if image taken includes the part
        self.parts_identification = Parts_Identification(self.PANEL_PLACEMENT_LOCATION)


    # Function which acquires the required image from the camera
    def get_required_image(self):
        # Initialise the request image: True - first request, False - scan again
        which_request = True
        while True:
            # Capture the image
            img = self.cam.get_image()
            # Show it with the request to put it in the correct location
            img_shown = self.painter.start_request_image(img, self.PANEL_PLACEMENT_LOCATION, which_request)
            # Check if mouse left was clicked on the image
            if self.disp.show_briefly_till_mouse(img_shown)[0] == "L":
                # Check if obtained image is correct by checking if something was returned
                if self.parts_identification.find_panel(img):
                    return img
                # If that image was not correct change the displayed request
                else:
                    which_request = False
            if self.disp.show_briefly_till_mouse(img)[0] == "R":
                return "ERROR - stopped by user"


if __name__ == '__main__':
    PANEL_PLACEMENT_LOCATION = {"TOPLEFT": (290, 220), "BOTRIGHT": (990, 600)}
    op_int = Operator_Interface(PANEL_PLACEMENT_LOCATION)
    print op_int.get_required_image()
