# Generated by Django 2.1.15 on 2020-08-29 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200829_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
