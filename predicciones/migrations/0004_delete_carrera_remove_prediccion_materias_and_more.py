# Generated by Django 5.1 on 2024-09-28 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predicciones', '0003_carrera_materia_prediccion_notas_materias_nota_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Carrera',
        ),
        migrations.RemoveField(
            model_name='prediccion',
            name='materias',
        ),
        migrations.RemoveField(
            model_name='nota',
            name='materia',
        ),
        migrations.RemoveField(
            model_name='nota',
            name='prediccion',
        ),
        migrations.RemoveField(
            model_name='prediccion',
            name='notas_materias',
        ),
        migrations.DeleteModel(
            name='Materia',
        ),
        migrations.DeleteModel(
            name='Nota',
        ),
    ]
