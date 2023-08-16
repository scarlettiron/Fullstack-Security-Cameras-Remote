import json
from logging import raiseExceptions
import global_vars as gv
from requests import post
import json
import cv2 as cv
from random import randint
import pendulum


gv.init()


#correctly formats message to be sent to remote SOCKET server, returns payload
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


class Alerts:
    def __init__(self, alert = None, type = 'intruder', unit_id = None, 
                 img = None, img_path = None, description = None, high_alert = False):
        self.alert = alert
        self.type = type
        self.unit_id = unit_id
        self.img = img
        self.img_path = img_path
        self.description = description
        self.high_alert = high_alert
     
     
    def format_alert_payload(self, alert):
        payload = {
            'description' : alert['description'],
            'unit_id' : alert['device'],
            'date' : alert['date'],
            'type' : alert['type'],
        }
        
        return payload
       
    #all alerts are appended to a global list and written to a txt file
    # in case of an error when sending to server
    def create_alert(self):
        
        #reset last frame count to allow
        if gv.localSockets[self.unit_id]['unit_type'] == 'camera' and gv.last_alert_frame_count >= 5:
            gv.last_alert_frame_count = 0
            return
            
        try:
            #handle saving image if any
            if self.img.any():
                file_id_txt = randint(1, 6000)
                filename = f"{self.type}_{file_id_txt}"
                path = f'./alerts/alert_images/{filename}.png'
                cv.imwrite(path, self.img)
                self.img_path = path
                
            #handle saving rest of alert data to txt file
            #this is structured to be sent to the remote servers api, 
            # not through sockets
            date = pendulum.now('utc').to_iso8601_string()
            
            alert = {
                'type':self.type,
                'date':date,
                'device':self.unit_id,
                'img_path':self.img_path,
                'description':self.description
            }
            
            #append to global list of alerts
            alert_id = randint(1, 10000)
            gv.alerts[alert_id] = alert
            self.alert = alert
            
            #append to list of alerts in txt file,
            #this is so alerts can be sent to remote api 
            #with a different background process
            with open('./alerts/alert_list.txt', 'r+') as alerts:
                lines = alerts.readlines()
                if len(lines) == 0:
                    alert_dict = {alert_id:alert}
                else:
                    alert_dict = json.loads(lines[0])
                    alert_dict[alert_id] = alert
                
                alert_dict = json.dumps(alert_dict)
                
                alerts.seek(0)
                alerts.writelines([alert_dict]) 
                alerts.truncate()
                alerts.close()

            #increase last alert frame count to prevent alert creation
            #spamming
            if gv.localSockets[self.unit_id]['unit_type'] == 'camera':
                gv.last_alert_frame_count += 1
                    
            return self
        
        except:
            raise Exception('error creating alert')
             
                
    
    #in case request fails at current time, alerts stay in global variable until
    #later time when they can be succesfully sent                
    def send_alert_list_to_remote_api(self):
        alerts_map = None
        sucessfully_sent = []
        null = None
        with open('./alerts/alert_list.txt', 'r+') as als:
            lines = als.readlines()
            if len(lines) == 0:
                als.close()
                return
            alerts_map = json.loads(lines[0])
        
            #if there are no alerts, exit out
            if not alerts_map or len(alerts_map) == 0:
                return
            
            for key, value in alerts_map.items():
                #if alert contains an image
                file = None
                payload = self.format_alert_payload(value)
                
                if 'img_path' in value:
                    file = open(value['img_path'], 'rb')
                
                r = post(gv.remoteServerApi['createAlert'], data = payload, files = {'image':file})
                file.close()
                
                print(r.status_code) 
                # request was succesfull remove from alert_list, else
                #keep in list for retrying later
                if r.status_code == 201:
                    sucessfully_sent.append(key)
                #remove successfully sent alerts from alerts map
            for ss in sucessfully_sent:
                alerts_map.pop(ss)
            
            #reset file pointer to beginning of alerts_list.txt file
            als.seek(0)      
            
            #if all alerts were not successfully sent, add to back txt file
            if len(alerts_map) != 0:
                alerts_txt = json.dumps(alerts_map)
                als.writelines([alerts_txt])
                als.truncate()
            
            #if all alerts were sent, clear alerts_list.txt
            else:
                als.truncate(0)
                
            #close file before exiting
            als.close()
        return self
    
    def send_immediate_alert(self):
        self.send_alert_list_to_remote_api() 
    
    
    #this structored to be sent through sockets not to the api    
    async def send_socket_alert(self):
        if not self.alert:
            raiseExceptions('alert not provided use func create_alert first')
            return
        if not gv.remoteSocket['connected']:
            raiseExceptions('not connected to remote server, try later')
            return

        socket_payload = format_message({
            'type':'alert',
            'action':self.alert.type,
            'unit_id':self.alert.device
        })
        await gv.remoteSocket['socket'].send(socket_payload)
                    
                
                    
            
            
            