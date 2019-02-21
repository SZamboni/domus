from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Device, DeviceType, StateAttribute, StateAttributeRecord, Function, FunctionParameter

class DeviceRegistrationForm(forms.ModelForm):
    deviceID = forms.CharField(required=True)
    deviceName = forms.CharField()
    deviceDescription = forms.CharField()

    deviceType = forms.CharField(required=True)
    deviceTypeName = forms.CharField()
    deviceTypeDescription = forms.CharField()
    deviceTypeManufacturer = forms.CharField()

    ownerUsername = forms.CharField(required=True)

    #number stateattributes

    #number functions
        #number parameters for that function

class DeviceTypeStateAttributesRegistrationForm(forms.ModelForm):
    deviceType = forms.CharField(required=True)
    attributeName = forms.CharField(required=True)
    attributeType = forms.CharField(required=True)
    attributeDescription = forms.CharField(required=True)

class DeviceTypeFunctionRegistrationForm(forms.ModelForm):
    deviceType = forms.CharField(required=True)
    functionName = forms.CharField(required=True)
    functionDescription = forms.CharField(required=True)

class DeviceTypeFunctionParameterRegistrationForm(forms.ModelForm):
    deviceType = forms.CharField(required=True)
    functionName = forms.CharField(required=True)
    paramName = forms.CharField(required=True)
    paramType = forms.CharField(required=True)

