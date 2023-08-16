/****************************************************************************************************************************
  ESP8266-Client.ino
  For ESP8266.

  original websocket library: Gil Maimon's ArduinoWebsockets library https://github.com/gilmaimon/ArduinoWebsockets
  modified websockets client by: Khoi Hoang https://github.com/khoih-prog/Websockets2_Generic
  Licensed under MIT license

  all initial lock firmware created by: Scarlett
 *****************************************************************************************************************************/
/****************************************************************************************************************************
  This sketch:
        1. Connects to a WiFi network
        2. Connects to a Websockets server
        3. Sends unit info to home server upon connection open
        4. Processes and completes actions sent from remote server or home server

  Hardware:
        For this sketch you need: an ESP8266 board, 

*****************************************************************************************************************************/

#include "defines.h"

#include <WebSockets2_Generic.h>
#include <ESP8266WiFi.h>
//#include <ESP8266WiFiMulti.h>
#include <WiFiClient.h>
//#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <String.h>
#include <Vector.h>
 #include "RestClient.h"


using namespace websockets2_generic;


//unit_identification variables
char  *unit_id = "2";
bool initial_powerup = true;

//wifi and websocket setup
char *ws_server_path = "ws://192.168.2.7:8080/";
char* remote_server = "192.168.2.7";
int remote_port = 8000;

//for websockets
WebsocketsClient client;
//for getting and posting data
RestClient rClient = RestClient(remote_server, remote_port);
String response;

//variables for lock status and pins
bool is_locked = false;
int forwards = 4;
int backwards = 5;
int motor_run_time = 3000;

//keypad variables
//store all lockcodes for unit
//char* lock_codes[50] = {"1212", "3443"};
//std::vector<char*> lock_codes;
String storage_array[10];
Vector<String> lock_codes(storage_array);
//Array<char*, 10> lock_codes;
//master lock code
String master_code = "2222";
//keypad wire pins
int LockBtn = 16;
int UnlockBtn = 3;
int btnA = 15;
int btnB = 13;
int btnC = 12;
int btnD = 14;
int btnE = 2;

//when key is pressed add this to array
String keypad_entries = "";
int max_passcode_length = 4;
// keep track of the time of the last entry
int last_time;
//in milliseconds
int clear_key_entry_wait = 3000;


//max size of json doc for socket payloads
const uint8_t max_json_size = JSON_OBJECT_SIZE(200);


//manually locks deadbolt when pressed if deadbolt is unlocked
//will reset user inputted keypad entries if deadbolt is already locked
void lock_deadbolt(){
    if(is_locked == false){
      Serial.println("locking");
      digitalWrite(forwards, HIGH);
      delay(motor_run_time);
      digitalWrite(forwards, LOW);
      is_locked = true;
    }
    return;
}

//unlocks deadbolt 
void unlock_deadbolt(){
  if(is_locked == true){
    Serial.println("unlocking");
    digitalWrite(backwards, HIGH);
    delay(motor_run_time);
    digitalWrite(backwards, LOW);
    is_locked = false;
    keypad_entries = "";
  }
  return;
}

//for unlocking and unlocking deadbolt remotely
void lock_unlock_deadbolt(String action){
 if(is_locked == true && action == "unlock"){
  unlock_deadbolt();
 }
 else if(is_locked == false && action == "lock"){
  lock_deadbolt();
 }
  return;
}



void onEventsCallback(WebsocketsEvent event, String data) 
{
  (void) data;
  Serial.println(data);
  
  if (event == WebsocketsEvent::ConnectionOpened) 
  {
    Serial.println("Connnection Opened");
    
    //on websocket connection to homeserver, send device information to home server 
    StaticJsonDocument<max_json_size> initial_message;
    initial_message["type"] = "unit_info";
    initial_message["status"] = is_locked ? "locked" : "unlocked";
    initial_message["unit_id"] = unit_id;

    char initial_payload[55];
    size_t payload_len = serializeJson(initial_message, initial_payload);
    client.send(initial_payload, payload_len);
    
  } 
  else if (event == WebsocketsEvent::ConnectionClosed) 
  {
    Serial.println("Connnection Closed");
  } 
  else if (event == WebsocketsEvent::GotPing) 
  {
    Serial.println("Got a Ping!");
  } 
  else if (event == WebsocketsEvent::GotPong) 
  {
    Serial.println("Got a Pong!");
  }


}

//fetch passcodes from remote server and add to lock_codes array
void fetch_passcodes(){
  response = "";
  int statusCode = rClient.get("/api/devices/unit-pwd/2/", &response);

  if(statusCode > 0){
    DynamicJsonDocument payload(1024);
    deserializeJson(payload, response);
    if(payload["count"] > 0){
       for(int x = 0; x < std::size(payload["results"]); x++){
            String formated_passcode = format_passcode(payload["results"][x]["code"]);
            lock_codes.push_back(formated_passcode);
          }
      }
  }
}

//format passcodes
String format_passcode(int inp_array){
    std::string tmp = std::to_string(inp_array);
    String code_array = tmp.c_str();
    String formated_code = "";
    
     for(int x = 0; x < code_array.length(); x++){
        if(code_array[x] >= '1' && code_array[x] <= '2'){
            formated_code.concat('1');
          }
        else if(code_array[x] > '2' && code_array[x] <= '4'){
          formated_code.concat('2');
        }
        else if(code_array[x] > '4' && code_array[x] < '6'){
          formated_code.concat('3');
        }
        else if(code_array[x] >  '6' && code_array[x] < '8'){
          formated_code.concat('4');
        }
        else if(code_array[x] == '9' || code_array[x] == '0'){
          formated_code.concat('5');
        }
    }
    return formated_code;
}


//handle passcode entries
//under costruction//
void handle_keypad_entries(int btn){
    //if user inputted keypad entries have exceeded maximum length, reset.
    if(keypad_entries.length() >= max_passcode_length){
        keypad_entries = "";
    }

    if(btn == btnA){
        keypad_entries.concat('1');
    }
    if(btn == btnB){
        keypad_entries.concat('2');
    }
    else if(btn == btnC){
        keypad_entries.concat('3');
    }
    else if(btn == btnD){
        keypad_entries.concat('4');
    }
     else if(btn == btnE){
        keypad_entries.concat('5');
    }

    if(keypad_entries.length() > 0){
        check_lock_code();
      } 
     delay(500);
    return;
}


//check to see if correct keypad code has been entered
void check_lock_code(){
  if(keypad_entries == master_code){
      unlock_deadbolt();
      return;
    }
    
  for(int x = 0; x < std::size(lock_codes); x++){
    if(lock_codes[x] == keypad_entries){
      unlock_deadbolt();
      break;
    }
  }
    return;
}


void setup() 
{
  Serial.begin(115200);
  //Serial.begin(57600);
  while (!Serial && millis() < 5000);

  Serial.print("\nStart ESP8266-Client on "); Serial.println(ARDUINO_BOARD);
  Serial.println(WEBSOCKETS2_GENERIC_VERSION);

  //set pins for deadbolt motor
  pinMode(forwards, OUTPUT);
  pinMode(backwards, OUTPUT);

  //set pins for keypad
  pinMode(LockBtn, INPUT);
  pinMode(UnlockBtn, INPUT);
  pinMode(btnA, INPUT); 
  pinMode(btnB, INPUT); 
  pinMode(btnC, INPUT); 
  pinMode(btnD, INPUT); 
  pinMode(btnE, INPUT);
  
  // Connect to wifi
  WiFi.begin(ssid, password);

  // Wait some time to connect to wifi
  for (int i = 0; i < 10 && WiFi.status() != WL_CONNECTED; i++) 
  {
    Serial.print(".");
    delay(1000);
  }

  // Check if connected to wifi
  if (WiFi.status() != WL_CONNECTED) 
  {
    Serial.println("No Wifi!");
    return;
  }

  //for api
  rClient.begin(ssid, password);
  
  Serial.print("Connected to Wifi, Connecting to WebSockets Server @");
 
  // run callback when messages are received
  client.onMessage([&](WebsocketsMessage sMessage) 
  {
    Serial.print("Got Message: ");
    Serial.println(sMessage.data());

    //deserialize message from home server
    StaticJsonDocument<300> mData;
    DeserializationError error = deserializeJson(mData, sMessage.data());
  
    if(error){
    Serial.println("error parsing message");
    Serial.println(error.f_str());
    return;
    } 

    
    //just in case message was sent to the wrong unit
    if(mData["unit_id"] != unit_id){return;}
    
    if(mData["type"] == "ping"){
      StaticJsonDocument<max_json_size> message;
      message["type"] = "pong";
      message["status"] = is_locked ? "locked" : "unlocked";
      message["unit_id"] = unit_id;

      char payload[55];
      size_t payload_len = serializeJson(message, payload);
      client.send(payload, payload_len); 
      }
    else if(mData["type"] == "command"){
      if(mData["action"] == "update"){
        fetch_passcodes();
        }
      else{
        lock_unlock_deadbolt(mData["action"]);
      }
    }
    return;
  });

  // run callback when events are occuring
  client.onEvent(onEventsCallback);
  //for websockets
  bool connected = client.connect(ws_server_path);
  
  if (connected) 
  {
    Serial.println("Connected!");


  } 
  else 
  {
    Serial.println("Not Connected!");
  }
}

void loop() 
{


  // fetch unit passcodes
  if(initial_powerup == true){
      if (WiFi.status() == WL_CONNECTED){
        fetch_passcodes();
        initial_powerup = false;
        }
      }
  
  

   //After clear_key_entry_wait has been met, reset keypad entries
   if(last_time == clear_key_entry_wait && keypad_entries.length() > 0){
    keypad_entries = "";
   }
  // increase last_time variable every loop, after this has increased so many times, keypad_entries will be reset
   last_time += 1;


    // manually lock deadbolt when pressed
   if(digitalRead(LockBtn) == HIGH){
    lock_deadbolt();
   }

   if(digitalRead(UnlockBtn) == HIGH){
    unlock_deadbolt();
   }

  //handle btn states if pressed
   if(digitalRead(btnA) == HIGH){
    handle_keypad_entries(btnC);
   }

   if(digitalRead(btnB) == HIGH){
    handle_keypad_entries(btnB);
   }
  
   if(digitalRead(btnC) == HIGH){
    handle_keypad_entries(btnC);
   }

   
   if(digitalRead(btnD) == HIGH){
    handle_keypad_entries(btnD);
   }
   
   if(digitalRead(btnE) == HIGH){
    handle_keypad_entries(btnE);
   }
  
  // let the websockets client check for incoming messages
  if (client.available()) 
  {
    client.poll();
  }

  delay(100);
}
