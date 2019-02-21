from django.contrib import admin
from .models import Category, Device, DeviceType, StateAttribute, StateAttributeRecord, FunctionParameter, Function, FunctionParameterConstraint, FunctionParameterOption, Alerts

admin.site.register(Category)
admin.site.register(Device)
admin.site.register(DeviceType)
admin.site.register(StateAttribute)
admin.site.register(StateAttributeRecord)
admin.site.register(FunctionParameter)
admin.site.register(Function)
admin.site.register(FunctionParameterConstraint)
admin.site.register(FunctionParameterOption)
admin.site.register(Alerts)
