# Generated by Django 2.1.15 on 2020-08-29 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='delivery_addres',
            field=models.BooleanField(default=0),
        ),
    ]