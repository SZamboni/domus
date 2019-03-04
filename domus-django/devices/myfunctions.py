from django.shortcuts import render,get_object_or_404,redirect, HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView , DeleteView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404,HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
import requests


def parseRegistrationJson(req): 
    print()
    data = json.loads(req.body)
    #integrity checks
    if 'deviceID' not in data:
        return HttpResponse("No deviceID value",status=400)
    
    if 'deviceName' not in data:
        return HttpResponse("No deviceName value",status=400)

    if 'deviceType' not in data:
        return HttpResponse("No deviceType value",status=400)

    if 'owner' not in data:
        return HttpResponse("No owner value",status=400)

    if 'stateAttributes' in data:

        for att in data['stateAttributes']:
            if 'attributeName' not in att:
                return HttpResponse("No attributeName value",status=400)
            if 'attributeType' not in att:
                return HttpResponse("No attributeType value",status=400)

    if 'functions' in data:

        for fun in data['functions']:
            if 'functionName' not in fun:
                return HttpResponse("No functionName value",status=400)
            
            if 'parameters' in fun:
            
                for par in fun['parameters']:
                    if 'parameterName' not in par:
                        return HttpResponse("No parameterName value",status=400)
                    if 'parameterType' not in par:
                        return HttpResponse("No parameterType value",status=400)

                    if 'options' in par:
                        for opt in par['options']:
                            if 'option' not in opt:
                                return HttpResponse("No option value",status=400)
                    
                    if 'constraints' in par:
                        for con in par['constraints']:
                            if 'type' not in con:
                                return HttpResponse("No constraint value",status=400)
                            if 'value' not in con:
                                return HttpResponse("No constraint value",status=400)

    #check if the owner is not valid
    if User.objects.filter(username = data['owner']).exists() == False:
        return HttpResponse("Unknown User",status=400)

    #check if the device is already inside the database
    if Device.objects.filter(deviceID = data['deviceID']).exists():
        print("device already exists")
        return HttpResponse("OK")

    #check if the devicetype already exists
    if DeviceType.objects.filter(deviceType = data['deviceType']).exists():
        devType = DeviceType.objects.filter(deviceType = data['deviceType']).first()
        print("DeviceType already exists")
        dev = Device(deviceID=data['deviceID'],Devtype=devType,name=data['deviceName'],description='',ip_adress=req.META['REMOTE_ADDR'],port="1",path="/")
        dev.save()
        print("Device: ")
        print(dev)

        user = User.objects.filter(username = data['owner']).first()
        print("User: ")
        print(user)

        #check if the category "New Devices" exists
        if Category.objects.filter(owner = user, name = 'New Devices').exists():
            print("adding to category")
            cat = Category.objects.filter(owner = user, name = 'New Devices').first()
            cat.devices.add(dev)
            cat.save()
            print(cat)
        else:
            print("creating new category")
            cat = Category(description="New devices are shown here",name= "New Devices",owner = user)
            cat.save()
            cat.devices.add(dev)
            cat.save()
            print(cat)
        return HttpResponse("OK")     

    else :
        #create new deviceType
        devicetypename = data['deviceType']
        if 'deviceTypeName' in data:
            devicetypename = data['deviceTypeName']

        devType = DeviceType(deviceType = data['deviceType'],name=devicetypename,manufacturer='',description='')
        devType.save()

        #create the state attributes for the deviceType
        if 'stateAttributes' in data:
            for att in data['stateAttributes']:
                attdesc = ''
                if 'attributeDescription' in att:
                    attdesc = att['attributeDescription']
                dataType = att['attributeType']
                if dataType != 'F' and dataType != 'S' and dataType != 'B':
                    dataType = 'S' 
                
                stateAtt = StateAttribute(name=att['attributeName'],description=attdesc,devType=devType,data_type=dataType)
                stateAtt.save()
        
        #create the functions for the devicetype
        if 'functions' in data:
            for fun in data['functions']:
                fundesc =  ''
                if 'functionDescription' in fun:
                    fundesc = fun['functionDescription']
                
                funct = Function(name = fun['functionName'],description=fundesc,devType=devType)
                funct.save()

                if 'parameters' in fun:
                    for par in fun['parameters']:
                        pardesc = ''
                        if 'parameterDescription' in par: 
                            pardesc = par['parameterDescription']

                        dataType = STRING
                        for par_type in DATA_CHOICES:
                            print((par_type))
                            if str(par['parameterType']) == par_type[0]:
                                dataType = par_type[0]
                        param = FunctionParameter(name=par['parameterName'],description = pardesc,funct = funct,data_type = dataType)
                        param.save()

                        if 'options' in par:
                            for opt in par['options']:
                                optdesc = ''
                                if 'optionDescription' in opt:
                                    optdesc = opt['optionDescription']
                                o = FunctionParameterOption(parameter=param,option=opt['option'],description = optdesc)
                                o.save()
                        if 'constraints' in par:
                            for con in par['constraints']:
                                constraint_type = CONSTRAINT_DIFFERENT
                                for con_type in PARAMETER_CONSTRAINT:
                                    if con_type[0] == str(con['type']):
                                        constraint_type = con_type[0]
                                c = FunctionParameterConstraint(parameter=param,value=con['value'],constraintType = constraint_type)
                                c.save()
                        
        #create the device
        dev = Device(deviceID=data['deviceID'],Devtype=devType,name=data['deviceName'],description='',ip_adress=req.META['REMOTE_ADDR'],port="1",path="/")
        dev.save()
        #get the user
        user = User.objects.filter(username = data['owner']).first()

        #insert the device in the appropriate category
        if Category.objects.filter(owner = user, name = 'New Devices').exists():
            print("adding to category")
            cat = Category.objects.filter(owner = user, name = 'New Devices').first()
            cat.devices.add(dev)
            cat.save()
            print(cat)
        else:
            print("creating new category")
            cat = Category(description="New devices are shown here",name= "New Devices",owner = user)
            cat.save()
            cat.devices.add(dev)
            cat.save()
            print(cat)
        
        return HttpResponse("OK")  

    return HttpResponse("OK")


def parseStateData(req):
    data = json.loads(req.body)
    #integrity checks
    if 'deviceID' not in data:
        return HttpResponse("No devideID value",status=400)

    if 'stateAttributes' in data:
        for att in data['stateAttributes']:
            if 'attributeName' not in att:
                return HttpResponse("No attributeName value",status=400)
            if 'value' not in att:
                return HttpResponse("No value value",status=400)
    else:
        return HttpResponse("No stateAttributes value",status=400)
    
    #check if the device is inside the database
    if Device.objects.filter(deviceID = data['deviceID']).exists():
        dev = Device.objects.filter(deviceID = data['deviceID']).first()
        ipaddr = req.META['REMOTE_ADDR']
        if ipaddr != dev.ip_adress:
            dev.ip_adress = ipaddr
            dev.save()

        stateatts = StateAttribute.objects.filter(devType=dev.Devtype)

        for st in stateatts:
            for att in data['stateAttributes']:
                if(st.name == att['attributeName']):
                    val = att['value']
                    if st.data_type == FLOAT:
                        try:
                            val = str(float(att['value']))
                        except:
                            return HttpResponse("Wrong data format",status=400)
                    elif st.data_type == BOOL:
                        try:
                            val = str(bool(att['value']))
                        except:
                            return HttpResponse("Wrong data format",status=400)

                    record = StateAttributeRecord(device = dev, attribute = st, value = val)
                    record.save()

    else:
        return HttpResponse("Device does not exists",status=400)
    
    return HttpResponse("OK")

def sendFunctionRequest(request,cat,dev,funct,values):
    print("sending to")
    print(dev)
    print("the function")
    print(funct)
    print("With the values:")
    print(values)

    ip_dest = dev.ip_adress
    port_dest = dev.port

    responsedata = {}
    responsedata['device'] = dev.deviceID
    responsedata['function'] = funct.name

    parameters = []

    for key,val in values.items():
        obj = {}
        obj['parameterName'] = key
        obj['parameterValue'] = val
        parameters.append(obj)

    responsedata['parameters'] = parameters
    print("Responsedata:")
    print(responsedata)
    
    json_data = json.dumps(responsedata)

    print("JSONDATA:")
    print(json_data)

    try:
        r = requests.post('http://'+str(dev.ip_adress)+':'+str(dev.port) + str(dev.path), json=responsedata,timeout=5)
        print(r.text)

        if r.status_code == 200:
            return True
        else:
            return False
    except:
        print("Erron in trying to send the command")
        return False