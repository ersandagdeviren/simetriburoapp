# Generated by Django 4.2.5 on 2024-06-15 19:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0025_orderitem_discount_rate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="discount_rate",
            field=models.PositiveIntegerField(),
        ),
    ]
