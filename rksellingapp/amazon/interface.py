import requests
import urllib
import xmltodict
import xml.etree.ElementTree as ET
from datetime import timedelta
import dateutil.parser
from StringIO import StringIO

from django.db import transaction
from django.conf import settings
from django.utils import timezone

from amazon.constants import (
    MWS_IN_MARKETPLACE_BASE_URL,
    MWS_IN_MARKETPLACE_ID,
    MWS_ORDERS_API_ENDPOINT,
    MWS_SIGNATURE_METHOD,
    MWS_SIGNATURE_VERSION,
    MWS_REQUEST_METHOD,
    RK_SELLER_ID,
)
from amazon.models import (
    ShippingAddress, AmazonOrder, AmazonBuyer, AmazonMarketPlace, PaymentMethod)
from amazon.utils import (
    get_amazon_canonicalized_string,
    sign_hmac_sha256
)
from seller.models import Address, EComPartner, SellerEcommerceData


def get_bool(string):
    return True if string.lower() in ['true', 'y', 'yes', 't'] else False


def save_order_information(order, seller):
    with transaction.atomic():
        try:
            purchase_date = dateutil.parser.parse(order.get('PurchaseDate'))
        except TypeError:
            purchase_date = None
        last_updated_amazon = dateutil.parser.parse(order['LastUpdateDate'])
        try:
            earliest_ship_date = dateutil.parser.parse(order.get('EarliestShipDate'))
        except TypeError:
            earliest_ship_date = None
        try:
            latest_ship_date = dateutil.parser.parse(order.get('LatestShipDate'))
        except TypeError:
            latest_ship_date = None
        try:
            earliest_delivery_date = dateutil.parser.parse(order.get('EarliestDeliveryDate'))
        except TypeError:
            earliest_delivery_date = None
        try:
            latest_delivery_date = dateutil.parser.parse(order.get('LatestDeliveryDate'))
        except TypeError:
            latest_delivery_date = None
        order_id = order['AmazonOrderId']
        buyer_defaults = {
            'amazon_email': order.get('BuyerEmail', ''),
            'name': order.get('BuyerName')
        }
        if buyer_defaults['amazon_email'] or buyer_defaults['name']:
            buyer, created = AmazonBuyer.objects.update_or_create(**buyer_defaults)
        else:
            buyer = None
        marketplace = AmazonMarketPlace.objects.get(
            marketplace_id=order['MarketplaceId'])
        payment_method = order.get('PaymentMethod')
        if payment_method:
            payment_method_obj = PaymentMethod.objects.get(
                payment_method=payment_method)
        else:
            payment_method_obj = None
        address_data = order.get('ShippingAddress')
        shipping_address = None
        if address_data:
            address_defaults = {
                'address_line_1': address_data.get('AddressLine1', ''),
                'address_line_2': address_data.get('AddressLine2', ''),
                'address_line_3': address_data.get('AddressLine3', ''),
                'city': address_data.get('City', ''),
                'state': address_data.get('StateOrRegion', ''),
                'postal_code': address_data.get('PostalCode', ''),
                'country': address_data.get('CountryCode', ''),
                'address_type': address_data.get('AddressType', 'Residential'),
                'phone_number': address_data.get('Phone')
            }
            address, created = Address.objects.update_or_create(
                name=address_data['Name'], defaults=address_defaults
                )
            shipping_address, created = ShippingAddress.objects.update_or_create(
                buyer=buyer, address=address)
        defaults = {
            'buyer': buyer,
            'seller': seller,
            'latest_ship_date': latest_ship_date,
            'order_type': order['OrderType'],
            'purchase_date': purchase_date,
            'is_replacement_order': get_bool(order['IsReplacementOrder']),
            'last_updated_amazon': last_updated_amazon,
            'number_items_shipped': order.get('NumberOfItemsShipped', 0),
            'ship_service_level': order['ShipServiceLevel'],
            'status': order['OrderStatus'],
            'sales_channel': order['SalesChannel'],
            'is_business_order': get_bool(order['IsBusinessOrder']),
            'earliest_ship_date': earliest_ship_date,
            'earliest_delivery_date': earliest_delivery_date,
            'latest_delivery_date': latest_delivery_date,
            'number_items_unshipped': order.get('NumberOfItemsUnshipped', 0),
            'currency': order.get('OrderTotal', {}).get('CurrencyCode', ''),
            'amount': order.get('OrderTotal', {}).get('Amount'),
            'is_premium_order': get_bool(order['IsPremiumOrder']),
            'marketplace': marketplace,
            'fulfillment_channel': order['FulfillmentChannel'],
            'shipment_status': order.get('TFMShipmentStatus', ''),
            'payment_method': payment_method_obj,
            'shipping_address': shipping_address,
            'is_prime': get_bool(order['IsPrime']),
            'shipment_service_level_category': order['ShipmentServiceLevelCategory']
        }
        print(defaults)
        order_obj, created = AmazonOrder.objects.update_or_create(
            order_id=order_id, defaults=defaults)
        if order.get('PaymentMethodDetails', []):
            if isinstance(order['PaymentMethodDetails'], list):
                for pymt_mthd in order['PaymentMethodDetails']:
                    method = (
                        'COD' if pymt_mthd['PaymentMethodDetail'] == 'CashOnDelivery'
                        else pymt_mthd['PaymentMethodDetail'])
                    payment_method = PaymentMethod.objects.get(
                        payment_method=method)
                    order_obj.payment_methods.add(payment_method)
            else:
                method = order['PaymentMethodDetails']['PaymentMethodDetail']
                method = 'COD' if method == 'CashOnDelivery' else method
                payment_method = PaymentMethod.objects.get(
                    payment_method=method)
                order_obj.payment_methods.add(payment_method)


def get_orders_list(seller=None, num_days=7):
    if seller is None:
        raise Exception("Please provide the seller")

    try:
        ecom_partner = EComPartner.objects.get(name="Amazon")
        seller_data = SellerEcommerceData.objects.get(
            ecom_partner=ecom_partner, seller=seller)
    except EComPartner.DoesNotExist:
        raise Exception("E-Commerce Partner with name Amazon does not exist")
    except SellerEcommerceData.DoesNotExist:
        raise Exception("Seller's Data for Amazon is not available")

    access_key = settings.AWS_ACCESS_KEY_ID
    action = 'ListOrders'
    orders_api_version = '2013-09-01'
    timestamp = timezone.now().isoformat()

    last_updated_after = timezone.now() - timedelta(days=num_days)
    last_updated_after_timestamp = last_updated_after.isoformat()

    query_params = {
        'AWSAccessKeyId': access_key,
        'Action': action,
        'MarketplaceId.Id.1': MWS_IN_MARKETPLACE_ID,
        'LastUpdatedAfter': last_updated_after_timestamp,
        'SellerId': seller_data.ecom_seller_id,
        'SignatureVersion': MWS_SIGNATURE_VERSION,
        'SignatureMethod': MWS_SIGNATURE_METHOD,
        'Timestamp': timestamp,
        'Version': orders_api_version,
    }

    sorted_query_params = sorted(query_params.items(), key=lambda x: x[0])

    query_string = urllib.urlencode(sorted_query_params)

    canonicalized_query_string = get_amazon_canonicalized_string(
        MWS_REQUEST_METHOD, MWS_IN_MARKETPLACE_BASE_URL.split("//")[1],
        MWS_ORDERS_API_ENDPOINT, query_string)
    signature = sign_hmac_sha256(canonicalized_query_string)
    query_params['Signature'] = signature

    sorted_query_params = sorted(query_params.items(), key=lambda x: x[0])
    query_string = urllib.urlencode(sorted_query_params)
    query_url = '{}{}?{}'.format(
        MWS_IN_MARKETPLACE_BASE_URL, MWS_ORDERS_API_ENDPOINT, query_string)
    response = requests.post(query_url)
    data = xmltodict.parse(response.content)
    print(data)
    print(response.headers)
    orders = data['ListOrdersResponse']['ListOrdersResult']['Orders']['Order']
    for order in orders:
        save_order_information(order, seller)


def get_order(order_id, seller=None):
    if seller is None:
        raise Exception("Please provide the seller")

    try:
        ecom_partner = EComPartner.objects.get(name="Amazon")
        seller_data = SellerEcommerceData.objects.get(
            ecom_partner=ecom_partner, seller=seller)
    except EComPartner.DoesNotExist:
        raise Exception("E-Commerce Partner with name Amazon does not exist")
    except SellerEcommerceData.DoesNotExist:
        raise Exception("Seller's Data for Amazon is not available")

    access_key = settings.AWS_ACCESS_KEY_ID
    action = 'GetOrder'
    orders_api_version = '2013-09-01'
    timestamp = timezone.now().isoformat()

    last_updated_after = timezone.now() - timedelta(days=60)
    last_updated_after_timestamp = last_updated_after.isoformat()

    query_params = {
        'AWSAccessKeyId': access_key,
        'Action': action,
        'AmazonOrderId.Id.1': order_id,
        'LastUpdatedAfter': last_updated_after_timestamp,
        'SellerId': seller_data.ecom_seller_id,
        'SignatureVersion': MWS_SIGNATURE_VERSION,
        'SignatureMethod': MWS_SIGNATURE_METHOD,
        'Timestamp': timestamp,
        'Version': orders_api_version
    }

    sorted_query_params = sorted(query_params.items(), key=lambda x: x[0])

    query_string = urllib.urlencode(sorted_query_params)

    canonicalized_query_string = get_amazon_canonicalized_string(
        MWS_REQUEST_METHOD, MWS_IN_MARKETPLACE_BASE_URL.split("//")[1], MWS_ORDERS_API_ENDPOINT, query_string)
    signature = sign_hmac_sha256(canonicalized_query_string)
    query_params['Signature'] = signature

    sorted_query_params = sorted(query_params.items(), key=lambda x: x[0])
    query_string = urllib.urlencode(sorted_query_params)
    query_url = '{}{}?{}'.format(
        MWS_IN_MARKETPLACE_BASE_URL, MWS_ORDERS_API_ENDPOINT, query_string)
    response = requests.post(query_url)
    data = xmltodict.parse(response.content)
    print(data)
    order = data['GetOrderResponse']['GetOrderResult']['Orders']['Order']
    save_order_information(order, seller)
