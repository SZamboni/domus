#include "wifi_utils.h"

/**
 * Function that starts the wifi module and tries to connect to the network
 * 
 * @param WiFiMulti : the WiFiMulti instance used to connect to the network
 * 
 * @return: true if the connection is successful, false otherwise
 */
bool startWiFi(ESP8266WiFiMulti &WiFiMulti,const char * ssid, const char * pwd) {

  WiFiMulti.addAP(ssid,pwd);

  // try to connect for WIFI_CONNECTION_TRIALS times, one 0.5 sec from the other
  int trials = 0;
  while (WiFiMulti.run() != WL_CONNECTED && trials < WIFI_CONNECTION_TRIALS) {
    delay(500);
    Serial.print(".");
    trials++;
  }
  Serial.println("");

  if(trials == WIFI_CONNECTION_TRIALS) {  // connection failed
    Serial.print("Unable to connect to the network named ");
    Serial.print(ssid);
    Serial.print(" with password ");
    Serial.println(pwd);
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
bool sendStringToServer(ESP8266WiFiMulti &WiFiMulti, const String &server_url, const String &s) {

  if(( WiFiMulti.run() == WL_CONNECTED)) {
    HTTPClient httpclient;
    httpclient.setTimeout(WIFI_TIMEOUT);

    Serial.println("Starting http request to:");
    
    httpclient.begin(server_url);

    int httpCode = httpclient.POST(s);

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
bool sendJSONToServer(ESP8266WiFiMulti &WiFiMulti, const String &server_url, const JsonObject &jsonobj) {

  if(( WiFiMulti.run() == WL_CONNECTED)) {
    HTTPClient httpclient;
    httpclient.setTimeout(WIFI_TIMEOUT);

    Serial.println("Starting http request to:");
    
    httpclient.begin(server_url);
    httpclient.addHeader("Content-Type", "application/json");

    String s_to_send = "";
    jsonobj.printTo(s_to_send);
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
bool sendJSONToServer(ESP8266WiFiMulti &WiFiMulti, const String &server_url, const String &s) {

  if(( WiFiMulti.run() == WL_CONNECTED)) {
    HTTPClient httpclient;
    httpclient.setTimeout(WIFI_TIMEOUT);

    Serial.println("Starting http request to:");
    
    httpclient.begin(server_url);
    httpclient.addHeader("Content-Type", "application/json");

    Serial.println("Sendind:");
    Serial.println(s);
    int httpCode = httpclient.POST(s);

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
