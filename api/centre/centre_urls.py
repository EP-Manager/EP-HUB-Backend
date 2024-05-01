from django.urls import path

from .centre_view import CentreDropDownAPIView, CentreAPIView, UserCentreView

urlpatterns = [
        path('', CentreDropDownAPIView.as_view(), name='centre_list'), #drop down
        path('all/', CentreAPIView.as_view(), name='centre_detail'), #get
        path('create/', CentreAPIView.as_view(), name='centre_create'), #single post
        path('delete/<str:centre_id>/', CentreAPIView.as_view(), name='centre_delete'), #single delete

        path('user/', UserCentreView.as_view(), name='user_centre_list'), #get
        path('user/create/', UserCentreView.as_view(), name='user_centre_create'), #single post
        path('user/update/<str:user_centre_id>/', UserCentreView.as_view(), name='user_centre_update'), #single patch
        path('user/delete/<str:user_centre_id>/', UserCentreView.as_view(), name='user_centre_delete'), #single delete

    ]