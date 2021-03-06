#include "domusJson.h"

String createRegistrationJson(String *deviceId,String *deviceName, String *deviceType, 
  String *owner, StateAttribute* stateatts, int stateattsSize, Funct *funs, int funSize) {
  // calculate the JSON capacity
  // mandatory root information + attributes (an attribute has 3 objects inside)
  int capacity = JSON_OBJECT_SIZE(6) + JSON_ARRAY_SIZE(stateattsSize) + stateattsSize*JSON_OBJECT_SIZE(3);

  capacity += JSON_ARRAY_SIZE(funSize) + funSize*JSON_OBJECT_SIZE(2);
  
  for(int i = 0; i < funSize; i++) {
    FunctionParameter *pars = funs[1].getParameters();
    int parsSize = funs[i].getParamSize();
    capacity += JSON_ARRAY_SIZE(parsSize) + parsSize*JSON_OBJECT_SIZE(3);

    for(int j = 0; j < parsSize; j++) {
      int optsSize = pars[j].getOptionsSize();
      capacity += JSON_ARRAY_SIZE(optsSize) + optsSize*JSON_OBJECT_SIZE(2);

    }
  }
  
  
  DynamicJsonBuffer jb(capacity);
  
  JsonObject &root = jb.createObject();

  Serial.print(root.set("deviceID",*deviceId));
  Serial.print(root.set("deviceName",*deviceName));
  Serial.print(root.set("deviceType",*deviceType));
  Serial.print(root.set("owner", *owner));

  JsonArray &atts = root.createNestedArray("stateAttributes");

  Serial.println("");
  Serial.print("Size of stateatts: ");
  Serial.println(stateattsSize);

  for(int i = 0; i < stateattsSize;i++) {
    JsonObject &tmp = atts.createNestedObject();
    Serial.print(tmp.set("attributeName",stateatts[i].getName()));
    Serial.print(tmp.set("attributeDescription",stateatts[i].getDescription()));
    Serial.print(tmp.set("attributeType",data_typeEnumToString(stateatts[i].getType())));
  }

  JsonArray &jsonfuns = root.createNestedArray("functions");
  for(int i = 0; i < funSize;i++) {
    JsonObject &tmpfun = jsonfuns.createNestedObject();
    Serial.print(tmpfun.set("functionName",funs[i].getFunctName()));
    Serial.print(tmpfun.set("functionDescription",funs[i].getFunctDesc()));
    FunctionParameter *pars = funs[i].getParameters();
    int parsSize = funs[i].getParamSize();

    JsonArray &jsonpars = tmpfun.createNestedArray("parameters");
    
    for(int j = 0; j < parsSize; j++) {
      JsonObject &tmpfun = jsonpars.createNestedObject();
      Serial.print(tmpfun.set("parameterName",pars[j].getParName()));
      Serial.print(tmpfun.set("parameterDescription",pars[j].getParDesc()));
      Serial.print(tmpfun.set("parameterType",data_typeEnumToString(pars[j].getParType() ) ) );
      ParameterOption *opts = pars[j].getOptions();
      int optsSize = pars[j].getOptionsSize();

      JsonArray &jsonopts = tmpfun.createNestedArray("options");

      for(int k = 0; k < optsSize; k++) {
        JsonObject &tmpopt = jsonopts.createNestedObject();
        Serial.print(tmpopt.set("option",opts[k].getOption()));
        Serial.print(tmpopt.set("description",opts[k].getOptionDesc()));
      }
    }
  }

  String to_return = ""; 
  root.prettyPrintTo(to_return);
  
  Serial.println("");
  Serial.println(to_return);
  
  return to_return;
  
}

String createRecordToSend(String const &devId, StateAttribute * stateatt, int data_count, String * values) {
  int capacity = JSON_OBJECT_SIZE(1) + JSON_ARRAY_SIZE(data_count) + data_count*JSON_OBJECT_SIZE(2);

  DynamicJsonBuffer jb(capacity);
  
  JsonObject &root = jb.createObject();

  Serial.print(root.set("deviceID",devId));

  JsonArray &atts = root.createNestedArray("stateAttributes");

  for(int i = 0; i < data_count; i++) {
    JsonObject &tmp = atts.createNestedObject();
    Serial.print(tmp.set("attributeName",stateatt[i].getName()));
    Serial.print(tmp.set("value",values[i]));
  }

  String to_return = ""; 
  root.prettyPrintTo(to_return);
  
  Serial.println("");
  Serial.println(to_return);
  
  return to_return;
  
}

String data_typeEnumToString(data_type type) {
  String str = "S";
  switch(type){
    case b: str = "B"; break;
    case s: str = "S"; break;
    case f: str = "F"; break;
    default: str = "S"; break;
  }
  return str;
}
