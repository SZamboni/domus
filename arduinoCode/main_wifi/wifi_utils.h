#ifndef __WIFI_UTILS__
#define __WIFI_UTILS__

#include <Arduino.h>
#include <HardwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

const String WIFI_SERVER_URL = "http://192.168.1.69:3000/";
const int WIFI_TIMEOUT = 2000;

const int WIFI_CONNECTION_TRIALS = 20;

bool startWiFi(ESP8266WiFiMulti *WiFiMulti);

bool sendStringToServer(ESP8266WiFiMulti *WiFiMulti,String* s);

bool sendJSONToServer(ESP8266WiFiMulti *WiFiMulti,JsonObject* jsonobj);

bool sendJSONToServer(ESP8266WiFiMulti *WiFiMulti,String* s);

#endif
