from django.urls import path

from .order_view import OrderAPIView, OrderCountAPIView

urlpatterns = [
        path('', OrderAPIView.as_view(), name='order_list'), #get
        path('create/', OrderAPIView.as_view(), name='order_create'), #single post
        path('update/<str:order_id>/', OrderAPIView.as_view(), name='order_update'), #single patch
        path('delete/<str:order_id>/', OrderAPIView.as_view(), name='order_delete'), #single delete

        path('count/<str:user_id>', OrderCountAPIView.as_view(), name='order_count'), #get

    ]