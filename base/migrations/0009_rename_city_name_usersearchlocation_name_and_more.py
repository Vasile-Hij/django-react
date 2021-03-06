# Generated by Django 4.0.5 on 2022-07-14 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_city_user_searched_locations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersearchlocation',
            old_name='city_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='city',
            name='user_searched_locations',
        ),
        migrations.AddField(
            model_name='city',
            name='tag',
            field=models.ManyToManyField(to='base.usersearchlocation'),
        ),
    ]
