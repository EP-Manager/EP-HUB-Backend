import uuid
from rest_framework import serializers
from api.models import Shop_Items
from auth_setup.models import User


class ShopItemsDropDownSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Shop_Items
        fields = ['id', 'name']

class ShopItemsListSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = Shop_Items
        fields = '__all__'

class ShopItemsCreateEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop_Items
        fields = ['name']

    def create(self, validated_data):
        user_id = self.context["user_id"]
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        Shop_Items = Shop_Items.objects.create(**validated_data)
        return Shop_Items

    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")
        instance.name = validated_data.get("name", instance.name)
        instance.updated_by_id = user_id
        instance.save()
        return instance
    
    def validate(self, data):
        if Shop_Items.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError("Blood Group already exists")
        return data