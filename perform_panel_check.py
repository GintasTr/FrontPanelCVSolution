from sys import argv
from SimpleCV import *
# LOTS OF IMPORTS AND CONFIGS
from Parts_Handler import Parts_Handler
from Operator_Interface import Operator_Interface


# Cropping (and drawing a square) location:
PANEL_PLACEMENT_LOCATION = {"TOPLEFT": (290,220), "BOTRIGHT": (990,600)}

# Object to acquire data from operator
operator_interface = Operator_Interface(PANEL_PLACEMENT_LOCATION)

# Object to handle all actions with the part comparison
parts_handler = Parts_Handler(PANEL_PLACEMENT_LOCATION)





# MAIN SOFTWARE LOOP
def perform_panel_check():
    # Pass the parameters list to the parts handler to identify the required parts
    # and store it for later comparison
    # Returns string in format of either "ERROR - of some kind" or "SUCCESS"
    required_parts = parts_handler.parts_required(argv)

    # Check if it returned error and terminate if so. #TODO: Replace with try/catch
    if type(required_parts) == str:
        if required_parts[0] == "E":
            print required_parts
            return required_parts

    # Get the testing image
    img = operator_interface.get_required_image()
    # Check if it returned error and terminate if so.
    if type(img) == str:
        if img[0] == "E":
            print img
            return img


    # Identify which parts are mounted currently
    parts_present = parts_handler.parts_present(img)
    # # Check if it returned error and terminate if so.
    if type(parts_present) == str:
        if parts_present[0] == "E":
            print parts_present
            return parts_present

    # Compare the present parts with required parts
    # test_result = Parts_Handler.compare_parts(required_parts, parts_present)





# If called by itself (Usually this is the case)
if __name__ == '__main__':
    print "starting"
    print perform_panel_check()