# Generated by Django 5.0.3 on 2024-03-13 04:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_customuser_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile',
            field=models.ForeignKey(default=1710305308.897533, on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
        ),
    ]
