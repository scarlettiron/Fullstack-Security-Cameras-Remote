import cv2 as cv
import numpy as np
import asyncio
import global_vars as gv
from utils import rescale_frame
from local_face_recognition import FaceRecognition
from alerts import Alerts
import nest_asyncio
nest_asyncio.apply()

#initialize open-cv's provided human detector
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

#initialize opencv's  provided face detection 
#arguments is path to cascade on system and the string is the base we want to go off of
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

def human_detection(frame, cam):
    #prep image for pocessing 
    #resize frame for faster processing
    print('inside human detecting')
    resized_frame = rescale_frame(frame)
    #convert to grayscale for even faster processing
    gray_frame = cv.cvtColor(resized_frame, cv.COLOR_RGB2GRAY)
    
    ### not currently in use ###
    # apply threshold. all pixels with a level larger than 80 are shown in white. the others are shown in black:
    #ret, frame = cv.threshold(gray_frame,80,255,cv.THRESH_BINARY)
    
    # detect people in the image
    # returns the bounding boxes for the detected objects
    #first argument is the frame to analyzed
    #second is the amount of windows for HOG to perform detection on
    #the SMALLER the winstride the MORE windows are evaluated
    boxes, weights = hog.detectMultiScale(gray_frame, winStride=(8,8) )

    #run through upclose face detection
    face = face_detection(frame, gray_frame, cam)
    
    #if face detection was unsuccessful create Alert that a body was
    #detected and return
    if weights and not face:
        Alerts(unit_id = cam["unit_id"], img = gray_frame, description="body detected").create_alert()
    return

        
        


#detect if there is a face in the frame        
def face_detection(org_frame, gray_frame, cam):
    print('inside face detection')
    ##detect faces in this image
    #https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbmF1cGpSYzRIbF96UmpyNVVFS1h6T05ieVN5d3xBQ3Jtc0trbnhhWW9JbEVEdUJkR3hUNmFFYVRWaUUtbnZINTl2Rlk3YzJnNWZKNjdVUFBoMlJtVEx3WUxobUtyaU5ySFFVcTVpSDlPRXM5NFpVcF84SkpjUlJLV0hrd0dVbXZmNTFLRllLTXdrcHg5ZWU5U3l1NA&q=https%3A%2F%2Fstackoverflow.com%2Fquestions%2F20801015%2Frecommended-values-for-opencv-detectmultiscale-parameters&v=mPCZLOVTEc4
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 3)
    print(faces)
    
    #if face is detected, run face recognition
    if len(faces) != 0:
        print('face detected')
        #face_rec_results = face_recognition(org_frame, cam)
        Fr = FaceRecognition(frame = org_frame, cam=cam)
        face_rec_results = asyncio.run(Fr.face_recognition())
        #in case face recognition was unsuccessful create alert that 
        #a face was detected
        if len(face_rec_results) == 0:
            Alerts(unit_id = cam["unit_id"], img = gray_frame, description="face detected").create_alert()
        return True
    return False





#for local object detectio testing only
from urllib.request import urlopen
from time import sleep
def OD():
    while True:
        stream_url = urlopen('http://192.168.2.15/capture')
        stream_feed = stream_url.read()
        imgnp = np.asarray(bytearray(stream_feed), dtype="uint8")
        img = cv.imdecode(imgnp, -1)
        cv.imshow('Face Detection', img)
        boxes, weights = hog.detectMultiScale(img, winStride=(8,8) )
       
        print(weights)
        if len(weights) > 0:
            boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

            for (xA, yA, xB, yB) in boxes:
                # display the detected boxes in the frame
                cv.rectangle(img, (xA, yA), (xB, yB),
                                    (0, 255, 0), 2)
            print('body detected')
            
        
        faces = face_cascade.detectMultiScale(img, 1.3, 3)
        print(faces)
        
        if len(faces) > 0:
            print('face detected')
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            for (x,y,w,h) in faces:
                img = cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
        
        cv.imshow('Face Detection', img)
        cv.waitKey(3000)
        cv.destroyAllWindows()
                
        #human_detection(img, {'unit_id':"2"}) 
        ''' boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the frame
            cv.rectangle(gray_frame, (xA, yA), (xB, yB),
                            (0, 255, 0), 2)  '''
    
if __name__ == "__main__":
    OD()
    