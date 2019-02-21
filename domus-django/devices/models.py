from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class DeviceType(models.Model):
    deviceType = models.CharField(max_length=50, unique = True)
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=80)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Device(models.Model):
    deviceID = models.CharField(max_length=50, unique = True)
    Devtype = models.ForeignKey(DeviceType,on_delete=models.CASCADE, default=DeviceType.objects.all().first())
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    ip_adress = models.CharField(max_length=15)
    port = models.IntegerField()

    def __str__(self):
        return self.name

class Category(models.Model):
    description = models.CharField(max_length=250)
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    devices = models.ManyToManyField(Device)

    def __str__(self):
        return self.name

INT = 'I'
FLOAT = 'F'
STRING = 'S'
BOOL = 'B'
DATA_CHOICES = (
    (INT, 'Integer'),
    (FLOAT, 'Float'),
    (STRING, 'String'),
    (BOOL, 'Boolean'),
)

class StateAttribute(models.Model):
    name = models.CharField(max_length=30) 
    description = models.CharField(max_length=250)
    devType = models.ForeignKey(DeviceType,on_delete= models.CASCADE)

    data_type = models.CharField(
        max_length=1,
        choices=DATA_CHOICES,
        default=STRING,
    )

    def __str__(self):
        return self.name

class StateAttributeRecord(models.Model):
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    attribute = models.ForeignKey(StateAttribute,on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    date_received = models.DateTimeField(default=timezone.now)

class Function(models.Model):
    name = models.CharField(max_length=30) 
    description = models.CharField(max_length=250)
    devType = models.ForeignKey(DeviceType,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FunctionParameter(models.Model):
    name = models.CharField(max_length=30) 
    description = models.CharField(max_length=250)
    funct = models.ForeignKey(Function,on_delete=models.CASCADE)
    data_type = models.CharField(
        max_length=1,
        choices=DATA_CHOICES,
        default=STRING,
    )

    def __str__(self):
        return self.name