# Generated by Django 4.2.4 on 2023-08-20 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtype',
            name='name',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
