# Generated by Django 2.1.15 on 2020-08-31 15:18

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200829_2005'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userprofile',
            managers=[
                ('Praha', django.db.models.manager.Manager()),
            ],
        ),
    ]
