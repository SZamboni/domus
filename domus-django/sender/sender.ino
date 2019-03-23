#include "wifi_utils.h"
#include "domusJson.h"

ESP8266WiFiMulti WiFiMulti;
const String devId = "ds2e7";
const String devName = "newdev1";
const String devType = "useless";
const String owner = "admin";
const char * wifi_ssid = "FASTWEB-1-1FAA45";
const char * wifi_pwd = "77861704BB";
const String server_url = "http://192.168.1.69:3000/";
StateAttribute att1 = StateAttribute("att1","desc1",s);
StateAttribute att2 = StateAttribute("att2","desc2",f);
StateAttribute *atts[2];


void setup() {
  Serial.begin(115200);

  atts[0] = &att1;
  atts[1] = &att2;
  
  startWiFi(WiFiMulti,wifi_ssid,wifi_pwd );

  String registration = createRegistrationJson(devId,devName,devType,owner,atts,2,NULL,0);
  
  sendJSONToServer(WiFiMulti,server_url,registration);

  delay(3000);
}

void loop() {
  att1.setValue("aa");
  att2.setValue("bb");
  
  String record = createRecordToSend(devId,atts,2);

  sendJSONToServer(WiFiMulti,server_url,record);
  
  delay(5000);

}
