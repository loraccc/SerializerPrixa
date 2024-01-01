from django.contrib import admin
from django.urls import path
from . import views
from .views import (ItemListAPIView,ItemDetail,
                    itemList, itemDetail, itemCreate, itemUpdate, itemDelete,
                    UserRegisterView,UserLoginView)


urlpatterns = [
    #Api 
    path('data/', ItemListAPIView.as_view(), name='data'),
    path('data/<int:pk>', ItemDetail.as_view(), name='view_data'),

    #Templates
    path('items/', itemList.as_view(), name='item-list'),
    path('items/create/', itemCreate.as_view(), name='item-create'),
    path('items/<int:pk>/', itemDetail.as_view(), name='item-detail'),
    path('items/<int:pk>/update/', itemUpdate.as_view(), name='item-update'),
    path('items/<int:pk>/delete/', itemDelete.as_view(), name='item-delete'),

    #User Registration & login
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),




]
