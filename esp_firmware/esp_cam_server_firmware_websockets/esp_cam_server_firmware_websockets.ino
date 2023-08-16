#include "esp_camera.h"
#include <WiFi.h>
#include "defines.h"
#include <ArduinoJson.h>
#define CAMERA_MODEL_AI_THINKER

#include "camera_pins.h"

// for websockets connection
#include <WebSockets2_Generic.h>
using namespace websockets2_generic;
WebsocketsClient client;

//max size of json doc for socket payloads
const uint8_t max_json_size = JSON_OBJECT_SIZE(600);

//unit_identification variables
char* unit_id = "2";
bool initial_powerup = true;

//for static ip
// Set your Static IP address
//IPAddress local_IP(192, 168, 1, 184);
// Set your Gateway IP address
//IPAddress gateway(192, 168, 1, 1);

//IPAddress subnet(255, 255, 0, 0);
//IPAddress primaryDNS(8, 8, 8, 8);   //optional
//IPAddress secondaryDNS(8, 8, 4, 4); //optional

//String IpAdressToString(ip){
  //return String(ip[0]) + String(".") + 
  //String(ip[1]) + String(".") + 
  //String(ip[2]) + String(".") + 
  //String(ip[3]);
//}


void onEventsCallback(WebsocketsEvent event, String data) 
{
  (void) data;
  
  if (event == WebsocketsEvent::ConnectionOpened) 
  {
    Serial.println("Connnection Opened");
    //on websocket connection to homeserver, send device information to home server 
    String ip = WiFi.localIP().toString();

    StaticJsonDocument<max_json_size> initial_message;
    initial_message["type"] = "unit_info";
    initial_message["status"] = "online";
    initial_message["unit_id"] = unit_id;
    initial_message["ip_url"] = ip;
    initial_message["unit_type"] = "camera";

    char initial_payload[100];
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
  else{
    Serial.println("no action");
  }
}




void startCameraServer();

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.frame_size = FRAMESIZE_UXGA;
  config.pixel_format = PIXFORMAT_JPEG; // for streaming
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count = 1;
  
  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if(config.pixel_format == PIXFORMAT_JPEG){
    if(psramFound()){
      config.jpeg_quality = 10;
      config.fb_count = 2;
      config.grab_mode = CAMERA_GRAB_LATEST;
    } else {
      // Limit the frame size when PSRAM is not available
      config.frame_size = FRAMESIZE_SVGA;
      config.fb_location = CAMERA_FB_IN_DRAM;
    }
  } else {
    // Best option for face detection/recognition
    config.frame_size = FRAMESIZE_240X240;
#if CONFIG_IDF_TARGET_ESP32S3
    config.fb_count = 2;
#endif
  }


  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t * s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  if(config.pixel_format == PIXFORMAT_JPEG){
    s->set_framesize(s, FRAMESIZE_QVGA);
  }

#if defined(CAMERA_MODEL_M5STACK_WIDE) || defined(CAMERA_MODEL_M5STACK_ESP32CAM)
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);
#endif

#if defined(CAMERA_MODEL_ESP32S3_EYE)
  s->set_vflip(s, 1);
#endif

// if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
  //  Serial.println("STA Failed to configure");
  //}

  WiFi.begin(ssid, password);
  WiFi.setSleep(false);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".wsssss");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  startCameraServer();

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");

  //for websockets connection and functionality
   // run callback when messages are received
  client.onMessage([&](WebsocketsMessage message) 
  {
    Serial.print("Got Message: ");
    Serial.println(message.data());

    //deserialize message from home server
    StaticJsonDocument<max_json_size> mData;
    DeserializationError error = deserializeJson(mData, message.data());
  
    if(error){
    Serial.println("error parsing message");
    Serial.println(error.f_str());
    return;
    } 

    //in case message was sent to wrong unit
    if(mData["unit_id"] != unit_id){return;}

  });

  // run callback when events are occuring
  client.onEvent(onEventsCallback);
  
  // try to connect to Websockets server
  bool connected = client.connect(websockets_server_host, websockets_server_port, "/");
  
  if (connected) 
  {
    Serial.println("Connected!");
  } 
  else 
  {
    Serial.println("Not Connected!");
  }
}

void loop() {

    if (client.available()) 
    {
      client.poll();
    }
  delay(10000);
}
