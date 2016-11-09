from SimpleCV import *
from Parts_Identification import Parts_Identification

cam = Camera(0, {"width": 1280, "height": 720})
disp = Display((1280,720))

# used to calibrate where to draw a square
def square_calibration():
    while disp.isNotDone():
        img = cam.getImage()
        # img = img.flipHorizontal()
        # img = img.flipVertical()

        pressed = pg.key.get_pressed()

        if disp.mouseLeft:
            local_result = [disp.mouseX, disp.mouseY]  # Show coords on screen with modifiable square size
            text = "X:" + str(local_result[0]) + " Y:" + str(local_result[1])
            print text
            img.dl().setFontSize(20)
            img.dl().text(text, (local_result[0] + 10, local_result[1] + 10), color=Color.RED)

        if (pressed[pg.K_RETURN] == 1):  # If enter pressed
            if local_result is not None:
                disp.done = True  # Turn off Display
            else:
                print "Pressed Enter too early"

        img.save(disp)


# Used to calibrate where to crop from the centre of the main blob
def cropping_calibration(panel_coordinates, button_location):
    parts_identifier = Parts_Identification(panel_coordinates)
    while disp.isNotDone():
        img = cam.getImage()
        main_blob = parts_identifier.find_panel(img)
        if main_blob == None:
            print "No blobs found"
            continue
        img2 = main_blob.crop()
        img2 = img2.invert()

        image_crop_top_left = (panel_coordinates['TOPLEFT'][0] + main_blob.topLeftCorner()[0],
                               panel_coordinates['TOPLEFT'][1] + main_blob.topLeftCorner()[1])
        image_crop_bot_right = (panel_coordinates['TOPLEFT'][0] + main_blob.bottomRightCorner()[0],
                               panel_coordinates['TOPLEFT'][1] + main_blob.bottomRightCorner()[1])

        img = img.crop(image_crop_top_left,image_crop_bot_right)

        # CHANGE HERE:
        # img = img2

        cropping_top_left = (main_blob.width() * button_location[0][0]/100,
                             main_blob.height() * button_location[0][1]/100)
        cropping_bot_rigth = (main_blob.width() * button_location[1][0] / 100,
                             main_blob.height() * button_location[1][1] / 100)
        img.dl().rectangle2pts(cropping_top_left,
                               cropping_bot_rigth,
                               Color.RED, 3)

        pressed = pg.key.get_pressed()

        if disp.mouseLeft:
            local_result = [disp.mouseX, disp.mouseY]  # Show coords on screen with modifiable square size
            text = "X:" + str(local_result[0]) + "," + str(local_result[0]*100/main_blob.width()) + \
                   " Y:" + str(local_result[1]) + "," + str(local_result[1]*100/main_blob.height())
            text2 = "X is a part of: ", (local_result[0]*100/main_blob.width())
            text3 = "Y is a part of: ", (local_result[1]*100/main_blob.height())
            print text
            print text2
            print text3
            img.dl().setFontSize(20)
            img.dl().text(text, (local_result[0] + 10, local_result[1] + 10), color=Color.RED)

        if (pressed[pg.K_RETURN] == 1):  # If enter pressed
            if local_result is not None:
                disp.done = True  # Turn off Display
            else:
                print "Pressed Enter too early"

        img.save(disp)



# If it is launched as a main
if __name__ == '__main__':
    # TO TEST CROPPING:
    PANEL_PLACEMENT_LOCATION = {"TOPLEFT": (290, 220), "BOTRIGHT": (990, 600)}
    BUTTON_CROPPING_LOCATION = ((10,32),(19,49))
    # square_calibration()
    cropping_calibration(PANEL_PLACEMENT_LOCATION, BUTTON_CROPPING_LOCATION)

