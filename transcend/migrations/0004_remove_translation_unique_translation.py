# Generated by Django 5.0.7 on 2024-10-20 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transcend', '0003_alter_language_code'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='translation',
            name='unique_translation',
        ),
    ]
