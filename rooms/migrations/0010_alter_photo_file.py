# Generated by Django 4.2.4 on 2023-08-22 10:19

from django.db import migrations, models
import rooms.models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0009_alter_photo_room_alter_room_amenities_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to=rooms.models.room_photo_directory_path),
        ),
    ]
