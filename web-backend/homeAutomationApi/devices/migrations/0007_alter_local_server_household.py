# Generated by Django 3.2.13 on 2022-07-28 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_allowed_person_pic'),
        ('devices', '0006_local_server_unit_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='local_server',
            name='household',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.household'),
        ),
    ]
