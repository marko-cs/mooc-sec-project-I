# Generated by Django 4.1.7 on 2023-07-26 11:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("flawsapp", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="urlnotes",
            name="id",
        ),
        migrations.AddField(
            model_name="urlnotes",
            name="uuid",
            field=models.UUIDField(
                auto_created=True,
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
