# Generated by Django 4.2.5 on 2024-02-21 21:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0006_alter_currencyrate_rateeur_alter_customer_taxoffice_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="adresName",
        ),
        migrations.AlterField(
            model_name="currencyrate",
            name="rateEUR",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=34.91, max_digits=10
            ),
        ),
    ]
