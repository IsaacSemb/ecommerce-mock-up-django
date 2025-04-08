# Generated by Django 5.1.7 on 2025-04-08 13:21

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Cart ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date and time created')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255, verbose_name='category name')),
                ('category_description', models.TextField(null=True, verbose_name='Category Description')),
            ],
            options={
                'ordering': ['category_name'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last Name')),
                ('phone', models.CharField(max_length=20, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Customer Email Address')),
                ('date_of_birth', models.DateField(null=True, verbose_name='Date of Birth')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date and time created')),
                ('membership', models.CharField(choices=[('B', 'Basic'), ('P', 'Premium')], default='B', max_length=1, verbose_name='Membership Tier')),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255, verbose_name='Street Name')),
                ('city', models.CharField(max_length=255, verbose_name='City Name')),
                ('country', models.CharField(max_length=255, verbose_name='Country of Residence')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Postal Code')),
                ('is_default', models.BooleanField(default=False, verbose_name='default address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customer', verbose_name='Owner of address')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Total Amount for Order')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date and time created')),
                ('payment_status', models.CharField(choices=[('P', 'pending'), ('C', 'complete'), ('F', 'failed')], default='P', max_length=1, verbose_name='payment status')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.customer', verbose_name='Ordered by')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255, verbose_name='Product Name')),
                ('product_description', models.TextField(verbose_name='Product Description')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Unit Price')),
                ('inventory', models.IntegerField(verbose_name='inventory')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date and time created')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='date and time updated')),
                ('slug', models.SlugField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_category', to='shop.category', verbose_name='Product Category')),
            ],
            options={
                'ordering': ['product_name'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Unit Price')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='Quantity of Items')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date and time created')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order', verbose_name='Which Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orderitems', to='shop.product', verbose_name='Which product')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='Quantity of all Items')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date and time created')),
                ('cart_item_description', models.TextField(null=True, verbose_name='Cart Item Description')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.cart', verbose_name='which Cart')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='which product')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='shop.product', verbose_name='which order')),
            ],
        ),
    ]
