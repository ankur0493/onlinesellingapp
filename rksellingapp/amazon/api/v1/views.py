from __future__ import unicode_literals

import math

from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import status

from .serializers import AmazonProfitLossSerializer


class AmazonProfitLossAPI(APIView) :
    serializer_class = AmazonProfitLossSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            purchase_price = serializer.data['purchase_price_with_gst']/1.18
            gst_paid = serializer.data['purchase_price_with_gst'] - purchase_price
            amazon_fee = shipping_cost = gst_to_be_paid = pnl = 0
            if serializer.data['list_price']:
                if serializer.data['region'] == 'Local':
                    customer_shipping_charge = 115
                elif serializer.data['region'] == 'Zonal':
                    customer_shipping_charge = 130
                elif serializer.data['region'] == 'National':
                    customer_shipping_charge = 150
                amazon_selling_price = serializer.data['list_price'] + customer_shipping_charge
                if amazon_selling_price <= 500:
                    closure_fee = 10
                elif 500 < amazon_selling_price <= 1000:
                    closure_fee = 20
                else:
                    closure_fee = 40
                amazon_fee = ((amazon_selling_price * 0.085) + closure_fee) * 1.18
                increments = 500 if serializer.data['weight'] < 5000 else 1000
                if serializer.data['region'] == "Local":
                    if serializer.data['weight'] < 5000:
                        base_rate = add_on_rate =30
                    else:
                        base_rate = 80
                        add_on_rate = 9
                elif serializer.data['region'] == "Zonal":
                    if serializer.data['weight'] < 5000:
                        base_rate = 45
                        add_on_rate = 35
                    else:
                        base_rate = 130
                        add_on_rate = 11
                elif serializer.data['region'] == "National":
                    if serializer.data['weight'] < 5000:
                        base_rate = 65
                        add_on_rate = 45
                    else:
                        base_rate = 180
                        add_on_rate = 13
                shipping_cost = (base_rate + (math.ceil(serializer.data['weight']/increments) - 1) * add_on_rate) * 1.18
                amazon_fee_shipping_gst = (amazon_fee + shipping_cost) - ((amazon_fee + shipping_cost) / 1.18)
                gst_to_be_paid = amazon_selling_price*0.09/0.59 - amazon_fee_shipping_gst - gst_paid
                packing_charge = 20
                pnl = (amazon_selling_price - serializer.data['purchase_price_with_gst']
                       - amazon_fee - shipping_cost - packing_charge - gst_to_be_paid)
            data = serializer.data.copy()
            data.update({
                'amazon_fee': amazon_fee,
                'shipping_cost': shipping_cost,
                'gst_to_be_paid': gst_to_be_paid,
                'pnl': pnl,
            })
            return Response(data=data, status=status.HTTP_200_OK)
