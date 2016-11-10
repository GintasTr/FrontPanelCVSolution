from SimpleCV import *

# Class which crops all of the required locations from the images
class Blob_Finder():
    def __init__(self):
        None


    # Find the button top left (clock or trapeze) blobs
    def button_blob(self, img, testing = False):
        # Find all blobs
        all_blobs = img.findBlobs()
        if all_blobs == None:
            return None
        # Select the one, closest to the middle of the left edge (x=1, y = height/2)
        main_blob = all_blobs.sortDistance((1, img.height/2))[0]
        if testing:
            main_blob.draw(color=Color.RED, width=5)
            all_blobs.draw()
            return img
        else:
            return main_blob