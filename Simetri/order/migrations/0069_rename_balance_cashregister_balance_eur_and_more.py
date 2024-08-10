# Generated by Django 5.0 on 2024-08-05 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0068_paymentreceipt_supplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cashregister',
            old_name='balance',
            new_name='balance_EUR',
        ),
        migrations.AddField(
            model_name='cashregister',
            name='balance_USD',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='cashregister',
            name='balance_tl',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='paymentreceipt',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='paymentreceipt',
            name='eur_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='paymentreceipt',
            name='usd_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]