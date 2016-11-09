from SimpleCV import *


# Class which performs all of the image filtering and morphops
class Filter():
    def __init__(self):
        # PUT CALIBRATED FILTER VALUES HERE
        None


    # Function which performs the binarization and smoothing to be able to determine whether image taken is correct
    def image_confirmation_filter(self, img):
        # Brightness level to binarize to:
        BINARIZE_THRESH = 80
        # Make the image binary (totally black or totally white)
        img = img.binarize(thresh = BINARIZE_THRESH)
        # Make the image smooth - morphopen http://homepages.inf.ed.ac.uk/rbf/HIPR2/morops.htm
        img = img.morphOpen()
        # Glue together seperate pieces - dilate
        img = img.dilate(2)
        return img



if __name__ == '__main__':
    topleft = (290,220) # Adjust these values for test
    botright = (990,600)    # Adjust these values for test
    testing_thing = Filter()
    cam = Camera(0, {"width": 1280, "height": 720})
    disp = Display((1280,720))
    while disp.isNotDone():
        img = cam.getImage()
        img = img.crop(topleft, botright)
        img = testing_thing.image_confirmation_filter(img)
        # ADD OTHER CROPPING LOCATIONS FOR TESTING
        img.save(disp)
