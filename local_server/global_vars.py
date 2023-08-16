
from decouple import config

def init():
    #household identification used for adding alerts and error logs
    global household_id
    household_id_env = config('householdId')
    household_id = int(household_id_env)
    
    #variables to identify local server unit
    global server_id
    server_id_env = config('serverId')
    server_id = str(server_id_env) #edit this to  match up with server ID in the database
    
    #variables for creating local ws server
    global PATH
    PATH = config("LOCAL_SERVER_IP")
    global PORT
    PORT = 8080
    
    #local server url
    global LOCAL_WS_SERVER 
    LOCAL_WS_SERVER = f'ws://{PATH}{PORT}/'
    
    #remote socket instance
    global remoteSocket
    remoteSocket = {'socket':False, 'connected':False}
    
    #handle keeping track of all sockets connected to local server
    #and information about them
    global localSockets
    localSockets = {}

    #keep track of global tasks that need to be awaited in main program
    #asigning them to a global variable keeps the streams and other tasks
    #from delaying other operations in the program
    global global_tasks
    global_tasks = []
    
    #keep track of global processes not involving camera streams or
    #camera stream relays
    global global_processes
    global_processes = []
    
    #keep track of all global errors
    global error_logs
    error_logs = []
    
    #keep track of all alerts from units
    global alerts
    alerts = {}
    
    #remote server api paths
    global remoteServerApi
    faceRecListUrl = config('getFaceRecognitionList')
    createAlertUrl = config('createAlert')
    createErrorLogUrl =config('createErrorLog')
    remoteServerApi = {
        'getFaceRecognitionList' : f'{faceRecListUrl}{household_id}/',
        'createAlert' : f'{createAlertUrl}{household_id}/',
        'createErrorLog':f'{createErrorLogUrl}{server_id}/',
        
    }
    
    #variables for connecting to remote ws server
    global remoteWsUrl
    remoteWsUrlEnv = config('remoteWsUrl')
    remoteWsUrl = remoteWsUrlEnv
    
    #stores face encodings for people in high alert list
    global high_alert_face_encodings
    high_alert_face_encodings = []
    
    #stores face encodings for people in allowed list
    global allowed_face_encodings
    allowed_face_encodings = []
    
    #keep track if face encodings for face recognition have loaded
    #into global variables
    global face_encoding_tasks
    face_encoding_tasks = {'allowed':False, 'high_alert':False}
    
    #Keep track of last recorded alert to prevent creating too many alerts back to back
    global last_alert_frame_count
    last_alert_frame_count = 0