# Generated by Django 5.0 on 2024-08-01 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0062_alter_buyinginvoice_billing_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyinginvoice',
            old_name='grand_total',
            new_name='grand_total_tl',
        ),
    ]
