# Generated by Django 5.0.7 on 2024-10-01 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transcend", "0002_rename_languages_language_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="translation",
            name="language",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="transcend.language"
            ),
        ),
    ]
