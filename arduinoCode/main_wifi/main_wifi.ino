/**
 * Program to test the Wifi capabilities of the Wemos
 */
// Library Include
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

// Custom file Include
#include "wifi_utils.h"
#include "domusJson.h"

// Global Variables
ESP8266WiFiMulti WiFiMulti;
String devId = "7";
StateAttribute stateatts[2];

/**
 * Setup function only run once at the start
 */
void setup() {
  Serial.begin(115200);
  
  startWiFi(&WiFiMulti);

  stateatts[0] = StateAttribute("att1","desc1",s);
  stateatts[1] = StateAttribute("att2","desc2",f);
  
  String devName = "Wemos2132";
  String devType = "WemosR1D2";
  String owner = "admin";

  ParameterOption opts1[2];
  opts1[0] = ParameterOption("a","desc opt a");
  opts1[1] = ParameterOption("b","desc opt b");

  FunctionParameter pars[2];
  pars[0] = FunctionParameter("par1","descpar1",s,opts1,2);
  pars[1] = FunctionParameter("par2","descpar2",f,NULL,0);

  Funct funs[2]; 
  funs[0] = Funct("f1name","f1desc",pars,2);
  funs[1] = Funct("f2name","f2desc",pars,2);

  String registration = createRegistrationJson(&devId,&devName,&devType,&owner,stateatts,2,funs,2);
  
  sendJSONToServer(&WiFiMulti,&registration);

  delay(3000);
}

void loop() {

  String values[2];
  values[0] = "val1";
  values[1] = "val2";
  String record = createRecordToSend(devId,stateatts,2,values);
  
  sendJSONToServer(&WiFiMulti,&record);
  
  delay(5000);
}
