/**
 * BasicHTTPClient.ino
 *
 *  Created on: 24.05.2015
 *
 */

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

#define USE_SERIAL Serial

#include "test.h"

ESP8266WiFiMulti WiFiMulti;

void setup() {

    testfun();
    cppfunction();
    
    USE_SERIAL.begin(115200);
    USE_SERIAL.setDebugOutput(true);

    WiFiMulti.addAP("Redmi Simone", "ciaociao"); //WiFiMulti.addAP("FASTWEB-1-1FAA45", "77861704BB"); 
  
    //while (WiFi.status() != WL_CONNECTED) {
    while (WiFiMulti.run() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
  
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

}

void loop() {
  testfun();
  cppfunction();
  Serial.println(AA);
    // wait for WiFi connection
    if((WiFiMulti.run() == WL_CONNECTED)) {

        HTTPClient http;
        http.setTimeout(2000);

        USE_SERIAL.print("[HTTP] begin...\n");
        // configure traged server and url
        http.begin("192.168.43.78", 3000, "/");
        http.addHeader("Content-Type", "application/json");


        USE_SERIAL.print("[HTTP] GET...\n");
        // start connection and send HTTP header
        int httpCode = http.POST("{ \"name\":\"value\" }");

        // httpCode will be negative on error
        if(httpCode > 0) {
            // HTTP header has been send and Server response header has been handled
            USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode);

            // file found at server
            if(httpCode == HTTP_CODE_OK) {
                String payload = http.getString();
                USE_SERIAL.println(payload);
            }
        } else {
            USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        }

        http.end();
    }

    delay(10000);
}
