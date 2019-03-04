#ifndef __WIFI_UTILS__
#define __WIFI_UTILS__

#include <Arduino.h>
#include <HardwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

const int WIFI_TIMEOUT = 2000;

const int WIFI_CONNECTION_TRIALS = 30;

bool startWiFi(ESP8266WiFiMulti &WiFiMulti,const char * ssid, const char * pwd);

bool sendStringToServer(ESP8266WiFiMulti &WiFiMulti,const String &server_url,const String &s, bool verb = true);

bool sendJSONToServer(ESP8266WiFiMulti &WiFiMulti,const String &server_url,const JsonObject &jsonobj, bool verb = true);

bool sendJSONToServer(ESP8266WiFiMulti &WiFiMulti,const String &server_url,const String &s, bool verb = true);

#endif
