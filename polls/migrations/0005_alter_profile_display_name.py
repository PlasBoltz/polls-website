# Generated by Django 3.2.9 on 2022-08-15 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20220815_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(default='Temp_Username', max_length=24),
        ),
    ]
