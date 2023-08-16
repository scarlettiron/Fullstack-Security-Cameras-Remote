import json
from requests import request, post
import global_vars as gv

gv.init()

testAlert = [{'device':'2','type':'intruder', 'path':'./images/scarlett1.jpg'}]

def send_alerts():
    
    file = open(testAlert[0]['path'], 'rb')
    print(file)
    ''' payload = json.dumps(testAlert[0])
    r = post(gv.remoteServerApi['createAlert'], data = testAlert[0], files = {'image':file})
    print(r.text) '''

def create_alert():
    print('creating')
    with open('../alerts/alert_list.txt', 'a') as al:
        alert = json.dumps(testAlert)
        al.writelines([alert, ","]) 
        al.close()
    print('created')   
        
def read_alerts():
    with open('./alerts/alert_list.txt', 'r') as al:
        alerts = al.readlines()
        vals = eval(alerts[0])
        str_vals = json.dumps(vals)
        print(str_vals)
        
        
def read_and_send_multiple_alerts():
    alert_list = []
    payload = []
    with open('./alerts/alert_list.txt', 'r') as al:
        alerts = al.readlines()
        for a in alerts:
            a_evaled = eval(a)
            alert_list.append(a_evaled)
            
    al.close()
    
    for a in alert_list:
        if a['img_path']:
            file = open(a['img_path'], 'rb')
            a['file'] = file
        payload.append(a)
    
    r = post(gv.remoteServerApi['createAlert'], data = testAlert[0], files = {'image':file})
    print(r.text)
    
    
        
        
if __name__ == '__main__':
    send_alerts()
    