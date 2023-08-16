from asyncio.windows_events import NULL
import websockets 
import json
import asyncio


unit = {'unit_id':2, 'ip_url':'192.168.2.4'}

Socket = {'socket':NULL}


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

async def client_socket():
    initial_setup_done = False
    try:
        #python client_testing.py
        print('attempting to connect to remote server')
        async with websockets.connect("ws://192.168.2.4:8080") as socket:
            print('local server successfully connected to remote server')
            #listen for messages from remote server
            Socket['socket'] = socket
            while True:
                if not initial_setup_done:
                    initial_payload = format_message({
                        'type':'unit_info',
                        'unit_id':unit['unit_id'],
                        'ip_url':unit['ip']
                    })
                    print('sending intial payload')
                    #await socket.send(intial_payload)
                    print(initial_payload)
                    await Socket['socket'].send(initial_payload)
                    initial_setup_done = True
                socket_message = await socket.recv()
                await handle_message(socket_message)
                #message = json.loads(socket_message)
            

    except websockets.exceptions.ConnectionClosed as e:
        print('remote socket error: ')
        print(e)
        return
    
async def handle_message(m):
    message = json.loads(m)
    print(message)
    if message['type'] == 'ping':
        print('pinged')
        
        payload = format_message({
            'type':'pong',
            'unit_id':unit['unit_id'],
            'status':'locked'
        })
        await Socket['socket'].send(payload)    

asyncio.run(client_socket())
