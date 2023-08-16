from asyncio.windows_events import NULL
import json
from multiprocessing import Process
from pickle import NONE
import websockets
from time import sleep
import asyncio
import global_vars as gv
from handle_socket_messages import LocalSocketActions
from error_logging import Error_Logs as eLog
from remote_client import remote_client
from alerts import Alerts 
from read_cam_feeds import read_camera_stream
from startup_operations import update_persons
#initialize global variables
gv.init()

#keep track of socket instances connected
localSocketsSet = set()


async def local_ws_server_client(local_socket, path):
    print('client connected')
    if local_socket not in localSocketsSet:
        localSocketsSet.add(local_socket)
    #have local server listen for and handle messages from units
        #ping = json.dumps({'type':'ping', 'unit_id':2, "event":"pong"})
        #await local_socket.send(ping)
    try:
        #see if there's a message
        async for message in local_socket:
            print('received message from client: ')  
            
            m = json.loads(message)
            print(m)
            #units initial message is info about itself
            #add this info to the global localSockets hash map
            if m['type'] == 'unit_info':
                unit_info = {   'ip_url':m['ip_url'], 
                                'unit_id':m['unit_id'], 
                                'unit_type':m['unit_type'],
                                "url":'http://' + m["ip_url"] + '/capture',
                                "remote_viewing":False, 
                                "viewers":0,
                                "stream_process":NULL,
                                "relay_process":NULL
                            }
                socketInfo = {'socket':local_socket} | unit_info
                
                gv.localSockets[m['unit_id']] = socketInfo
                
                try:
                    if m['unit_type'] == 'camera':
                            cam_class = read_camera_stream(unit_info)
                            p = Process(target = cam_class.run, args = [], daemon=True)
                            p.start()
                            
                            gv.localSockets[m['unit_id']]['stream_process'] = p
                            
                except:
                    eLog.create_error_log(type = 'device', 
                                            unit = NULL, 
                                            server = NULL, 
                                            description = 'could not add unit information') 
            
            else:
                try:
                    la = LocalSocketActions(message = message)
                    await la.handle_cases()
                except:
                    eLog.create_error_log(
                        type='server',
                        server = gv.server_id,
                        unit = NONE,
                        description = 'cannot process local socket message'
                    ) 
        
        
    #except websockets.exceptions.ConnectionClosed as e:
    except:
        print('local socket disconnected')
        eLog.create_error_log(type='server', 
                              server = gv.server_id,
                              unit = NULL,
                              description='error handling local sockets'
                              )  
        
    finally:
        #remove socket from active sockets set
        localSocketsSet.remove(local_socket)
        for key in gv.localSockets:
            if gv.localSockets[key]['socket'] == local_socket:
                unit = gv.localSockets[key]
                #if device is a camera remove from camera's connected
                if unit['stream_process']:
                    unit['stream_process'].terminate()
                if unit['relay_process']:
                    unit['relay_process'].terminate()
                        
                gv.localSockets.pop(key, NONE) 
                break
                 
                
#start local server 
async def start_server():
    async with websockets.serve(local_ws_server_client, gv.PATH, gv.PORT):
        print('starting program')
        await asyncio.Future()  
                
   


#the two following methods run the home local server as well as 
# the remote server client which handles pinging and other events
async def run_localServer_MainRemoteClient():
    task1 = asyncio.create_task(start_server())
    task2 = asyncio.create_task(remote_client(type='main'))
    await task2
    await task1

def lServer_rClient():
    asyncio.run(run_localServer_MainRemoteClient())
    
    
### the following method is for sending error logs from the entire functioning
###program and sending alerts if not successfully sent when first created
#this runs periodically
def handle_sending_logs():
    while True:
        Alerts().send_alert_list_to_remote_api()
        #eLog().send_error_logs()
        sleep(86400)

#main
if __name__ == '__main__':

    #start main local server and remote client that controls everything in the house
    #except for camera streams
    P1 = Process(target = lServer_rClient)
    P1.start()  
    
    #for updating images for facial rec
    P2 = Process(target=update_persons)
    P2.start()
    
    #for error logging and sending alert records
    P3 = Process(target = handle_sending_logs)
    P3.start()
    
    P1.join()
    P2.join()
    P3.join()

     

