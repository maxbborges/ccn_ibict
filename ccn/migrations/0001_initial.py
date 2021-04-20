# Generated by Django 3.2 on 2021-04-18 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('cod', models.TextField(db_column='cod', primary_key=True, serialize=False)),
                ('des', models.TextField(db_column='des')),
            ],
            options={
                'db_table': 'pais',
            },
        ),
        migrations.CreateModel(
            name='Postagens',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('frequencia', models.CharField(max_length=100)),
                ('titulo_proprio', models.CharField(max_length=100)),
                ('titulo_abreviado', models.CharField(max_length=100)),
                ('codigo_ccn', models.CharField(max_length=100)),
                ('codigo_issn', models.CharField(max_length=100)),
                ('situacao', models.CharField(max_length=100)),
                ('titulo_completo', models.CharField(max_length=100)),
                ('designacao', models.CharField(max_length=100)),
                ('nome', models.CharField(max_length=100)),
                ('des', models.CharField(max_length=100)),
                ('uf', models.CharField(max_length=100)),
            ],
        ),
    ]
