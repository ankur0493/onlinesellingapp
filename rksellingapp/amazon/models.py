# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

from seller.models import Seller, Address


class AmazonMarketPlace(models.Model):
    marketplace_id = models.CharField(max_length=64)
    name = models.CharField(max_length=254)
    base_url = models.URLField(blank=True, null=True)


class AmazonBuyer(models.Model):
    amazon_email = models.EmailField(max_length=254, blank=True)
    name = models.CharField(_('Buyer Name'), max_length=254)


class ShippingAddress(models.Model):
    buyer = models.ForeignKey(AmazonBuyer)
    address = models.ForeignKey(Address)


class PaymentMethod(models.Model):
    PAYMENT_METHODS = (
        ('Standard', 'Standard'),
        ('COD', 'COD'),
        ('CVS', 'CVS'),
        ('GiftCertificate', 'Gift Certificate'),
        ('CreditCard', 'Credit Card'),
        ('Other', 'Other'))
    payment_method = models.CharField(
        _('Payment Method'), choices=PAYMENT_METHODS, max_length=64)


class AmazonOrder(models.Model):
    ORDER_TYPES = (
        ('StandardOrder', 'Standard Order'),
        ('PreOrder', 'Pre Order'))
    FULFILLMENT_CHANNELS = (
        ('MFN', 'Seller'),
        ('AFN', 'Fulfilled by Amazon'))
    SHIPPING_SERVICE_LEVELS = (
        ('Local', 'Local'),
        ('Zonal', 'Zonal'),
        ('National', 'National'))
    CURRENCIES = (
        ('INR', 'Rupee'),)
    SHIPMENT_STATUSES = (
        ('PendingPickUp', 'Waiting for Pickup'),
        ('LabelCanceled', 'Label Canceled'),
        ('PickedUp', 'Picked Up'),
        ('AtDestinationFC', 'At Destination Fulfilment Center'),
        ('Delivered', 'Delivered'),
        ('RejectedByBuyer', 'Rejected By Buyer'),
        ('Undeliverable', 'Undeliverable'),
        ('ReturnedToSeller', 'Returned To Seller'))
    SHIPMENT_SERVICE_LEVEL_CATEGORIES = (
        ('Standard', 'Standard'),
        ('Expedited', 'Expedited'),
        ('FreeEconomy', 'FreeEconomy'),
        ('NextDay', 'NextDay'),
        ('SameDay', 'SameDay'),
        ('BuyerTaxInfo', 'BuyerTaxInfo'),
        ('SecondDay', 'SecondDay'),
        ('Scheduled', 'Scheduled'))
    seller = models.ForeignKey(Seller, related_name='orders')
    order_type = models.CharField(_("Order Type"), choices=ORDER_TYPES,
                                  default=ORDER_TYPES[0][0], max_length=13)
    purchase_date = models.DateTimeField()
    order_id = models.CharField(_("Order ID"), max_length=19)
    is_replacement_order = models.BooleanField(default=False)
    replaced_order_id = models.CharField(_("Replacement Order ID"),
                                         max_length=19, blank=True)
    last_updated_amazon = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)
    time_created = models.DateTimeField(auto_now_add=True)
    number_items_shipped = models.IntegerField()
    ship_service_level = models.CharField(max_length=254, blank=True)
    status = models.CharField(_('Order Status'), max_length=64)
    fulfillment_channel = models.CharField(
        _('Fulfillment Channel'), choices=FULFILLMENT_CHANNELS,
        default=FULFILLMENT_CHANNELS[0][0], max_length=3)
    sales_channel = models.CharField(_('Sales Channel'), max_length=56)
    is_business_order = models.BooleanField(default=False)
    earliest_ship_date = models.DateTimeField(null=True)
    latest_ship_date = models.DateTimeField(null=True)
    earliest_delivery_date = models.DateTimeField(null=True)
    latest_delivery_date = models.DateTimeField(null=True)
    number_items_unshipped = models.IntegerField()
    payment_methods = models.ManyToManyField(
        PaymentMethod, related_name='payment_method_detail_orders')
    buyer = models.ForeignKey(AmazonBuyer, null=True)
    currency = models.CharField(_('Order Currency'), choices=CURRENCIES,
                                default=CURRENCIES[0][0], max_length=3,
                                blank=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, null=True)
    is_premium_order = models.BooleanField(default=False)
    is_prime = models.BooleanField(default=False)
    marketplace = models.ForeignKey(AmazonMarketPlace)
    shipment_status = models.CharField(
        _('Shipment Status'), choices=SHIPMENT_STATUSES,
        max_length=16, blank=True)
    payment_method = models.ForeignKey(
        PaymentMethod, related_name='payment_detail_orders', null=True)
    shipment_service_level_category = models.CharField(
        _('Shipment Service Level'), choices=SHIPMENT_SERVICE_LEVEL_CATEGORIES,
        default=SHIPMENT_SERVICE_LEVEL_CATEGORIES[0][0], max_length=32)


# class AmazonOrderItem(models.Model):
#     order = models.ForeignKey(AmazonOrder)
#     asin = models.CharField(_('ASIN'), max_length=64)
#     order_item_id = models.CharField(_('Order Item ID'), max_length=64)
#     sku = models.CharField(_('Seller SKU'), max_length=64, blank=True)
#     title = models.CharField(_('Item Title'), max_length=254, blank=True)
