# Generated by Django 4.2.5 on 2024-06-13 08:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0019_orderitem_tax_rate"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderitem",
            old_name="TAX_rate",
            new_name="Tax_rate",
        ),
    ]
