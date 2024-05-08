from django.contrib import admin
from .models import Role, UserRoleLink, District, City, Centre, UserCentreLink, Order, Shop_Items


# Register your models here.
admin.site.register(Role)
admin.site.register(UserRoleLink)
admin.site.register(District)
admin.site.register(City)
admin.site.register(Centre)
admin.site.register(UserCentreLink)
admin.site.register(Order)
admin.site.register(Shop_Items)