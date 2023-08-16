from asyncio.windows_events import NULL
import global_vars as gv
from datetime import datetime as dt
from requests import post
import json
from random import randint
import pendulum


gv.init()

class Error_Logs:
    
    def __init__(self, error = NULL):
        self.error = error

    def create_error_log(type, description, unit, server):
        date = pendulum.now('utc').to_iso8601_string()
        error = json.dumps({
            'type':type,
            'description':description,
            'device':unit,
            'server':server,
            'date':date
        })
        
        print(error)
        
        #add error to gloabl error logging list
        gv.error_logs.append(error)
        
        #add error to error logging txt to be accessed by seperate background
        #processes
        with open('./error_logging/error_logs.txt', 'a') as els:
            els.writelines([error])
        els.close()

    
    def send_error_logs(self):
        payload = None
        with open('./error_logging/error_logs.txt', 'r') as els:
            txt_errors = els.readlines()
            if len(txt_errors) == 0:
                els.close()
                return
            els.close()
            
            payload = eval(txt_errors[0])
            
            r = post(gv.remoteServerApi['createErrorLog'], data = payload)
            if r.status_code == 201:
                gv.error_logs = []
            #DELETE ALL ERROR LOGS AND CLOSE FILE
            
            els.close()