from django.contrib import admin
from django.urls import path
from . import views
from .views import (ItemListAPIView,ItemDetail,
                    itemList, itemDetail, itemCreate, itemUpdate, itemDelete,
                    UserRegisterView,UserLoginView)

app_name = 'restFramework'
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
    
    #ECOM
    path('product/', views.product_list, name='product_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    #User Registration & login
    path('users/register/', UserRegisterView.as_view(), name='register'),
    path('users/login/', UserLoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),

    


]
