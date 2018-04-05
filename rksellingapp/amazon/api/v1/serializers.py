from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from rest_framework import serializers


class AmazonProfitLossSerializer(serializers.Serializer):
    product_name = serializers.CharField(label=_("Product Name"))
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

