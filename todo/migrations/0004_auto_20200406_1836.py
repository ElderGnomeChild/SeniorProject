# Generated by Django 3.0.2 on 2020-04-06 18:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_todo_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='due',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
