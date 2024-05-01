from django.urls import path

from .centre_view import CentreDropDownAPIView, CentreAPIView

urlpatterns = [
        path('', CentreDropDownAPIView.as_view(), name='centre_list'), #drop down
        path('all/', CentreAPIView.as_view(), name='centre_detail'), #get
        path('create/', CentreAPIView.as_view(), name='centre_create'), #single post
        path('delete/<str:centre_id>/', CentreAPIView.as_view(), name='centre_delete'), #single delete

    ]