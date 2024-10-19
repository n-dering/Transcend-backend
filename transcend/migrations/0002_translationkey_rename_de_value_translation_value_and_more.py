# Generated by Django 5.0.7 on 2024-10-19 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslationKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='translation',
            old_name='de_value',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='key',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='pl_value',
        ),
        migrations.AlterField(
            model_name='translation',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='transcend.language'),
        ),
        migrations.AddField(
            model_name='translation',
            name='translation_key',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='transcend.translationkey'),
            preserve_default=False,
        ),
    ]