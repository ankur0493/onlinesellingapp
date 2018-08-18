from django.conf.urls import url

from .views import AmazonProfitLossAPI, AmazonOrderListAPI


urlpatterns = [
     url(r'^profit-loss/$', AmazonProfitLossAPI.as_view()),
     url(r'^orders/$', AmazonOrderListAPI.as_view()),
]
