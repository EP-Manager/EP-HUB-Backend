from django.urls import path, include

urlpatterns = [
    path('district/', include('api.district.district_urls')),
    
]