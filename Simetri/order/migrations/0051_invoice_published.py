# Generated by Django 4.2.5 on 2024-07-01 20:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0050_customerupdaterequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="published",
            field=models.BooleanField(default=False),
        ),
    ]
