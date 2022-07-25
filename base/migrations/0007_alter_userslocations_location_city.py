# Generated by Django 4.0.5 on 2022-07-23 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_userslocations_location_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userslocations',
            name='location_city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_location_city', to='base.location'),
        ),
    ]
