# Generated by Django 4.2.4 on 2023-09-08 10:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo",
            name="is_checked",
            field=models.BooleanField(default=False),
        ),
    ]
