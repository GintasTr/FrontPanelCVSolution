from sys import argv
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
    required_parts = parts_handler.parts_required(argv)

    # Check if it returned error (string, where it should return dictionary) and terminate if so, returning the error.
    if type(required_parts) == str: print required_parts; return required_parts

    # Get the testing image
    img = operator_interface.get_required_image()

    # Check if it returned error (string, where it should return image)and terminate if so.
    if type(img) == str:
        if img[0] == "E": print img; return img


    # Identify which parts are mounted currently
    parts_present = parts_handler.parts_present(img)

    # Check if it returned error (string, where it should return dictionary) and terminate if so.
    if type(parts_present) == str: print parts_present; return parts_present

    # Compare the present parts with required parts
    test_result = parts_handler.compare_parts(required_parts, parts_present)

    # Compile the result report
    if "Failed" in test_result.values():
        # if at least one failed, then:
        return "FAILED TEST", str(test_result)
    # If no fails happened
    else: return "PASSED TEST", str(test_result)



# If called by itself (Usually this is the case)
if __name__ == '__main__':
    print "starting"
    print perform_panel_check()