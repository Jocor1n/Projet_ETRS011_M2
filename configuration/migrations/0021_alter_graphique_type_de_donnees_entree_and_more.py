# Generated by Django 4.2.6 on 2023-11-26 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0020_graphique_type_de_donnees_entree_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphique',
            name='type_de_donnees_entree',
            field=models.CharField(choices=[('Texte', 'Texte'), ('Entier', 'Entier'), ('Boolean', 'Boolean'), ('Heure', 'Heure'), ('Minutes', 'Minutes'), ('Secondes', 'Secondes')], default='Texte', max_length=255),
        ),
        migrations.AlterField(
            model_name='graphique',
            name='type_de_donnees_sortie',
            field=models.CharField(choices=[('Texte', 'Texte'), ('Entier', 'Entier'), ('Boolean', 'Boolean'), ('Heure', 'Heure'), ('Minutes', 'Minutes'), ('Secondes', 'Secondes')], default='Texte', max_length=255),
        ),
        migrations.CreateModel(
            name='Machine_has_OID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuration.oid')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuration.machine')),
            ],
        ),
        migrations.CreateModel(
            name='Graphique_has_Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('graphique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuration.graphique')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuration.machine')),
            ],
        ),
    ]