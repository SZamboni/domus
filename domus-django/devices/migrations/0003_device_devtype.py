# Generated by Django 2.1.6 on 2019-02-14 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20190214_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='Devtype',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='devices.DeviceType'),
        ),
    ]
