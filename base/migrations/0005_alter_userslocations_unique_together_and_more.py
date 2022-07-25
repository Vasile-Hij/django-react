# Generated by Django 4.0.5 on 2022-07-23 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0004_alter_userslocations_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userslocations',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='userslocations',
            name='location_city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location_city', to='base.location'),
        ),
        migrations.AlterUniqueTogether(
            name='userslocations',
            unique_together={('user', 'location_city')},
        ),
        migrations.RemoveField(
            model_name='userslocations',
            name='city',
        ),
    ]
