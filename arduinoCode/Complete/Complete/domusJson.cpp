#include "domusJson.h"

String createRegistrationJson(const String &deviceId,const String &deviceName,const String &deviceType, 
  const String &owner, StateAttribute* stateatts[], int stateattsSize, Funct *funs[], int funSize) {
  // calculate the JSON capacity
  // mandatory root information + attributes (an attribute has 3 objects inside)
  int capacity = JSON_OBJECT_SIZE(6) + JSON_ARRAY_SIZE(stateattsSize) + stateattsSize*JSON_OBJECT_SIZE(3);

  capacity += JSON_ARRAY_SIZE(funSize) + funSize*JSON_OBJECT_SIZE(2);
  
  for(int i = 0; i < funSize; i++) {
    FunctionParameter *pars = funs[1]->getParameters();
    int parsSize = funs[i]->getParamSize();
    capacity += JSON_ARRAY_SIZE(parsSize) + parsSize*JSON_OBJECT_SIZE(3);

    for(int j = 0; j < parsSize; j++) {
      int optsSize = pars[j].getOptionsSize();
      capacity += JSON_ARRAY_SIZE(optsSize) + optsSize*JSON_OBJECT_SIZE(2);

    }
  }
  
  DynamicJsonBuffer jb(capacity);
  
  JsonObject &root = jb.createObject();

  root.set("deviceID",deviceId);
  root.set("deviceName",deviceName);
  root.set("deviceType",deviceType);
  root.set("owner", owner);

  JsonArray &atts = root.createNestedArray("stateAttributes");

  for(int i = 0; i < stateattsSize;i++) {
    JsonObject &tmp = atts.createNestedObject();
    tmp.set("attributeName",stateatts[i]->getName());
    tmp.set("attributeDescription",stateatts[i]->getDescription());
    tmp.set("attributeType",data_typeEnumToString(stateatts[i]->getType()));
  }

  JsonArray &jsonfuns = root.createNestedArray("functions");
  for(int i = 0; i < funSize;i++) {
    JsonObject &tmpfun = jsonfuns.createNestedObject();
    tmpfun.set("functionName",funs[i]->getFunctName());
    tmpfun.set("functionDescription",funs[i]->getFunctDesc());
    FunctionParameter *pars = funs[i]->getParameters();
    int parsSize = funs[i]->getParamSize();

    JsonArray &jsonpars = tmpfun.createNestedArray("parameters");
    
    for(int j = 0; j < parsSize; j++) {
      JsonObject &tmpfun = jsonpars.createNestedObject();
      tmpfun.set("parameterName",pars[j].getParName());
      tmpfun.set("parameterDescription",pars[j].getParDesc());
      tmpfun.set("parameterType",data_typeEnumToString(pars[j].getParType() ) );
      ParameterOption *opts = pars[j].getOptions();
      int optsSize = pars[j].getOptionsSize();

      JsonArray &jsonopts = tmpfun.createNestedArray("options");

      for(int k = 0; k < optsSize; k++) {
        JsonObject &tmpopt = jsonopts.createNestedObject();
        tmpopt.set("option",opts[k].getOption());
        tmpopt.set("description",opts[k].getOptionDesc());
      }
    }
  }

  String to_return = ""; 
  root.prettyPrintTo(to_return);
  
  //Serial.println(to_return);
  
  return to_return;
  
}

String createRecordToSend(String const &devId, StateAttribute * stateatt[], int data_count) {
  int capacity = JSON_OBJECT_SIZE(1) + JSON_ARRAY_SIZE(data_count) + data_count*JSON_OBJECT_SIZE(2);

  DynamicJsonBuffer jb(capacity);
  
  JsonObject &root = jb.createObject();

  root.set("deviceID",devId);

  JsonArray &atts = root.createNestedArray("stateAttributes");

  for(int i = 0; i < data_count; i++) {
    JsonObject &tmp = atts.createNestedObject();
    tmp.set("attributeName",stateatt[i]->getName());
    tmp.set("value",stateatt[i]->getValue());
  }

  String to_return = ""; 
  root.prettyPrintTo(to_return);
  
  
  //Serial.println(to_return);
  
  return to_return;
  
}

String data_typeEnumToString(const data_type &type) {
  String str = "S";
  switch(type){
    case b: str = "B"; break;
    case s: str = "S"; break;
    case f: str = "F"; break;
    default: str = "S"; break;
  }
  return str;
}
