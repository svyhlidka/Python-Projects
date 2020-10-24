# Generated by Django 2.1.15 on 2020-09-02 15:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_friend_current_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(blank=True, on_delete=None, related_name='updator', to=settings.AUTH_USER_MODEL),
        ),
    ]
