from SimpleCV import *
from Image_Operations.Cropper import Cropper
from Image_Operations.Filter import Filter
from Image_Operations.Blob_Finder import Blob_Finder
import time

class Parts_Identification():
    def __init__(self, coordinates):
        # CALIBRATION DATA TO DETERMINE CORRECT FILTERS VALUES
        # Assign coordinates to a local oject variable
        self.coordinates = coordinates
        # Cropper object - used when cropping:
        self.cropper = Cropper(self.coordinates["TOPLEFT"], self.coordinates["BOTRIGHT"])
        # Filter object - used to apply filters and morphops to image
        self.filter = Filter()
        # Blob finder object - used to find the needed blobs in the image
        self.blob_finder = Blob_Finder()
        # Panel size limits for confirmation:
        self.MINIMUM_PANEL_SIZE, self.MAXIMUM_PANEL_SIZE = 134000, 143000

        # Panel edges limits for confirmation:
        self.MINIMUM_WIDTH, self.MAXIMUM_WIDTH = 600, 650
        self.MINIMUM_HEIGHT, self.MAXIMUM_HEIGHT = 200, 250

    # Funtion to find the front panel in the image
    def find_panel(self, img, testing = False):
        # Crop the image to the location where panel should be placed
        img = self.cropper.placement_location_crop(img)
        # Filter the image to be able to find the panel in the cropped image
        img = self.filter.image_confirmation_filter(img)
        # Find all of the blobs in the image which satisfy the size requirements
        all_blobs = img.findBlobs(minsize = self.MINIMUM_PANEL_SIZE, maxsize = self.MAXIMUM_PANEL_SIZE)
        # If none of the blobs were found, return that image is not good
        if all_blobs == None:
            return None
        # If any of the blobs were found, get only ones which are not on the edge
        all_blobs = all_blobs.notOnImageEdge()
        # If none of the blobs were found, return that image is not good
        if len(all_blobs) == 0:
            return None
        # Check whether biggest one(representing panel) passes the dimension requirements
        biggest_blob = all_blobs.sortArea()[-1]
        if self.MINIMUM_WIDTH < biggest_blob.width() < self.MAXIMUM_WIDTH and \
            self.MINIMUM_HEIGHT < biggest_blob.height() < self.MAXIMUM_HEIGHT:

            # DEBUGGING AND CALIBRATION
            if testing:
                all_blobs.draw()
                biggest_blob.draw(color=Color.RED, width=5, alpha=-1, layer=img.dl())
                print "Biggest blob area is:", biggest_blob.area()
                print "Biggest blob width is:", biggest_blob.width()
                print "Biggest blob height is:", biggest_blob.height()
                print "Biggest blob coordinates are:", biggest_blob.coordinates()
                return img


            return biggest_blob
        else:
            return None


    # Function to identify which button is present: "Clock" or "trapeze"
    def which_button(self, img, testing = False):
        # Find the front panel in the image
        panel_location = self.find_panel(img)
        # Check if it was correctly found
        if panel_location == None: return "Error - front panel was not found"
        # Crop to the button edges
        img = self.cropper.relative_crop(img, panel_location, "button")
        # Filter the image so that we have only white parts
        img1 = self.filter.parts_identification_filter(img)
        # When testing cropper of filters
        # if testing:
        #     # To test cropper:
        #     #return img
        #     # To test filters:
        #     return (img, img1)
        # Clear testing variable, for simplicity
        img = img1
        # # When testing main blob finding
        if testing:
            img1 = self.blob_finder.button_blob(img, True)
        # Find the actual button we are interested in
        button_blob = self.blob_finder.button_blob(img)
        # Return error if main button blob was not found
        if button_blob == None: return "Error - button was not found correctly"
        # When testing main blob_circle distance
        if testing:
            print "Circle distance is:", button_blob.circleDistance()
            return img1
        # Check the button similarity to circle. If less than 0.35 - its clock. If more - its trapeze
        if button_blob.circleDistance() <0.35:
            return 'clock'
        else:
            return 'trapeze'



    # Function to identify which temperature is present: "celsius" or "fahrenheit"
    def which_temperature(self, img):
        None


# Function to identify which controller is present: "figures" or "squares"
    def which_controller(self, img):
        None




if __name__ == '__main__':
    PANEL_PLACEMENT_LOCATION = {"TOPLEFT": (290, 220),
                                "BOTRIGHT": (990, 600)}
    testing_thing = Parts_Identification(PANEL_PLACEMENT_LOCATION)
    cam = Camera(0, {"width": 1280, "height": 720})
    disp = Display((1548,768))

    while disp.isNotDone():

        # # to test FIND_PANEL
        # img =  cam.getImage()
        # img.dl().rectangle2pts(PANEL_PLACEMENT_LOCATION["TOPLEFT"],
        #                        PANEL_PLACEMENT_LOCATION["BOTRIGHT"],
        #                        Color.RED, 5)
        # img1 = testing_thing.find_panel(img, True)
        # if img1 == None:
        #     img.save(disp)
        # else:
        #     img1.save(disp)
        #     #img2 = img.sideBySide(img1)
        #     #img2.save(disp)

        # to test WHICH_* and filters
        img =  cam.getImage()
        img1 = testing_thing.which_button(img, True)
        if (type(img1) == str):
            print img1
            img.save(disp)
        else:
            # # To test filter
            # img3 = img1[0].sideBySide(img1[1])
            # img3.save(disp)

            # To test WHICH_* and blob finder
            img1.save(disp)
