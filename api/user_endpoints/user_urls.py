from django.urls import path, include
from .user_view import UserAPIView

urlpatterns = [
    path('all/', UserAPIView.as_view(), name='user_list'), #get

]