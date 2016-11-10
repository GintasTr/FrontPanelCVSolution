from SimpleCV import *
from Image_Operations.Cropper import Cropper
from Image_Operations.Filter import Filter
from Image_Operations.Blob_Finder import Blob_Finder

class Parts_Identification():
    def __init__(self, coordinates):
        # Assign coordinates to a local oject variable
        self.coordinates = coordinates
        # Cropper object - used when cropping:
        self.cropper = Cropper(self.coordinates["TOPLEFT"], self.coordinates["BOTRIGHT"])
        # Filter object - used to apply filters and morphops to image
        self.filter = Filter()
        # Blob finder object - used to find the needed blobs in the image
        self.blob_finder = Blob_Finder()

    # Funtion to find the front panel in the image
    def find_panel(self, img, testing = False):
        # Crop the image to the location where panel should be placed, store cropped image if in testing mode
        img = self.cropper.placement_location_crop(img)
        if testing: img_cropped = img

        # Filter the image to find the panel in the cropped image, store the filtered image if in testing mode
        img = self.filter.image_confirmation_filter(img)
        if testing: img_filtered = img

        # Find the panel blob, which satisfies all of the requirements
        panel_blob = self.blob_finder.panel_blob(img)

        # Return the values. If testing - all of the tested ones.
        if testing: return {'crop': img_cropped, 'filter': img_filtered, 'blob': panel_blob}
        return panel_blob


    # Function to identify which button is present: "Clock" or "trapeze"
    def which_button(self, img, testing = False):

        # Find the front panel in the image and check if it was correctly found
        panel_location = self.find_panel(img)
        if panel_location == None: return "Error - front panel was not found"

        # Crop to the button edges and store cropped image if in testing mode
        img = self.cropper.relative_crop(img, panel_location, "button")
        if testing: img_cropped = img

        # Filter the image so that we have only white parts and store the filtered image if in testing mode
        img = self.filter.parts_identification_filter(img)
        if testing: img_filtered = img

        # Find the actual button we are interested in and return error if it was not found (and not testing mode)
        button_blob = self.blob_finder.button_blob(img)
        if (button_blob == None) and (not testing): return "Error - button was not found correctly"

        # Return values in testing mode
        if testing: return {'crop': img_cropped, 'filter': img_filtered, 'blob': button_blob}

        # Check the button similarity to circle. If less than 0.6 - its clock. If more - its trapeze
        if button_blob.circleDistance() <0.6:
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
    # select the testing mode from: "find_panel", "button"
    testing_mode = "button"

    # select the testing section from "cropping", "filtering", "blobbing"
    testing_section = "blobbing"

    # Setting the variables which usually come from the top
    PANEL_PLACEMENT_LOCATION = {"TOPLEFT": (290, 220),
                                "BOTRIGHT": (990, 600)}
    testing_thing = Parts_Identification(PANEL_PLACEMENT_LOCATION)
    cam = Camera(0, {"width": 1280, "height": 720})
    disp = Display((1548,768))

    while disp.isNotDone():
        img = cam.getImage()
        img.dl().rectangle2pts(PANEL_PLACEMENT_LOCATION["TOPLEFT"],
                               PANEL_PLACEMENT_LOCATION["BOTRIGHT"],
                               Color.RED, 5)

        if testing_mode == "find_panel": test_result = testing_thing.find_panel(img, True)
        elif testing_mode == "button": test_result = testing_thing.which_button(img, True)

        if type(test_result) == str: print "Str received, probably panel not found"; img.save(disp); continue

        cropped_image, filtered_image, found_blob = test_result['crop'],test_result['filter'],test_result['blob']

        if testing_section == "cropping": img = cropped_image
        elif testing_section == "filtering": img = img.sideBySide(filtered_image)
        elif testing_section == "blobbing":
            if found_blob:
                if found_blob.circleDistance() < 0.6: tmp_color = Color.GREEN
                else: tmp_color = Color.RED
                found_blob.draw(color=tmp_color, width=1, alpha=-1, layer=filtered_image.dl())
                # print "Biggest blob area is:", found_blob.area()
                # print "Biggest blob width is:", found_blob.width()
                # print "Biggest blob height is:", found_blob.height()
                print "Distance to circle is:", found_blob.circleDistance()
                # print found_blob.minX()
                img = filtered_image
        img.save(disp)

    # elif testing_mode == "something else":
    #     # to test WHICH_* and filters
    #     img =  cam.getImage()
    #     img1 = testing_thing.which_button(img, True)
    #     if (type(img1) == str):
    #         print img1
    #         img.save(disp)
    #     else:
    #         # # To test filter
    #         # img3 = img1[0].sideBySide(img1[1])
    #         # img3.save(disp)
    #
    #         # To test WHICH_* and blob finder
    #         img1.save(disp)