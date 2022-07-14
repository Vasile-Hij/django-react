# Generated by Django 4.0.5 on 2022-07-14 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_city_user_searched_locations_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSearchLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=85)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='users_location',
            field=models.ManyToManyField(to='base.usersearchlocation'),
        ),
    ]
