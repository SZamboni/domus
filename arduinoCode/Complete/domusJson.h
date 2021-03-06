#ifndef __DOMUS_JSON__
#define __DOMUS_JSON__

#include <Arduino.h>
#include <HardwareSerial.h>
#include <ArduinoJson.h>
#include <ESP8266WebServer.h>

enum data_type {
  b,
  s,
  f
};

class StateAttribute {
private:
  String attributeName;
  String attributeDescription;
  data_type attributeType;
  String value;
public:
  StateAttribute() {
    attributeName = "";
    attributeDescription = "";
    attributeType = s;
    value = "";
  }

  StateAttribute(String const &_attName, String const &_attDesc, data_type const &_attType ) {
    attributeName = _attName;
    attributeDescription = _attDesc;
    attributeType = _attType;
    value = "";
  }
  String getName() const {return attributeName; }
  String getDescription() const {return attributeDescription; }
  data_type getType() const { return attributeType; }
  void setValue(const String &s) { value = s; }
  String getValue() { return value; }
};

class ParameterOption {
private:
  String option;
  String description;
public:
  ParameterOption() {
    option = "";
    description = ""; 
  }
  ParameterOption(String const &opt, String const &desc) {
    option = opt;
    description = desc; 
  }
  String getOption() const {
    return option;
  }
  String getOptionDesc() const {
    return description;
  }
};

class FunctionParameter {
private:
  String parameterName;
  String parameterDesc;
  data_type parameterType;
  ParameterOption *options;
  int optionsSize;
public:
  FunctionParameter() {
    parameterName = "";
    parameterDesc = "";
    parameterType = s;
    options = NULL;
    optionsSize = 0;
  }
  FunctionParameter(String const &parName, String const &parDesc, data_type const &parType, ParameterOption* opts, int optsSize) {
    parameterName = parName;
    parameterDesc = parDesc;
    parameterType = parType;
    options = opts;
    optionsSize = optsSize;
  }
  String getParName() const { return parameterName; }
  String getParDesc() const { return parameterDesc; }
  data_type getParType() const { return parameterType; }
  int getOptionsSize() const { return optionsSize; }
  ParameterOption* getOptions() { return options; }
  
};

class Funct {
private:
  String functName;
  String functDesc;
  FunctionParameter *pars;
  int parsSize;
public:
  Funct(){
    functName = "";
    functDesc = "";
    pars = NULL;
    parsSize = 0;  
  }
  Funct(String const &fname,String const & fdesc,FunctionParameter * p, int psize){
    functName = fname;
    functDesc = fdesc;
    pars = p;
    parsSize = psize;  
  }
  String getFunctName() const { return functName; }
  String getFunctDesc() const { return functDesc; }
  int getParamSize() const { return parsSize; }
  FunctionParameter * getParameters() { return pars; }
};

class ServerCommand {
private:
  String funName;
  String devId;
  int parSize;
  String * parNames;
  String * parValues;
  bool readed;
public:
  ServerCommand() {
    funName = "";
    devId = "";
    parSize = 0;
    parNames = NULL;
    parValues = NULL;
    readed = true;
  }
  ServerCommand(const String &_devId, const String &_funName, int _parSize, String * _parNames, String * _parValues) {
    funName = _funName;
    devId = _devId;
    parSize = _parSize;
    parNames = _parNames;
    parValues = _parValues;
    readed = false;
  }
  ~ServerCommand() {
    free(parNames);
    free(parValues);
  }
  int getParNumber() { return parSize; }
  String getFunName() { return funName; }
  bool isAlreadyReaded(){ return readed; }
  void markAsRead() { readed = true; }
  String getParName(int i) {
    if(i < 0 && i > parSize) {
      return "";
    } else {
      return parNames[i];
    }
  }
  String getParValue(int i) {
    if(i < 0 && i > parSize) {
      return "";
    } else {
      return parValues[i];
    }
  }
  void printToSerial() {
    Serial.print("deviceID: ");
    Serial.println(devId);
    Serial.print("functionName: ");
    Serial.println(funName);
    for(int i = 0; i < parSize;i++) {
      Serial.print(parNames[i]);
      Serial.print(" : ");
      Serial.println(parValues[i]);
    }
  }
  void markAsNotRead() { readed = false; };
  void setfunName(String _funName) { funName = _funName; }
  void setDevId(String _devId) { devId = _devId; }
  void setParSize(int _parSize) { parSize = _parSize; }
  void setParNames(String * _parNames) {
    free(parNames);
    parNames = _parNames;
  }
  void setParValues(String * _parValues) {
    free(parValues);
    parValues = _parValues;
  }
  
};

String createRegistrationJson(const String &deviceId,const String &deviceName, const String &deviceType, 
  const String &owner, StateAttribute * stateatts[],int stateattsSize, Funct* funs[], int funSize);

String createRecordToSend(String const &devId, StateAttribute * stateatt[], int data_count);

String data_typeEnumToString(const data_type &type);


#endif
