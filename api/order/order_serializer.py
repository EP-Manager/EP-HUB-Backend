from rest_framework import serializers

from api.models import Order, Shop_Items, Centre
from auth_setup.models import User

class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name')
    delivery_person = serializers.CharField(source='delivery_person.get_full_name', required=False)
    centre = serializers.CharField(source='centre.city.name')
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = Order
        fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)
    item = serializers.CharField(required=True)
    delivery_person = serializers.CharField(required=False)
    centre = serializers.CharField(required=True)
    
    class Meta:
        model = Order
        fields = ['item', 'quantity', 'total_price', 'status', 'order_type','user', 'delivery_person', 'centre']

    def create(self, validated_data):
        user_id = self.context["user_id"]

        validated_data["user_id"] = validated_data.pop("user")
        validated_data["item_id"] = validated_data.pop("item")
        if "delivery_person" in validated_data:
            validated_data["delivery_person_id"] = validated_data.pop("delivery_person")
        validated_data["centre_id"] = validated_data.pop("centre")
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        order = Order.objects.create(**validated_data)
        return order
    
    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value
    
    def validate_centre(self, value):
        if not Centre.objects.filter(id=value).exists():
            raise serializers.ValidationError("Centre does not exist")
        return value

    def validate_item(self, value):
        if not Shop_Items.objects.filter(id=value).exists():
            raise serializers.ValidationError("Item does not exist")
        return value