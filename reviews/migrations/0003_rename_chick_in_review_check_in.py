# Generated by Django 4.2.4 on 2023-08-21 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_review_room_alter_review_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='chick_in',
            new_name='check_in',
        ),
    ]
