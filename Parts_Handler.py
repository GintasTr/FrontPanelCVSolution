from SimpleCV import *
from Parts_Identification import Parts_Identification

class Parts_Handler:
    def __init__(self, PANEL_PLACEMENT_LOCATION):
        # Localise PANEL_PLACEMENT_LOCATION
        self.PANEL_PLACEMENT_LOCATION = PANEL_PLACEMENT_LOCATION
        # Object to identify the present parts
        self.parts_identification = Parts_Identification(self.PANEL_PLACEMENT_LOCATION)

    # Function to determine whether barcode was correctly entered and which parts are required for specific barcode
    def parts_required(self, parameters_entered):
        # This is where the front panel appearance addition/modification should occur!
        panel_17444646 = {'button': 'clock','temperature': 'celsius','controller': 'squares'}
        panel_17444648 = {'button': 'clock','temperature': 'fahrenheit','controller': 'squares'}
        panel_17444664 = {'button': 'trapeze','temperature': 'fahrenheit','controller': 'figures'}
        panel_17444661 = {'button': 'trapeze','temperature': 'celsius','controller': 'figures'}

        # Check if any parameters were entered and return the error if none.
        if len(parameters_entered) < 2: return "ERROR - barcode not entered as a parameter."
        # Report barcode received
        print "Barcode entered:", parameters_entered[1]

        # Check if barcode entered is one of required ones and assign corresponding appearance
        if parameters_entered[1] == "17444646-01": required_panel = panel_17444646
        elif parameters_entered[1] == "17444648-01": required_panel = panel_17444648
        elif parameters_entered[1] == "17444664-01": required_panel = panel_17444664
        elif parameters_entered[1] == "17444661-01": required_panel = panel_17444661
        else: return "ERROR - incorrect barcode enetered"

        print "Panel appearance successfully selected:", required_panel
        return required_panel


    # Function to check which parts are actually present
    def parts_present(self, img):

        # Identify the button
        button = self.parts_identification.which_button(img)
        # If button was not found - ERROR was returned
        if button[0] == "E": print button; return button

        # Identify the temperature
        temperature = self.parts_identification.which_temperature(img)
        # If temperature was not found - ERROR was returned
        if temperature[0] == "E": print temperature; return temperature

        # Identify the controller
        controller = self.parts_identification.which_controller(img)
        # If button was not found - ERROR was returned
        if controller[0] == "E": print controller; return controller

        # Assign parts present to the list, to be easily comparable
        local_parts_present = {'button': button,
                         'temperature': temperature,
                         'controller': controller}
        # Report the result and return
        print "Parts present:", local_parts_present
        return local_parts_present


    # Function to compare parts present and parts reuired
    def compare_parts(self, required_parts, parts_present):
        result = {}
        for key in required_parts:
            if required_parts[key] == parts_present[key]: result[key] = "Passed"
            else: result[key] = "Failed"
        print "Result is:", result
        return result


# If it is launched as a main
if __name__ == '__main__':
    cam = Camera(0, {"width": 1280, "height": 720})
    time.sleep(0.2)
    img = cam.getImage()
    PANEL_PLACEMENT_LOCATION = {"TOPLEFT": (290, 220), "BOTRIGHT": (990, 600)}
    testing_object = Parts_Handler(PANEL_PLACEMENT_LOCATION)
    parts_required = testing_object.parts_required(("launching_call",'17444646-01'))
    parts_present = testing_object.parts_present(img)

    testing_object.compare_parts(parts_present, parts_required)
