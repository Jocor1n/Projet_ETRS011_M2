# Generated by Django 4.2.6 on 2023-11-17 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0018_alter_graphique_graphiquetype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oid',
            name='is_Integer',
        ),
    ]
