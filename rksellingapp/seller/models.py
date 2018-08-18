# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from django_countries.fields import CountryField


class Address(models.Model):
    ADDRESS_TYPES = (
        ('Commercial', 'Commercial'),
        ('Residential', 'Residential'))
    name = models.CharField(_('Address Name'), max_length=254)
    address_line_1 = models.CharField(_('Address Line 1'), max_length=254,
                             blank=True)
    address_line_2 = models.CharField(_('Address Line 1'), max_length=254,
                             blank=True)
    address_line_3 = models.CharField(_('Address Line 1'), max_length=254,
                             blank=True)
    city = models.CharField(_('City'), max_length=254, blank=True)
    district = models.CharField(_('District'), max_length=254, blank=True)
    state = models.CharField(_('State'), max_length=64, blank=True)
    postal_code = models.CharField(_('Postal Code'), max_length=10, blank=True)
    country = CountryField(_('Country Code'), max_length=2, blank=True)
    phone_number = models.CharField(_('Phone Number'), max_length=15, null=True)
    address_type = models.CharField(_('Address Type'), choices=ADDRESS_TYPES,
                                    default=ADDRESS_TYPES[0][0], blank=True,
                                    max_length=11)


class Seller(models.Model):
    user = models.ForeignKey(User, related_name='sellers')
    communication_email = models.EmailField(
        _('Communication Email Address'), max_length=254)
    address = models.ForeignKey(Address, null=True)


class EComPartner(models.Model):
    name = models.CharField('Name of the Ecommerce Platform', max_length=254)


class SellerEcommerceData(models.Model):
    seller = models.ForeignKey(Seller, related_name='ecommerce_partners')
    ecom_partner = models.ForeignKey(EComPartner, related_name='sellers')
    ecom_seller_id = models.CharField(_('Seller\'s ID on the E-Com Platform'),
                                 max_length=254, blank=True)
    login_email = models.EmailField(_('Seller\'s login email on the E-Com Platform'),
                                    max_length=254, blank=True)
