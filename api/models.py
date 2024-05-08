from django.db import models
from auth_setup.models import User
import uuid

class Role(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role_updated_by')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class UserRoleLink(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_role_link')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_role_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_role_updated_by')

    class Meta:
        ordering = ['role']

    def __str__(self):
        return f"{self.user.get_full_name} - {self.role.name}"

class District(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='district_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='district_updated_by')

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

class City(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='city_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='city_updated_by')

    class Meta:
        ordering = ['district', 'name']

    def __str__(self) -> str:
        return f"{self.name} - {self.district.name}"

class Centre(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='centre_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='centre_updated_by')

    class Meta:
        ordering = ['city']

    def __str__(self) -> str:
        return f"{self.city.name} - {self.city.district.name}"

class UserCentreLink(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_centre_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_centre_updated_by')

    class Meta:
        ordering = ['centre']

    def __str__(self) -> str:
        return f"{self.user.get_full_name} - {self.centre.city.name} - {self.centre.city.district.name}"

class Shop_Items(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True, blank=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_group_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_group_updated_by')

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Shop_Items, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    status = models.CharField(max_length=30, blank=False, default='Pending')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_type = models.CharField(max_length=4, blank=False, default='BUY')
    delivery_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_delivery_person', null=True, blank=True)
    centre = models.ForeignKey(Centre, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_updated_by')

    class Meta:
        ordering = ['status', 'created_at']

    def __str__(self) -> str:
        return f"{self.user.get_full_name} - {self.item.name} - {self.quantity} - {self.total_price} - {self.status}"