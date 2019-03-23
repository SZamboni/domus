#include "wifi_utils.h"

const char * WIFI_UTILS_SSID = "FASTWEB-1-1FAA45";
const char * WIFI_UTILS_PASSWORD = "77861704BB";

/**
 * Function that starts the wifi module and tries to connect to the network
 * 
 * @param WiFiMulti : the WiFiMulti instance used to connect to the network
 * 
 * @return: true if the connection is successful, false otherwise
 */
bool startWiFi(ESP8266WiFiMulti *WiFiMulti) {

  WiFiMulti->addAP(WIFI_UTILS_SSID,WIFI_UTILS_PASSWORD);

  // try to connect for WIFI_CONNECTION_TRIALS times, one 0.5 sec from the other
  int trials = 0;
  while (WiFiMulti->run() != WL_CONNECTED && trials < WIFI_CONNECTION_TRIALS) {
    delay(500);
    Serial.print(".");
    trials++;
  }
  Serial.println("");

  if(trials == WIFI_CONNECTION_TRIALS) {  // connection failed
    Serial.print("Unable to connect to the network named ");
    Serial.print(WIFI_UTILS_SSID);
    Serial.print(" with password ");
    Serial.println(WIFI_UTILS_PASSWORD);
    return false;
  } 

  // connection suceeded
  Serial.print("WiFi connected, ");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  return true;
  
}

/**
 * Function that sends a string to the server
 * 
 * @param WiFiMulti : the WiFiMulti instance used to connect to the network
 * @param s : string to send
 * 
 * @return: true if the sending is successful, false otherwise
 */
bool sendStringToServer(ESP8266WiFiMulti *WiFiMulti, String* s) {

  if(( WiFiMulti->run() == WL_CONNECTED)) {
    HTTPClient httpclient;
    httpclient.setTimeout(WIFI_TIMEOUT);

    Serial.println("Starting http request to:");
    
    httpclient.begin(WIFI_SERVER_URL);

    int httpCode = httpclient.POST(*s);

    if(httpCode > 0) {
      Serial.print("Server response code: ");
      Serial.println(httpCode);

      if(httpCode == HTTP_CODE_OK) {
          String payload = httpclient.getString();
          Serial.println("Response body: ");
          Serial.println(payload);
      }
      return true;
    } else {
      Serial.print("Connection Error: ");
      Serial.println(httpclient.errorToString(httpCode).c_str());
      return false;
    }
    
  } else {
    return false;
  }
  
}

/**
 * Function that sends a JsonObject to the server
 * 
 * @param WiFiMulti : the WiFiMulti instance used to connect to the network
 * @param jsonobj : JsonObject that will be converted in string to send
 * 
 * @return: true if the sending is successful, false otherwise
 */
bool sendJSONToServer(ESP8266WiFiMulti *WiFiMulti,JsonObject* jsonobj) {

  if(( WiFiMulti->run() == WL_CONNECTED)) {
    HTTPClient httpclient;
    httpclient.setTimeout(WIFI_TIMEOUT);

    Serial.println("Starting http request to:");
    
    httpclient.begin(WIFI_SERVER_URL);
    httpclient.addHeader("Content-Type", "application/json");

    String s_to_send = "";
    jsonobj->printTo(s_to_send);
    Serial.println("Sendind:");
    Serial.println(s_to_send);
    int httpCode = httpclient.POST(s_to_send);

    if(httpCode > 0) {
      Serial.print("Server response code: ");
      Serial.println(httpCode);

      if(httpCode == HTTP_CODE_OK) {
          String payload = httpclient.getString();
          Serial.println("Response body: ");
          Serial.println(payload);
          httpclient.end();
          return true;
      }
      httpclient.end();
      return false;
    } else {
      Serial.print("Connection Error: ");
      Serial.println(httpclient.errorToString(httpCode).c_str());
      httpclient.end();
      return false;
    }
    
  } else {
    return false;
  }
  
}

/**
 * Function that sends a JsonObject to the server
 * 
 * @param WiFiMulti : the WiFiMulti instance used to connect to the network
 * @param s : string to send
 * 
 * @return: true if the sending is successful, false otherwise
 */
bool sendJSONToServer(ESP8266WiFiMulti *WiFiMulti,String* s) {

  if(( WiFiMulti->run() == WL_CONNECTED)) {
    HTTPClient httpclient;
    httpclient.setTimeout(WIFI_TIMEOUT);

    Serial.println("Starting http request to:");
    
    httpclient.begin(WIFI_SERVER_URL);
    httpclient.addHeader("Content-Type", "application/json");

    Serial.println("Sendind:");
    Serial.println(*s);
    int httpCode = httpclient.POST(*s);

    if(httpCode > 0) {
      Serial.print("Server response code: ");
      Serial.println(httpCode);

      if(httpCode == HTTP_CODE_OK) {
          String payload = httpclient.getString();
          Serial.println("Response body: ");
          Serial.println(payload);
          httpclient.end();
          return true;
      }
      httpclient.end();
      return false;
    } else {
      Serial.print("Connection Error: ");
      Serial.println(httpclient.errorToString(httpCode).c_str());
      httpclient.end();
      return false;
    }
    
  } else {
    return false;
  }
  
}
