# Generated by Django 4.0.6 on 2022-08-02 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_location_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecastnow',
            name='city',
            field=models.CharField(max_length=85),
        ),
    ]
