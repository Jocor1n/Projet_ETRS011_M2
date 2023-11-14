# Generated by Django 4.2.7 on 2023-11-12 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0013_alter_graphique_graphiquetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphique',
            name='GraphiqueType',
            field=models.CharField(choices=[('1', 'Fleche'), ('2', 'Curseur'), ('3', 'Comparaison'), ('4', 'Texte')], default='1', max_length=255),
        ),
        migrations.AlterField(
            model_name='graphique',
            name='axex',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='graphique',
            name='axey',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
