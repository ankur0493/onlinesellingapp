from django.conf.urls import url

from .views import AmazonProfitLossAPI


urlpatterns = [
     url(r'^profit-loss/$', AmazonProfitLossAPI.as_view()),
]
