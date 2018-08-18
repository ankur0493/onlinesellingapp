from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from rest_framework import serializers

from amazon.models import (
    Address, AmazonBuyer, AmazonMarketPlace,
    AmazonOrder, PaymentMethod)


class AmazonProfitLossSerializer(serializers.Serializer):
    product_name = serializers.CharField(label=_("Product Name"), required=False)
    purchase_price_with_gst = serializers.IntegerField()
    weight = serializers.IntegerField(label=_("Weight (in grams)"))
    region = serializers.ChoiceField(choices=["Local", "Zonal", "National"])
    list_price = serializers.IntegerField()
    amazon_fee = serializers.FloatField(read_only=True)
    shipping_cost = serializers.FloatField(read_only=True)
    gst_to_be_paid = serializers.FloatField(read_only=True)
    pnl = serializers.FloatField(read_only=True)

    class Meta:
        fields = ()


class AmazonMarketPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmazonMarketPlace
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    address_type = serializers.CharField(source='get_address_type_display')
    country = serializers.CharField(source='country.name')

    class Meta:
        model = Address
        fields = '__all__'


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmazonBuyer
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    payment_method = serializers.CharField(source='get_payment_method_display')

    class Meta:
        model = PaymentMethod
        fields = '__all__'


class AmazonOrderSerializer(serializers.ModelSerializer):
    order_type = serializers.CharField(source='get_order_type_display')
    shipping_address = AddressSerializer()
    buyer = BuyerSerializer()
    payment_methods = PaymentMethodSerializer(many=True)
    payment_method = serializers.SerializerMethodField()
    marketplace = AmazonMarketPlaceSerializer()
    fulfillment_channel = serializers.CharField(source='get_fulfillment_channel_display')
    currency = serializers.CharField(source='get_currency_display')
    shipment_status = serializers.CharField(source='get_shipment_status_display')
    shipment_service_level_category = serializers.CharField(
        source='get_shipment_service_level_category_display')

    def get_payment_method(self, obj):
        if obj.payment_method:
            return obj.payment_method.payment_method
        return ''

    class Meta:
        model = AmazonOrder
        fields = '__all__'