from django.urls import path, include

urlpatterns = [
    path('district/', include('api.district.district_urls')),

    path('role/', include('api.role.role_urls')),
    
]