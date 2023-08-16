from asyncio.windows_events import NULL
from pickle import NONE
import websockets
import global_vars as gv
from handle_socket_messages import RemoteServerActions
from error_logging import Error_Logs as eLog
import json


gv.init()

#connect to remote websocket server
async def remote_client(cam=NULL, type=''):
    #try:
    print('attempting to connect to remote server')
        
    async with websockets.connect(gv.remoteWsUrl) as remoteServerSocket:
        gv.remoteSocket['connected'] = True
        gv.remoteSocket['socket'] = remoteServerSocket
        print(type + ' local server successfully connected to remote server')
        #listen for messages from remote server
        while True:
            message = await remoteServerSocket.recv()
            print(type + ': got a message')
            print(message)
            #try:
            m = json.loads(message)
            ra = RemoteServerActions(message=m, type=type)
            #socket =  await ra.get_unit()
            status = await ra.handle_cases()
            ''' except:
                eLog.create_error_log(
                    type='remote server',
                    server = gv.server_id,
                    unit = False,
                    description = type + ' issue handling socket message from remote server'
                ) '''

    #except websockets.exceptions.WebsocketException as e:
    ''' except:
        print('remote socket error: ')
        eLog.create_error_log(type='server',
                              server=gv.server_id,
                              unit = NULL,
                              description= type + ' error with socket connection to remote server'
                              )
        gv.remoteSocket['connected'] = False
        return '''
    

     