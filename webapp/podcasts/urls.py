from django.urls import path

from podcasts.views import PodCreate, PodList, PodScrap, PodcastDetail, PodcastList

urlpatterns = [
    path('pods/', PodList.as_view(), name='pod-list'),
    path('pods/create/', PodCreate.as_view(), name='pod-create'),
    path('pods/edit/<int:pk>/', PodScrap.as_view(), name='pod-scrap'),
    path('', PodcastList.as_view(), name='podcast-list'),
    path('<int:pk>', PodcastDetail.as_view(), name='podcast-detail'),
]
