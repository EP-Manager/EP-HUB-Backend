from django.urls import path, include

urlpatterns = [
    path('role/', include('api.role.role_urls')),

    path('district/', include('api.district.district_urls')),
    path('city/', include('api.city.city_urls')),

    path('shop_items/', include('api.shop_items.shop_items_urls')),

    path('centre/', include('api.centre.centre_urls')),

    
]