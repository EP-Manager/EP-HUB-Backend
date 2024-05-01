from django.urls import path

from .order_view import OrderAPIView

urlpatterns = [
        path('', OrderAPIView.as_view(), name='order_list'), #get
        path('create/', OrderAPIView.as_view(), name='order_create'), #single post

    ]