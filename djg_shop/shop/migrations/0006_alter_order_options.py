# Generated by Django 5.1.7 on 2025-04-11 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'can cancel an order')]},
        ),
    ]
