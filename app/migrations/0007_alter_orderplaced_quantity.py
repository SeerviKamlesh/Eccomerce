# Generated by Django 5.1.6 on 2025-04-13 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_payment_paid_orderplaced'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
