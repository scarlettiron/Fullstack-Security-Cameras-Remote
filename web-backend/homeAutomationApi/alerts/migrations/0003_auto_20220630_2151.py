# Generated by Django 3.2.13 on 2022-07-01 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0002_alert_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='alert/images/'),
        ),
    ]
