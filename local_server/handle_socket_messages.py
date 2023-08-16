from asyncio.windows_events import NULL
import json
from pickle import NONE
import global_vars as gv
from error_logging import Error_Logs as eLog
from multiprocessing import Process
from live_stream import run_stream_process
from startup_operations import update_face_encodings

#load global vars
gv.init()


#correctly formats message to be sent to remote server, returns payload
def format_message(message):

    defaultDict = {
    "type":False,
    "action":False,
    "unit_id":False,
    "unit_ip_url":False,
    "image":False,
    "status":False
    }
    for x in message:
        if x in defaultDict.keys():
            defaultDict[x] = message[x]
            
    payload = json.dumps(defaultDict)
    return payload




#containes methods for handling all messages and corresponding actions 
# from remote server
class RemoteServerActions:
    def __init__(self, socket=NONE, message = NONE, unit = NONE, type = NONE):
        #when asigned, must be a dictionary
        self.socket = socket
        self.message = message
        self.unit = unit
        self.type = type
     
    #find the correct socket instance in the global local_sockets array
    #this insures the message will only be sent to the required unit 
    #instead of all units   
    async def get_unit(self):
        if not self.message or not self.unit:
            print('provide message from socket and global sockets array')
            return
        
        
        #if unit id is not set as 'all' this is used when not
        #performing a mass update
        if gv.localSockets[self.message['unit_id']]:
            self.unit = gv.localSockets[self.message['unit_id']]
        
        #if unit is set to all from remote server
        #this is used when performing a mass update
        #local servers socket map provides unit id in home_server.py
        elif self.message['unit_id'] == 'all':
            unit = gv.localSockets[self.unit]
            self.unit = unit
        
        else:
            print('unit not in gv.localSockets')
            return False
        
        if self.unit['socket']:
            self.socket = self.unit['socket']
        else:
            
            return False
        
        return self
        
    
    
    
    
    #handles ping from frontend or remote server to see if unit is available
    #to receive commands
    async def ping(self):
        if not self.socket or not self.message:
            print('socket instance and message from server required')
            return
        
        payload = format_message({
                'type':self.message['type'],
                'unit_id':self.message['unit_id'],  
                })

        try:
            await self.socket['socket'].send(payload)
        except:
            eLog.create_error_log(type='device', 
                                server = NULL,
                                unit = self.socket['unit_id'],
                                description='could not relay ping to unit')
    
          
    #relays command to correct unit       
    async def command(self):
        if not self.socket or not self.message:
            print('socket instance and socket message required')
        try:
            #if remote client type is 'main' client for home server
            if self.type == 'main' and self.message['action'] == 'update persons':
                update_face_encodings()
            
            else:
                payload = format_message({
                'type':self.message['type'],
                'action':self.message['action'],
                'unit_id':self.message['unit_id'],
                })
                
                await self.socket['socket'].send(payload)
        except:
            eLog.create_error_log(type = 'socket', 
                                unit = self.message['unit_id'],
                                server=NULL, 
                                description='could not send command to unit')
   
   
    
    ###!!!under major construction!!!###    
    #has to be modified to support multiple users viewing and ending streams from
    #the same unit
    async def stream(self):
        if not self.message and self.unit['unit_type'] != 'camera':
            print('remote socket message and unit_type must be camera')
            return
        
        if isinstance(self.message['unit_id'], list) and self.message['action'] == 'end':
            for id in self.message['unit_id']:
                if id in gv.localSockets.keys():
                    cam = gv.localSockets['id']
                    if cam['viewers'] <= 1:
                        cam['remote_viewing'] == False
                        cam['viewers'] = 0
                        cam['relay_process'].terminate()
                        
                    elif cam['viewers'] > 1:
                        cam['viewers'] -= 1
            return True

        match self.message['action']:
            #modify this to support multiple viewing and ending requests
            case 'request':
                gv.localSockets[self.unit['unit_id']]['remote_viewing'] = True
                gv.localSockets[self.unit['unit_id']]['viewers'] += 1

                if self.unit['relay_process']:
                    return True
                
                non_passed_args = ['socket', 'stream_process', 'relay_process']
                passed_args = {}

                for key in self.unit:
                    if key not in non_passed_args:
                        passed_args[key] = self.unit[key]
                        
                #relay_process = Process(target = camera_live_stream_process(passed_args).run(), args=[passed_args], daemon=True)
                relay_process = Process(target = run_stream_process, args = [passed_args], daemon=True)
                relay_process.start()
                gv.localSockets[self.unit['unit_id']]['relay_process'] = relay_process
                return self
            case 'end':
                gv.localSockets[self.unit['unit_id']]['remote_viewing'] = False
            #this needs to be included for when server echo's back to
            # all connected sockets
            case 'sending':
                print('sending frame')
                pass
            case _:
                pass

    #decides what action to take based on remote socket message 'type'
    async def handle_cases(self):
        try:
            if not self.message:
                print('message from remote server required')
                return
            
            socket_unit_info = await self.get_unit()
            if not socket_unit_info and self.message['unit_id'] is not 'all':
                print('can not find unit')
                return  
            match self.message['type']:
                case 'ping':
                    if not self.unit['unit_type'] == 'camera':
                        await self.ping()
                case 'command':
                    #if self.unit['unit_type'] != 'camera':
                        await self.command()
                case 'stream':
                    if self.unit['unit_type'] == 'camera':
                        await self.stream()
                
                case 'pong':
                    print('pong')
                    
                case _:
                    eLog.create_error_log(type='remote server', 
                                        server=gv.server_id, 
                                        unit=self.message['unit_id'],
                                        description='Unknown command type')
            return True
        except:
            eLog.create_error_log(type='remote server', 
                                        server=gv.server_id, 
                                        unit=self.message['unit_id'],
                                        description='type not included in message')
            return False




        

class LocalSocketActions:
    def __init__(self, socket = NONE, message = NONE, unit_id = NONE):
        #has to be a dictionary {'socket':socket}
        self.socket = socket
        self.message = message
        self.unit_id = unit_id
        
    def get_unit_socket(self):
        if not self.message:
            print('socket message required')
            return
        
        for socket in gv.localSockets:
            print(self.message['unit_id'])
            if socket['unit_id'] == int(self.message['unit_id']):
                self.socket = {'socket':socket['socket']}
                self.unit_id = socket['unit_id']
                break
        return self


    
    async def pong(self):
        if not self.message:
            print('socket message required')
            return

        payload = format_message(self.message)

        try:
            await gv.remoteSocket['socket'].send(payload)
        except:
            eLog.create_error_log(
                type='remote server',
                server = gv.server_id,
                unit = NONE,
                description='could not send pong to remote server'
            )
            
    async def error(self):
        if not self.message:
            print('socket message required')
            return
        eLog.create_error_log(type = 'device', unit = self.message['unit_id'], 
                                  server = NULL, description='unknown issue with unit')
        

    async def handle_cases(self):
        if not self.message:
            print('socket message required')
            return
        data = json.loads(self.message)
        self.message = data
        try:
            match data['type']:
                case 'pong':
                    await self.pong()
            
                case 'error':
                    await self.error()
        except:
            eLog.create_error_log(
                type = 'server',
                server = gv.server_id,
                unit = NONE,
                description = 'error processing local socket messages'
            )
        
        