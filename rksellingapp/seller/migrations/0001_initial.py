# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-21 05:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Address Name')),
                ('address_line_1', models.CharField(blank=True, max_length=254, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(blank=True, max_length=254, verbose_name='Address Line 1')),
                ('address_line_3', models.CharField(blank=True, max_length=254, verbose_name='Address Line 1')),
                ('city', models.CharField(blank=True, max_length=254, verbose_name='City')),
                ('district', models.CharField(blank=True, max_length=254, verbose_name='District')),
                ('state', models.CharField(blank=True, max_length=64, verbose_name='State')),
                ('postal_code', models.CharField(blank=True, max_length=10, verbose_name='Postal Code')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='Country Code')),
                ('phone_number', models.CharField(max_length=15, null=True, verbose_name='Phone Number')),
                ('address_type', models.CharField(blank=True, choices=[('Commercial', 'Commercial'), ('Residential', 'Residential')], default='Commercial', max_length=11, verbose_name='Address Type')),
            ],
        ),
        migrations.CreateModel(
            name='EComPartner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Name of the Ecommerce Platform')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('communication_email', models.EmailField(max_length=254, verbose_name='Communication Email Address')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.Address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SellerEcommerceData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ecom_seller_id', models.CharField(blank=True, max_length=254, verbose_name="Seller's ID on the E-Com Platform")),
                ('login_email', models.EmailField(blank=True, max_length=254, verbose_name="Seller's login email on the E-Com Platform")),
                ('ecom_partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellers', to='seller.EComPartner')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ecommerce_partners', to='seller.Seller')),
            ],
        ),
    ]
