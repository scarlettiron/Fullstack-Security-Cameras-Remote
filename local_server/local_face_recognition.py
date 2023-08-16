import cv2 as cv
import numpy as np
import global_vars as gv
import face_recognition as fr
import os
from utils import rescale_frame
from alerts import Alerts

#load global variables
gv.init()

class FaceRecognition:
    def __init__(self, frame = None, cam = None, 
                 face_results = [], alert_face_encodings = [],
                 tasks = [], allowed_face_encodings = [],
                 frame_encodings = None):
        self.frame = frame
        self.cam  = cam
        self.face_results = face_results
        self.frame_encodings = frame_encodings
        self.alert_frame_encodings = alert_face_encodings
        self.allowed_face_encodings = allowed_face_encodings
        self.tasks = tasks
    
    #see if person is in high alert list
    #if so send alert immediately
    def find_if_high_alert(self):
        
        recognized_alerts = []
        for high_alert_encoding in gv.high_alert_face_encodings:
            result = fr.compare_faces(self.frame_encodings, high_alert_encoding)
            for r in result:
                recognized_alerts.append(r)
        
        if len(recognized_alerts) > 0:
            Alerts(unit_id = self.cam['unit_id'], img = self.frame, high_alert = True).create_alert().send_immediate_alert()
            return
        Alerts(unit_id = self.cam['unit_id'], img = self.frame).create_alert()
        return
    
    #rewrite designed to load alert encdoings when camera is connected to socket
    #this saves time when processing images during face recognition
    async def load_high_alert_faces(self):
        for file in os.listdir('./images/high_alert_persons/'):
            img_path = os.path.join('./images/high_alert_persons/', file)
            img = cv.imread(img_path)
            #resize frame for faster processing
            resized_img = rescale_frame(img)
            #convert to grayscale for even faster processing
            rgb= cv.cvtColor(resized_img, cv.COLOR_BGR2RGB)
            img_encoding = fr.face_encodings(rgb)[0]
            
            #add to global list of encodings
            self.alert_frame_encodings.append(img_encoding)
            gv.high_alert_face_encodings.append(img_encoding)
            
            return self
    
    #rewrite designed to load allowed encdoings when camera is connected to socket
    #this saves time when processing images during face recognition       
    async def load_allowed_faces(self):
        for file in os.listdir('./images/allowed_persons/'):
            img_path = os.path.join('./images/allowed_persons/', file)
            img = cv.imread(img_path)
            
            #resize frame for faster processing
            resized_img = rescale_frame(img)
            
            #convert to grayscale for even faster processing
            rgb= cv.cvtColor(resized_img, cv.COLOR_BGR2RGB)
            img_encoding = fr.face_encodings(rgb)[0]
            
            #add to global list of encodings
            self.allowed_face_encodings.append(img_encoding)
            gv.allowed_face_encodings.append(img_encoding)
            
            return self
        
    async def face_recognition(self):
        print('face rec trigired')
        results = []
        #encode image for processing
        try:
            encodings = fr.face_encodings(self.frame)
            self.frame_encodings = encodings
        except:
            print('cannot encode frame')
            return
        
        #ensure all encodings have loaded for allowed persons
        if len(gv.allowed_face_encodings) == 0 and not gv.face_encoding_tasks['allowed'].done():
            await gv.face_encoding_tasks['allowed']
        
        #get and loop through all images in folder for comparison
        for allowed_encoding in gv.allowed_face_encodings:
            #compare current faces to image
            result = fr.compare_faces(encodings, allowed_encoding)
            for r in result:
                results.append(r)
        print(results)  
        if False in result:
            #ensure all encodings have loaded for high alert persons
            if len(gv.high_alert_face_encodings) == 0 and not gv.face_encoding_tasks['high_alert'].done():
                await gv.face_encoding_tasks['high_alert']
                
            #see if person is in high alert folder
            self.find_if_high_alert()
        
        #in case 
        return results
    
        

def face_recognition(frame, cam):
    #array of results for face rec
    print(cam)
    results = []
    #encode image for processing
    try:
        encodings = fr.face_encodings(frame)
    except:
       print('cannot encode frame')
       return
    
    #get and loop through all images in folder for comparison
    for file in os.listdir('./images/allowed_persons/'):
        img_path = os.path.join('./images/allowed_persons/', file)
        img = cv.imread(img_path)
        #resize frame for faster processing
        #resized_img = cv.resize(img, (300, 400))
        resized_img = rescale_frame(img)
        #convert to grayscale for even faster processing
        rgb= cv.cvtColor(resized_img, cv.COLOR_BGR2RGB)
        img_encoding = fr.face_encodings(rgb)[0]
        #compare current faces to image
        result = fr.compare_faces(encodings, img_encoding)
        for r in result:
            results.append(r)
        
    if False in result:
        #see if person is in high alert folder

        Alerts(unit_id = cam['unit_id'], img = frame).create_alert()
    return results
    


  
    