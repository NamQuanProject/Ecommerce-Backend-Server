# Generated by Django 5.0.3 on 2024-03-12 06:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile',
            field=models.ForeignKey(default=1710223357.652879, on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
        ),
    ]
