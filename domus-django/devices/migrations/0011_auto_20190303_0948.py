# Generated by Django 2.1.6 on 2019-03-03 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0010_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='alert',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
