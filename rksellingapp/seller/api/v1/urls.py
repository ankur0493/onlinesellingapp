from __future__ import unicode_literals

from django.conf.urls import url

from .views import LoginAPIView, LogoutAPIView, SignupAPIView

urlpatterns = [
    url(r'^signup$', SignupAPIView.as_view()),
    url(r'^login$', LoginAPIView.as_view()),
    url(r'^logout$', LogoutAPIView.as_view())
]
