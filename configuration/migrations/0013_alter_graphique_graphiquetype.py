# Generated by Django 4.2.7 on 2023-11-12 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0012_oid_donnee_fixe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphique',
            name='GraphiqueType',
            field=models.CharField(choices=[('1', 'Fleche'), ('2', 'Curseur'), ('3', 'Comparaison')], default='1', max_length=255),
        ),
    ]
