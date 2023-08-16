from requests import get
import global_vars as gv
import os
from urllib.parse import urlparse
from boto3 import client, resource
from decouple import config
from read_cam_feeds import read_camera_stream
from multiprocessing import Process

gv.init()

#for accessing photographs from S3 buckets for facial recognition
AWS_SECRET = config('AWS_SECRET_KEY')
AWS_ACCESS = config('AWS_ACCESS_KEY')

S3CLIENT = client('s3', aws_access_key_id=AWS_ACCESS, aws_secret_access_key=AWS_SECRET)
S3 = resource('s3') 

S3BUCKET = config('AWS_S3_BUCKET_NAME')
ALLOWED_PATH = config('AWS_ALLOWED_PERSONS')



# delete object from s3 bucket
def delete_allowed_person(all = False, key=None):
    #if deleting all allowed persons
    if all:
        for file in os.listdir('./images/allowed_persons/'):
            #remove from local directory
            basename = os.path.basename(file)
            s3_file_path = f"{ALLOWED_PATH}{basename}"
            local_file_path = f'./images/allowed_persons/{basename}'
            
            #remove from s3 bucket
            try:
                S3CLIENT.delete_object(Bucket=S3BUCKET, Key = s3_file_path)
            except:
                pass
            if os.path.exists(local_file_path):
                os.remove(local_file_path)
        return
    
    #if only deleting one person
    s3_file_path = f"{ALLOWED_PATH}{key}"
    local_file_path = f'./images/allowed_persons/{key}'
    
    #remove from local directory
    if os.path.exists(local_file_path):
        os.remove(local_file_path)
    
    #remove from s3 bucket
    try:
        S3CLIENT.delete_object(Bucket=S3BUCKET, Key = s3_file_path)
    except:
        pass


#update images for allowed and high alert people
def update_persons():
    #get data from api
    #response structure:
    # {'allowed':[list of allowed persons], 
    # {'high_alert':[list of high alert persons]}
    r = get(gv.remoteServerApi['getFaceRecognitionList'])
    
    if r.status_code != 200:
        return

    data = r.json()
    
    #for storing filenames of persons stored locally
    cached_faces = []
    # for storing filnames of persons from remote server
    cached_faces_updated_list = []
    
    for file in os.listdir('./images/allowed_persons/'):
        basename = os.path.basename(file)
        cached_faces.append(basename)
        
    #if there are no allowed persons for household
    #delete all current files
    if len(data['allowed']) == 0 and len(cached_faces) > 0:
        delete_allowed_person(all=True)
    
    #iterate through list of allowed persons from api
    if len(data['allowed']) > 0:
        for p in data['allowed']:
            url_parsed = urlparse(p['pic'])

            name = os.path.basename(url_parsed.path)
            
            #used for later image deletion and cleanup
            cached_faces_updated_list.append(name)

            #if file is not already stored locally
            if name not in cached_faces:
                with open(f"./images/allowed_persons/{name}", "wb") as file:
                    s3_file_path = f"{ALLOWED_PATH}{name}"
                    try:
                        S3CLIENT.download_fileobj(S3BUCKET, s3_file_path, file)
                        file.close()
                    except:
                        file.close()
                        os.remove(f"./images/allowed_persons/{name}")

        for old_key in cached_faces:
            if old_key not in cached_faces_updated_list:
                delete_allowed_person(key = old_key)      

def update_face_encodings():
    #update locally stored files to reflect changes
    update_persons()
    
    #iterate through all connected camera's and kill their outdated stream process
    # create new stream process, this will update stored face encodings for
    # facial recognition
    for key, unit in gv.localSockets.items():
        
        if unit['unit_type'] == 'camera':
            #stop current stream process
            gv.localSockets[key]['stream_process'].terminate()
            gv.localSockets[key]['stream_process'] = None
            
            # handle rebooting camera stream
            cam_class = read_camera_stream(gv.localSockets[key])
            p = Process(target = cam_class.run, args = [], daemon=True)
            p.start()   
            
            gv.localSockets[key]['stream_process'] = p
            
                      
if __name__ == '__main__':
    update_persons()
    
    
