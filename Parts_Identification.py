from SimpleCV import *
from Image_Operations.Cropper import Cropper
from Image_Operations.Filter import Filter
from Image_Operations.Blob_Finder import Blob_Finder

class Parts_Identification():
    def __init__(self, coordinates_panel):
        # Assign coordinates_panel to a local oject variable
        self.coordinates_panel = coordinates_panel
        # Cropper object - used when cropping:
        self.cropper = Cropper(self.coordinates_panel["TOPLEFT"], self.coordinates_panel["BOTRIGHT"])
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
        img = self.filter.button_identification_filter(img)
        if testing: img_filtered = img

        # Find the actual button we are interested in and return error if it was not found (and not testing mode)
        button_blob = self.blob_finder.button_blob(img)
        if (button_blob == None) and (not testing): return "Error - button was not found correctly"

        # Return values in testing mode
        if testing: return {'crop': img_cropped, 'filter': img_filtered, 'blob': button_blob}

        # Check the button symbol perimeter. If less than 80 - its clock. If more - its trapeze
        if button_blob.perimeter() < 80:
            return 'clock'
        else:
            return 'trapeze'


    # Function to identify which temperature is present: "celsius" or "fahrenheit"
    def which_temperature(self, img, testing = False):

        # Find the front panel in the image and check if it was correctly found
        panel_location = self.find_panel(img)
        if panel_location == None: return "Error - front panel was not found"

        # Crop to the 64/18 number edges (including blue thing) and store cropped image if in testing mode
        img = self.cropper.relative_crop(img, panel_location, "temperature")
        if testing: img_cropped = img

        # Filter the image so that we have only white parts and store the filtered image if in testing mode
        img = self.filter.temperature_filter(img)
        if testing: img_filtered = img

        # Find temperature blob that we are interested in and return error if it was not found (and not testing mode)
        temperature_blob = self.blob_finder.temperature_blob(img)
        if (temperature_blob == None) and (not testing): return "Error - temperature scale was not found correctly"

        # Return values in testing mode
        if testing: return {'crop': img_cropped, 'filter': img_filtered, 'blob': temperature_blob}

        # Check the scale numbers blob width. If less than 12 - its 18 (celsius). If more - its 64 (fahrenheit)
        if temperature_blob.width() < 12: return 'celsius'
        else: return 'fahrenheit'


# Function to identify which controller is present: "figures" or "squares"
    def which_controller(self, img, testing = False):

        # Find the front panel in the image and check if it was correctly found
        panel_location = self.find_panel(img)
        if panel_location == None: return "Error - front panel was not found"

        # Crop to the location at the top of the controller knob and store cropped image if in testing mode
        img = self.cropper.relative_crop(img, panel_location, "controller")
        if testing: img_cropped = img

        # Filter the image so that we have only white parts and store the filtered image if in testing mode
        img = self.filter.controller_filter(img)
        if testing: img_filtered = img

        # Find controller blob that we are interested in and return error if it was not found (and not testing mode)
        controller_blob = self.blob_finder.controller_blob(img)
        if (controller_blob == None) and (not testing): return "Error - temperature scale was not found correctly"

        # Return values in testing mode
        if testing: return {'crop': img_cropped, 'filter': img_filtered, 'blob': controller_blob}

        # Check the scale numbers blob width. If less than 12 - its 18 (celsius). If more - its 64 (fahrenheit)
        if controller_blob.area() < 40: return 'figures'
        else: return 'squares'




if __name__ == '__main__':
    # select the testing mode from: "find_panel", "button", "temperature", "controller"
    testing_mode = "find_panel"

    # select the testing section from "cropping", "filtering", "blobbing"
    testing_section = "blobbing"

    # Setting the variables which usually come from the top
    PANEL_PLACEMENT_LOCATION = {"TOPLEFT": (290, 220),
                                "BOTRIGHT": (990, 600)}
    testing_thing = Parts_Identification(PANEL_PLACEMENT_LOCATION)
    cam = Camera(0, {"width": 1280, "height": 720})
    disp = Display((1700,720))

    while disp.isNotDone():
        img = cam.getImage()
        img.dl().rectangle2pts(PANEL_PLACEMENT_LOCATION["TOPLEFT"],
                               PANEL_PLACEMENT_LOCATION["BOTRIGHT"],
                               Color.RED, 5)

        if testing_mode == "find_panel": test_result = testing_thing.find_panel(img, True)
        elif testing_mode == "button": test_result = testing_thing.which_button(img, True)
        elif testing_mode == "temperature": test_result = testing_thing.which_temperature(img, True)
        elif testing_mode == "controller": test_result = testing_thing.which_controller(img, True)

        if type(test_result) == str: print "Str received, probably panel not found"; img.save(disp); continue

        cropped_image, filtered_image, found_blob = test_result['crop'],test_result['filter'],test_result['blob']

        if testing_section == "cropping": img = cropped_image
        elif testing_section == "filtering": img = filtered_image
        elif testing_section == "blobbing":
            if found_blob:

                # if found_blob.circleDistance() < 0.6: tmp_color = Color.GREEN
                # if found_blob.perimeter() < 80: tmp_color = Color.GREEN
                if found_blob.width() < 12: tmp_color = Color.GREEN
                # if found_blob.area() < 40: tmp_color = Color.GREEN
                else: tmp_color = Color.RED

                found_blob.draw(color=tmp_color, width=1, alpha=-1, layer=filtered_image.dl())
                # print "Biggest blob area is:", found_blob.area()
                # print "Biggest blob width is:", found_blob.width()
                # print "Biggest blob height is:", found_blob.height()
                # print "Distance to circle is:", found_blob.circleDistance()
                # print found_blob.minX()
                print "Blob perimeter is:", found_blob.perimeter()
                img = filtered_image
            else: print "Blob was not found"
        img.save(disp)