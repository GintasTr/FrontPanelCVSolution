from SimpleCV import *

class Display_Painter():
    def __init__(self):
        # Fontsize for all of the text
        self.FONTSIZE = 40
        self.COLOR = Color.RED
        # Text location in the image
        self.UPPER_TEXTLOCATION = (30, 20)
        self.LOWER_TEXTLOCATION = (30, 660)
        # Text for the first scan
        self.REQUEST_TEXT = "Padekite panele nurodytame kvadrate"
        self.REQUEST_TEXT_LOWER = "Padeje spauskite kairi peles klavisa. Noredami sustabdyti, spauskite desini peles klavisa"
        # Text for the incorrect scan
        self.SCAN_AGAIN_TEXT = "Panele nerasta! Bandykite dar karta."
        self.SCAN_AGAIN_TEXT_LOWER = "Padeje spauskite kairi peles klavisa. Noredami sustabdyti, spauskite desini peles klavisa"
        # NOT USED DUE TO MODIFICATIONS # TODO: Delete when surely not needed
        # # Drawn square data:
        self.WIDTH = 5

    # Draws the components on the screen needed for the start request image
    def start_request_image(self, img, PANEL_PLACEMENT_LOCATION, initial_request):
        # Check which tesxt has to be printed: True - first request, False - scan again
        if initial_request: upper_text, lower_text = self.REQUEST_TEXT, self.REQUEST_TEXT_LOWER
        else: upper_text, lower_text = self.SCAN_AGAIN_TEXT, self.SCAN_AGAIN_TEXT_LOWER

        # Set the font size
        img.dl().setFontSize(self.FONTSIZE)

        # Print the text
        img.dl().text(upper_text, self.UPPER_TEXTLOCATION, color = self.COLOR)
        img.dl().text(lower_text, self.LOWER_TEXTLOCATION, color = self.COLOR)

        # Draw the square
        img.dl().rectangle2pts(PANEL_PLACEMENT_LOCATION["TOPLEFT"],
                               PANEL_PLACEMENT_LOCATION["BOTRIGHT"],
                               Color.RED, self.WIDTH)

        # Return the modified image
        return img
