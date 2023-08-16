import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class WsConsumer(AsyncWebsocketConsumer):
    ### add logic to ensure client ip connecting to channel is a part of the
    #household
    
    async def connect(self):
        #self.user = self.scope['user']
        #print(self.user)
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print("about to join channel")
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("about to except")
        
        await self.accept()
        print("accepted")

        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        type = text_data_json['type']
        action = text_data_json['action']
        status = text_data_json['status']
        unit_id = text_data_json['unit_id']
        image = text_data_json['image']
        unit_ip_url = text_data_json['unit_ip_url']
        



        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': type,
                'action':action,
                'status':status,
                'unit_id':unit_id,
                'unit_ip_url':unit_ip_url,
                'image':image,
            })

    # Receive message from room group
    #for sending commands to different devices
    #put 'command' as type
    #put device id as device
    #put action device is to perform as action (lock, unlock)
    async def command(self, event):
        type = event['type']
        action = event['action']
        status = event['status']
        unit_id = event['unit_id']
        unit_ip_url = event['unit_ip_url']
        image = event['image']
        
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': type,
            'action':action,
            'status':status,
            'unit_id':unit_id,
            'unit_ip_url':unit_ip_url,
            'image':image,
        }))
        
        
    # ping device to see if device is online  
    async def ping(self, event):
        type = event['type']
        action = event['action']
        status = event['status']
        unit_id = event['unit_id']
        unit_ip_url = event['unit_ip_url']
        image = event['image']
        
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': type,
            'action':action,
            'status':status,
            'unit_id':unit_id,
            'unit_ip_url':unit_ip_url,
            'image':image,
        }))
    
    #unit responding to command of type 'ping'
    #returns unit ip url for viewing video stream
    #or returns if unit is online and availabe to receive commands
    async def pong(self, event):
        type = event['type']
        action = event['action']
        status = event['status']
        unit_id = event['unit_id']
        unit_ip_url = event['unit_ip_url']
        image = event['image']
        
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': type,
            'action':action,
            'status':status,
            'unit_id':unit_id,
            'unit_ip_url':unit_ip_url,
            'image':image,
        }))
    
    
    #if alert is intruder include image as blob 
    async def alert(self, event):
        type = event['type']
        action = event['action']
        status = event['status']
        unit_id = event['unit_id']
        unit_ip_url = event['unit_ip_url']
        image = event['image']
        
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': type,
            'action':action,
            'status':status,
            'unit_id':unit_id,
            'unit_ip_url':unit_ip_url,
            'image':image,
        }))
        
        
        
        
        
        
    async def stream(self, event):
        type = event['type']
        action = event['action']
        status = event['status']
        unit_id = event['unit_id']
        unit_ip_url = event['unit_ip_url']
        image = event['image']
        
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': type,
            'action':action,
            'status':status,
            'unit_id':unit_id,
            'unit_ip_url':unit_ip_url,
            'image':image,
        }))
        
        ### under contruction ####      
        
    #for messages sent from units
    #put 'unit_message' as type
    #put device info message is coming in unit_id and unit
    #put action type as action (logging)
    async def unit_message(self, event):
        type = event['type']
        action = event['action']
        status = event['status']
        unit_id = event['unit_id']
        unit_ip_url = event['unit_ip_url']
        image = event['image']
        
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': type,
            'action':action,
            'status':status,
            'unit_id':unit_id,
            'unit_ip_url':unit_ip_url,
            'image':image,
        }))