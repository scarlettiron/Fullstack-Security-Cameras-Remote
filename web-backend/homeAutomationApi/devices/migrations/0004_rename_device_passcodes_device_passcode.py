# Generated by Django 3.2.13 on 2022-07-17 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_auto_20220715_2017'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='device_passcodes',
            new_name='device_passcode',
        ),
    ]
