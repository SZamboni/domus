#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ArduinoJson.h>

#ifndef STASSID
#define STASSID "FASTWEB-1-1FAA45"
#define STAPSK  "77861704BB"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

ESP8266WebServer server(80);

void getRequestInfo() {
  Serial.print("Method: ");
  Serial.println(server.method());
  Serial.print("Arguments: ");
  Serial.println(server.args());
  for (int i = 0; i < server.args(); i++) {
    Serial.print("Argument n° ");
    Serial.print(i);
    Serial.print(" name: ");
    Serial.print(server.argName(i));
    Serial.print(" value: ");
    Serial.println(server.arg(i));
  } 
  
  Serial.print("headers:");
  Serial.println(server.headers());

  for(int i = 0; i < server.headers(); i++) {
    Serial.print("Header: ");
    Serial.print(server.headerName(i));
    Serial.print(" : ");
    Serial.println(server.header(i));
  }
  server.send(200,"text/plain","OK");
}

void handlePostFunction() {
  if (server.hasArg("plain")== true && server.method() == HTTP_POST){ //Check if body received
    String body = server.arg("plain");
    int capacity = JSON_OBJECT_SIZE(2) + JSON_ARRAY_SIZE(10) + 10*JSON_OBJECT_SIZE(2);
    DynamicJsonBuffer jb(capacity);
    JsonObject& root = jb.parseObject(body);

    if(root.success()) {
      Serial.println("JSON serialization suceeded");
      String devId = root["deviceID"];
      String functName = root["function"];
      if( devId == "" || functName == "") {
        Serial.println("No deviceID or function");
        server.send(400,"text/plain","No deviceID or function");
        return;
      }
      Serial.print("deviceID: ");
      Serial.println(devId);
      Serial.print("function desired: ");
      Serial.println(functName);
      String pars = root["parameters"];

      if(pars == "") {
        Serial.println("No parameters");
        server.send(400,"text/plain","No parameters");
      }

      JsonArray& arr = jb.parseArray(pars);
      for(int i = 0; i < arr.size(); i++) {
        String pname = arr[i]["paramName"];
        String pvalue = arr[i]["paramValue"];
        if(pname == "" || pvalue == "") {
          Serial.println("Wrong paramName or paramValue");
          server.send(400,"text/plain","Wrong paramName or paramValue");
        }
        Serial.print(pname); Serial.print(" "); Serial.println(pvalue);
      }


      server.send(200,"text/plain","OK");
    } else {
      Serial.println("JSON serialization failed");
      server.send(400,"text/plain","Wrong JSON format");
    }

    
  } else {
    Serial.println("Wrong method or no body");
    server.send(400,"text/plain","Wrong method or no body");
  }
}


void handleRoot() {
  server.send(200, "text/plain", "hello from esp8266!");
}

void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}

void setup(void) {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);
  server.on("/post",handlePostFunction);

  server.on("/inline", []() {
    server.send(200, "text/plain", "this works as well");
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}
