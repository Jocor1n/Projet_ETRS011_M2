# Generated by Django 4.2.6 on 2023-11-26 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0021_alter_graphique_type_de_donnees_entree_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='graphique_has_machine',
            name='ordre',
            field=models.IntegerField(default=1),
        ),
    ]
