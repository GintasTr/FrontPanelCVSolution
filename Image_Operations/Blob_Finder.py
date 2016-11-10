from SimpleCV import *

# Class which crops all of the required locations from the images
class Blob_Finder():
    def __init__(self):
        None


    # Find the main panel blob
    def panel_blob(self, img):
        # PANEL LIMITS CONSTANTS:
        MIN_PANEL_SIZE, MAX_PANEL_SIZE = 134000, 143000
        MINIMUM_WIDTH, MAXIMUM_WIDTH = 610, 640
        MINIMUM_HEIGHT, MAXIMUM_HEIGHT = 200, 245
        # Find all of the blobs in the image which satisfy the size requirements
        all_blobs = img.findBlobs(minsize=MIN_PANEL_SIZE, maxsize=MAX_PANEL_SIZE)
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
        if (MINIMUM_WIDTH < biggest_blob.width() < MAXIMUM_WIDTH) and \
           (MINIMUM_HEIGHT < biggest_blob.height() < MAXIMUM_HEIGHT):
            return biggest_blob
        else:
            return None


    # Find the button top left (clock or trapeze) blobs
    def button_blob(self, img):
        # Find all blobs
        all_blobs = img.findBlobs()
        if all_blobs == None:
            return None
        # Select the one which minimum X value is smallest (closest to the left edge)
        main_blob = all_blobs[0]
        for single_blob in all_blobs:
            if single_blob.minX() < main_blob.minX(): main_blob = single_blob
        return main_blob

    # Find the temperature 18/64 blobs - closest to the left edge
    def temperature_blob(self, img):
        # Find all blobs
        all_blobs = img.findBlobs()
        if all_blobs == None:
            return None
        # Select the one which minimum X value is smallest (closest to the left edge)
        main_blob = all_blobs[0]
        for single_blob in all_blobs:
            if single_blob.minX() < main_blob.minX(): main_blob = single_blob
        return main_blob

    # Find the controller blob - one at the top.
    def controller_blob(self, img):
        # Find all blobs
        all_blobs = img.findBlobs(minsize = 5)
        if all_blobs == None:
            return None
        # Select the biggest one in the image
        biggest_blob = all_blobs.sortArea()[-1]
        return biggest_blob