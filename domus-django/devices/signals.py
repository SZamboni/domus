from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Category)
def test_signal(sender, instance, **kwargs):
    print('TestSignel')

@receiver(post_save, sender=StateAttributeRecord)
def test_signal(sender, instance, **kwargs):
    print('StateAttributeRecord signal' + str(instance))
    att = instance.attribute
    print(att)
    dev = instance.device
    print(dev)
    alerts = Alert.objects.filter(attribute = att, device = dev)

    for al in alerts:

        if att.data_type == FLOAT:
            if al.alert_condition == CONDITION_GREATER:
                if float(instance.value) > float(al.value):
                    print("condition greater satisfied: " + str(float(instance.value)) + " > " + str(float(al.value)))
            elif al.alert_condition == CONDITION_SMALLER:
                if float(instance.value) < float(al.value):
                    print("condition smaller satisfied: " + str(float(instance.value)) + " < " + str(float(al.value)))
            elif al.alert_condition == CONDITION_EQUAL:
                if float(instance.value) == float(al.value):
                    print("condition equal satisfied: " + str(float(instance.value)) + " = " + str(float(al.value)))
            elif al.alert_condition == CONDITION_DIFFERENT:
                if float(instance.value) != float(al.value):
                    print("condition different satisfied: " + str(float(instance.value)) + " != " + str(float(al.value)))
        
        elif att.data_type == BOOL:
            if al.alert_condition == CONDITION_EQUAL:
                if bool(instance.value) == bool(al.value):
                    print("condition equal satisfied: " + str(bool(instance.value)) + " = " + str(bool(al.value)))
            elif al.alert_condition == CONDITION_DIFFERENT:
                if bool(instance.value) != bool(al.value):
                    print("condition different satisfied: " + str(bool(instance.value)) + " != " + str(bool(al.value)))
        
        elif att.data_type == STRING:
            if al.alert_condition == CONDITION_EQUAL:
                if instance.value == al.value:
                    print("condition equal satisfied: " + instance.value + " = " + al.value)
            elif al.alert_condition == CONDITION_DIFFERENT:
                if instance.value != al.value:
                    print("condition different satisfied: " + instance.value + " != " +al.value)



