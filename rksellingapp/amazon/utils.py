import base64
import hashlib
import hmac
from tempfile import NamedTemporaryFile
from subprocess import call

from django.conf import settings
from django.forms import model_to_dict
from django.template.loader import render_to_string


def get_amazon_canonicalized_string(method, host, url, query):
    canonicalized_string = "{}\n{}\n{}\n{}".format(method, host, url, query)
    return canonicalized_string


def sign_hmac_sha256(query_req):
    secret_key = settings.AWS_SECRET_KEY
    hmac_obj = hmac.new(secret_key, query_req, hashlib.sha256)
    hmac_digest = hmac_obj.digest()
    return base64.b64encode(hmac_digest)


def get_shipping_label(order):
    shipping_address = model_to_dict(order.shipping_address.address)
    seller_address = model_to_dict(order.seller.address)
    content = render_to_string('shipping_label.html', {
        'shipping_address': shipping_address,
        'seller_address': seller_address})
    print(content)
    f = NamedTemporaryFile(delete=False, suffix=".html")
    f.write(content)
    f.flush()
    output_f_name = '{}.pdf'.format(order.order_id)
    call(['wkhtmltopdf', str(f.name), output_f_name])
    f.close()
    return output_f_name
