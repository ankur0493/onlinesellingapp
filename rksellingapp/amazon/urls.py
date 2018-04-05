from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('amazon.api.v1.urls')),
]
