# Generated by Django 4.2.6 on 2023-11-10 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0009_logs_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='type_log',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Graphique',
        ),
    ]
