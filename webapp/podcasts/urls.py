from django.urls import path

from podcasts.views import PodCreate

urlpatterns = [
    path('', PodCreate.as_view(), name='pod-create'),
]
