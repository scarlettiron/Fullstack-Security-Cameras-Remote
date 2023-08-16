from asyncio.windows_events import NULL
from logging import raiseExceptions
import cv2 as cv
from urllib.request import urlopen
import numpy as np
import json
import asyncio
from base64 import b64encode
import global_vars as gv
from object_detection import human_detection
from error_logging import Error_Logs as eLog
from local_face_recognition import FaceRecognition as faceRec
#load global variables
gv.init()

class read_camera_stream:
    def __init__(self, cam):
        self.cam = cam
        
    def load_encodings(self):
        load_high_alerts_task = asyncio.create_task(faceRec().load_high_alert_faces())
        load_allowed_faces_task = asyncio.create_task(faceRec().load_allowed_faces())
        gv.face_encoding_tasks['high_alert'] = load_high_alerts_task
        gv.face_encoding_tasks['allowed'] = load_allowed_faces_task
        return True
    
    #takes camera info object as argument
    async def read_unit_stream(self):
        encoding_loader  = self.load_encodings()
            
        if not self.cam:
            eLog.create_error_log(
            type='stream',
            unit=NULL,
            server=gv.server_id,
            description='error finding camera'
            )
            return
        
        while True:
            #open url to view info
            try:
                stream_url = urlopen(self.cam['url'])
            except:
                eLog.create_error_log(
                    type='stream',
                    unit=NULL,
                    server=gv.server_id,
                    description='error opening unit stream url'
                )
                return
            
            #read information from url, convert array into bytarray 
            #pull frame from stream_feed for later use
            stream_feed = stream_url.read()
            imgnp = np.asarray(bytearray(stream_feed), dtype="uint8")
            img = cv.imdecode(imgnp, -1)
            

            human_detection(img, self.cam) 
            ''' if not encoding_loader.done():
                await encoding_loader '''

    #run face rec stream
    def run(self):
        print('inside run')
        gv.localSockets[self.cam['unit_id']] = self.cam
        asyncio.run(self.read_unit_stream())
        

  
async def send_to_remote_server(frame, camObj):
    print('sending frame to remote server')
    str_frame = str(b64encode(frame))
    payload = json.dumps({
        'type': 'stream',
        'action':'stream',
        'status':False,
        'unit_id':camObj['unit_id'],
        'unit_ip_url':camObj['ip_url'],
        'image':str_frame,
    })
    try:
        await gv.remoteSocket['socket'].send(payload)
        return
    except:
        raiseExceptions('error sending encoded frame to remote websocket server')
        eLog.create_error_log(
            type='stream',
            unit=NULL,
            server=gv.server_id,
            description='error sending video frame to remote server'
        )
        
        
 

    