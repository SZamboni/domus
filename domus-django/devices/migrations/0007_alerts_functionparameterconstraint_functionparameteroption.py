# Generated by Django 2.1.6 on 2019-02-21 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_auto_20190221_1228'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alerts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250)),
                ('alert_condition', models.CharField(choices=[('MAX', 'Maximum'), ('MIN', 'Minimum'), ('DIF', 'Different'), ('EQL', 'Equal')], default='EQL', max_length=3)),
                ('level', models.CharField(choices=[('LOW', 'Lowest'), ('MID', 'Medium'), ('HIG', 'Highest')], default='MID', max_length=3)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.StateAttribute')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.Device')),
            ],
        ),
        migrations.CreateModel(
            name='FunctionParameterConstraint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('constraintType', models.CharField(choices=[('MAX', 'Maximum'), ('MIN', 'Minimum'), ('DIF', 'Different')], default='DIF', max_length=3)),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.FunctionParameter')),
            ],
        ),
        migrations.CreateModel(
            name='FunctionParameterOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250)),
                ('option', models.CharField(max_length=30)),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.FunctionParameter')),
            ],
        ),
    ]