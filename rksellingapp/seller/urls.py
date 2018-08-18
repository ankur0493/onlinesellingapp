from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('seller.api.v1.urls')),
]
