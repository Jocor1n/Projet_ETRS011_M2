# Generated by Django 4.2.6 on 2023-10-20 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='Community',
            field=models.CharField(default=None, max_length=255),
        ),
    ]