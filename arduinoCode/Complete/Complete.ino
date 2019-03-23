#include "wifi_utils.h"
#include "domusJson.h"

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ArduinoJson.h>

unsigned long sendTimer;

ESP8266WiFiMulti WiFiMulti;
ESP8266WebServer server(80);

const String devId = "ds2e7";
const String devName = "newdev1";
const String devType = "useless";
const String owner = "admin";
const char * wifi_ssid = "CASA_ASUS";  // "FASTWEB-1-1FAA45"
const char * wifi_pwd = "casamiamia"; // "77861704BB"
const String server_url = "http://192.168.1.106:3000/"; // "http://192.168.1.69:3000/"

ServerCommand last_command;

StateAttribute att1 = StateAttribute("att1","desc1",s);
StateAttribute att2 = StateAttribute("att2","desc2",f);
StateAttribute *atts[2];

ParameterOption opts[3];
FunctionParameter pars1[2];
FunctionParameter pars2[2];
Funct *funs[2];
Funct f1 = Funct("funct1","f1desc",pars1,2);
Funct f2 = Funct("funct2","f2desc",pars2,2);

void handleServerCommand() {
  if (server.hasArg("plain")== true){ //Check if body received
    String body = server.arg("plain");
    int capacity = JSON_OBJECT_SIZE(2) + JSON_ARRAY_SIZE(10) + 10*JSON_OBJECT_SIZE(2);
    DynamicJsonBuffer jb(capacity);
    JsonObject& root = jb.parseObject(body);

    if(root.success()) {
      String devId = root["deviceID"];
      String functName = root["function"];
      if( devId == "" || functName == "") {
        Serial.println("No deviceID or function received");
        server.send(400,"text/plain","No deviceID or function received");
        return;
      }
      String pars = root["parameters"];

      if(pars == "") {
        Serial.println("No parameters received");
        server.send(400,"text/plain","No parameters received");
      }

      JsonArray& arr = jb.parseArray(pars);
      
      String *names =  (String *) calloc(int(arr.size()),sizeof(String));
      String *vals =  (String *) calloc(int(arr.size()),sizeof(String));
      
      for(int i = 0; i < arr.size(); i++) {
        String pname = arr[i]["paramName"];
        String pvalue = arr[i]["paramValue"];
        if(pname == "" || pvalue == "") {
          Serial.println("Wrong paramName or paramValue received");
          server.send(400,"text/plain","Wrong paramName or paramValue received");
        }
        names[i]=pname;
        vals[i]=pvalue;
      }

      last_command.setfunName(functName);
      last_command.setDevId(devId);
      last_command.setParSize(int(arr.size()));
      last_command.setParNames(names);
      last_command.setParValues(vals);
      last_command.markAsNotRead();
      
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

void handleNotFound() {
  server.send(404,"text/plain","Not Found");
}

void setup() {
  Serial.begin(115200);

  int sendTimer = 0;

  last_command = ServerCommand();

  atts[0] = &att1;
  atts[1] = &att2;

  opts[0] = ParameterOption("opt1","descopt1");
  opts[1] = ParameterOption("opt2","descopt2");
  opts[2] = ParameterOption("opt3","descopt3");

  pars1[0] = FunctionParameter("par1","par1desc",s,opts,3);
  pars1[1] = FunctionParameter("par2","par2desc",b,NULL,0);
  pars2[0] = FunctionParameter("par3","par3desc",f,NULL,0);
  pars2[1] = FunctionParameter("par4","par4desc",s,NULL,0);
  
  funs[0] = &f1;
  funs[1] = &f2;
  
  startWiFi(WiFiMulti,wifi_ssid,wifi_pwd );
  

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }
  server.on("/",HTTP_POST,handleServerCommand);
  server.onNotFound(handleNotFound);
  server.begin();
  
  String registration = createRegistrationJson(devId,devName,devType,owner,atts,2,funs,2);

  Serial.print("registration JSON: ");
  Serial.println(registration);
  
  if(!sendJSONToServer(WiFiMulti,server_url,registration,false)){
    Serial.println("Error while sending occurred!");
  }

  delay(3000);
}

void loop() {
  
  if(millis() - sendTimer > 15000) {
    att1.setValue("aa");
    att2.setValue("bb");
    
    String record = createRecordToSend(devId,atts,2);
    Serial.print("record to send: ");
    Serial.println(record);
  
    if(!sendJSONToServer(WiFiMulti,server_url,record,false) ) {
      Serial.println("Error while sending occurred!");
    }

    sendTimer = millis();
  }
  
  server.handleClient();
  MDNS.update();

  if(!(last_command.isAlreadyReaded())) {
    Serial.println("New Command:");
    last_command.markAsRead();
    last_command.printToSerial();
  }

}
