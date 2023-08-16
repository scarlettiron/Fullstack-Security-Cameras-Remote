from asyncio.windows_events import NULL
from logging import raiseExceptions
import cv2 as cv
from urllib.request import urlopen
import numpy as np
import json
from base64 import b64encode
import global_vars as gv
from error_logging import Error_Logs as eLog
import websockets
import asyncio
#load global variables
gv.init()


class camera_live_stream_process:
    def __init__ (self, cam):
        self.cam = cam

        
    async def send_to_remote_server(self, frame):
        print('sending frame to remote server')
        str_frame = str(b64encode(frame))
        payload = json.dumps({
            'type': 'stream',
            'action':'stream',
            'status':False,
            'unit_id':self.cam['unit_id'],
            'unit_ip_url':self.cam['ip_url'],
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


    async def read_camera_stream(self):
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
            await self.send_to_remote_server(imgnp)
        

    async def start_stream_process(self):
    #connect to remote websocket server
        try:
            async with websockets.connect(gv.remoteWsUrl) as remoteServerSocket:
                gv.remoteSocket['connected'] = True
                gv.remoteSocket['socket'] = remoteServerSocket
                
                #send frames from camera streams to remote viewers
                while True:
                    await self.read_camera_stream()
                        

            #except websockets.exceptions.WebsocketException as e:
        except:
            print('remote socket error: ')
            eLog.create_error_log(type='server',
                                    server=gv.server_id,
                                    unit = NULL,
                                    description= 'cam relay socket error with socket connection to remote server'
                                    )
            gv.remoteSocket['connected'] = False
            return
    
            
def run_stream_process(camObj):
        print("inside run")
        stream_process = camera_live_stream_process(camObj)
        asyncio.run(stream_process.start_stream_process())