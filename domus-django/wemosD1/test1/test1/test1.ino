#include <WiFiUdp.h>
#include <WiFiClientSecureBearSSL.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266WiFiType.h>
#include <CertStoreBearSSL.h>
#include <WiFiServerSecureAxTLS.h>
#include <WiFiServer.h>
#include <ESP8266WiFiScan.h>
#include <ESP8266WiFiSTA.h>
#include <WiFiClientSecure.h>
#include <ESP8266WiFiAP.h>
#include <BearSSLHelpers.h>
#include <ESP8266WiFi.h>
#include <WiFiServerSecureBearSSL.h>
#include <WiFiServerSecure.h>
#include <WiFiClient.h>
#include <WiFiClientSecureAxTLS.h>
#include <ESP8266WiFiGeneric.h>

int i;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  i = 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Hello World!");
  Serial.println(i);
  i++;
  delay(1000);
}
