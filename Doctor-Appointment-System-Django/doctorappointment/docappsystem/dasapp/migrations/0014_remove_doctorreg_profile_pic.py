# Generated by Django 5.0.2 on 2024-02-24 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dasapp', '0013_page_alter_customuser_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorreg',
            name='profile_pic',
        ),
    ]
