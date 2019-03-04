from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance,unreaded_notifications=0)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=StateAttributeRecord)
def test_signal(sender, instance, **kwargs):
    print('StateAttributeRecord signal' + str(instance))
    att = instance.attribute
    print(att)
    dev = instance.device
    print(dev)
    alerts = Alert.objects.filter(attribute = att, device = dev)
    

    for al in alerts:
        
        user = al.user
        if att.data_type == FLOAT:
            if al.alert_condition == CONDITION_GREATER:
                if float(instance.value) > float(al.value):
                    print("condition greater satisfied: " + str(float(instance.value)) + " > " + str(float(al.value)))
                    n = Notification(alert = al, record = instance, date = timezone.now(), readed = False)
                    n.save()
                    user.userprofile.unreaded_notifications += 1
                    user.userprofile.save()                    
            elif al.alert_condition == CONDITION_SMALLER:
                if float(instance.value) < float(al.value):
                    print("condition smaller satisfied: " + str(float(instance.value)) + " < " + str(float(al.value)))
                    n = Notification(alert = al, record = instance, date = timezone.now(), readed = False)
                    n.save()
                    user.userprofile.unreaded_notifications += 1
                    user.userprofile.save()     
            elif al.alert_condition == CONDITION_EQUAL:
                if float(instance.value) == float(al.value):
                    print("condition equal satisfied: " + str(float(instance.value)) + " = " + str(float(al.value)))
                    n = Notification(alert = al, record = instance, date = timezone.now(), readed = False)
                    n.save()
                    user.userprofile.unreaded_notifications += 1
                    user.userprofile.save()     
            elif al.alert_condition == CONDITION_DIFFERENT:
                if float(instance.value) != float(al.value):
                    print("condition different satisfied: " + str(float(instance.value)) + " != " + str(float(al.value)))
                    n = Notification(alert = al, record = instance, date = timezone.now(), readed = False)
                    n.save()
                    user.userprofile.unreaded_notifications += 1
                    user.userprofile.save()     
        
        elif att.data_type == BOOL:
            if al.alert_condition == CONDITION_EQUAL:
                if bool(instance.value) == bool(al.value):
                    print("condition equal satisfied: " + str(bool(instance.value)) + " = " + str(bool(al.value)))
                    n = Notification(alert = al, record = instance, date = timezone.now(), readed = False)
                    n.save()
                    user.userprofile.unreaded_notifications += 1
                    user.userprofile.save()     
            elif al.alert_condition == CONDITION_DIFFERENT:
                if bool(instance.value) != bool(al.value):
                    print("condition different satisfied: " + str(bool(instance.value)) + " != " + str(bool(al.value)))
                    n = Notification(alert = al, record = instance, date = timezone.now(), readed = False)
                    n.save()
                    user.userprofile.unreaded_notifications += 1
                    user.userprofile.save()     
        
        elif att.data_type == STRING:
            if al.alert_condition == CONDITION_EQUAL:
                if instance.value == al.value:
                    print("condition equal satisfied: " + instance.value + " = " + al.value)
                    n = Notification(alert = al, record = instance, date = timezone.now(), readed = False)
                    n.save()
                    user.userprofile.unreaded_notifications += 1
                    user.userprofile.save()     
            elif al.alert_condition == CONDITION_DIFFERENT:
                if instance.value != al.value:
                    print("condition different satisfied: " + instance.value + " != " +al.value)
                    n = Notification(alert = al, record = instance, date = timezone.now(), readed = False)
                    n.save()
                    user.userprofile.unreaded_notifications += 1
                    user.userprofile.save()     



