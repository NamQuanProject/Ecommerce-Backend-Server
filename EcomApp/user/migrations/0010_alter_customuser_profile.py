# Generated by Django 5.0.3 on 2024-03-13 08:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_customuser_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile',
            field=models.ForeignKey(default=1710317686.348079, on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
        ),
    ]