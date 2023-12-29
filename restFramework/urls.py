from django.contrib import admin
from django.urls import path
from . import views
from .views import ItemListAPIView,ItemDetail

urlpatterns = [
    path('data/', ItemListAPIView.as_view(), name='get_data'),
    path('data/<int:pk>', ItemDetail.as_view(), name='view_data'),
]
