from django.urls import path
from .shop_items_view import Shop_Items_DropdownAPIview, Shop_Items_APIview

urlpatterns = [
        path('', Shop_Items_DropdownAPIview.as_view(), name='shop_items_list'), #drop down
        path('all/', Shop_Items_APIview.as_view(), name='shop_items_detail'), #get
        path('create/', Shop_Items_APIview.as_view(), name='shop_items_create'), #single post
        path('update/<str:shop_items_id>/', Shop_Items_APIview.as_view(), name='shop_items_update'), #single patch
        path('delete/<str:shop_items_id>/', Shop_Items_APIview.as_view(), name='shop_items_delete'), #single delete

    ]