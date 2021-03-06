from SimpleCV import *

# Class which crops all of the required locations from the images
class Cropper():
    def __init__(self, panel_coordinates_topleft, panel_coordinates_botright):
        # Localise variables
        self.panel_coordinates_topleft = panel_coordinates_topleft
        self.panel_coordinates_botright = panel_coordinates_botright


    # Crop the square area to check whether panel is in it
    def placement_location_crop(self, img):
        img = img.crop(self.panel_coordinates_topleft, self.panel_coordinates_botright)
        return img


    # Crop for the specific feature
    def relative_crop(self, img, panel_blob, case):
        # Relative cropping values for button:
        BUTTON_LOCATION = ((41,129),(74,200))
        TEMPERATURE_LOCATION = ((208,265),(239,314))
        CONTROLLER_LOCATION = ((310,70),(340,125))

        if case == "button":
            relative_location = BUTTON_LOCATION
        elif case == "temperature":
            relative_location = TEMPERATURE_LOCATION
        elif case == "controller":
            relative_location = CONTROLLER_LOCATION
        else:
            return "ERROR - should not have reached relative cropping else"

        # Crop the image around the required given field
        img = self.placement_location_crop(img)

        # Crop the image around the main panel blob
        img = img.crop(panel_blob.topLeftCorner(),
                       panel_blob.bottomRightCorner())

        # Calculating actual pixel values required for cropping
        cropping_top_left = (panel_blob.width() * relative_location[0][0]/400,
                             panel_blob.height() * relative_location[0][1]/400)
        cropping_bot_rigth = (panel_blob.width() * relative_location[1][0] / 400,
                              panel_blob.height() * relative_location[1][1] / 400)
        # Cropping around the required relative location
        img = img.crop(cropping_top_left,cropping_bot_rigth)
        return img


if __name__ == '__main__':
    panel_coordinates_topleft = (290, 220)
    panel_coordinates_botright = (990, 600)
    PANEL_PLACEMENT_LOCATION = {"TOPLEFT": (290, 220), "BOTRIGHT": (990, 600)}
    testing_cropper = Cropper(panel_coordinates_topleft, panel_coordinates_botright)

    cam = Camera(0, {"width": 1280, "height": 720})
    disp = Display((1280,720))

    while disp.isNotDone():
        img =  cam.getImage()
        img = testing_cropper.placement_location_crop(img)
        # Use Parts identification to test relative crop
        img.save(disp)
