from logging import raiseExceptions
import cv2 as cv
import numpy as np
from random import randint



def rescale_frame(frame, scale_to=0.75):
        # to access width and height of frame use frame.shape
        # frame[0] is for height
        # frame[1] is for width
        #make sure to cast as int
        new_height = int(frame.shape[0] * scale_to)
        new_width = int(frame.shape[1] *  scale_to)
        new_dimensions = (new_width, new_height)
        
        return cv.resize(frame, new_dimensions, interpolation = cv.INTER_AREA)

def save_img(frame, extension='.jpg', name='intruder'):
        rnum = randint(0, 300)
        try:
                cv.imwrite('/images/alerts/' + str(name)+str(rnum)+str(extension), frame)
        except:
                raiseExceptions('could not save image')