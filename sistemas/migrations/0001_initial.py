# Generated by Django 5.2.4 on 2025-07-04 07:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tema",
            fields=[
                (
                    "id_tema",
                    models.CharField(max_length=3, primary_key=True, serialize=False),
                ),
                ("nombre_tema", models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name="Sistema",
            fields=[
                ("id_sistema", models.BigAutoField(primary_key=True, serialize=False)),
                ("dir3_id", models.CharField(max_length=9)),
                ("codigo", models.CharField(max_length=32, unique=True)),
                ("nombre", models.CharField(max_length=220)),
                ("descripcion", models.CharField(max_length=512)),
                ("explicacion", models.TextField(blank=True, default="")),
                (
                    "tema",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sistemas",
                        to="sistemas.tema",
                    ),
                ),
            ],
        ),
    ]
