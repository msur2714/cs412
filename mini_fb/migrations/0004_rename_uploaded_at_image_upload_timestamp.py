# Generated by Django 5.1.2 on 2024-10-21 16:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mini_fb", "0003_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="image",
            old_name="uploaded_at",
            new_name="upload_timestamp",
        ),
    ]
