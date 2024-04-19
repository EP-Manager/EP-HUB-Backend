import uuid
from rest_framework import serializers
from api.models import Plastic_Types
from auth_setup.models import User


class ShopItemsDropDownSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Plastic_Types
        fields = ['id', 'name']

class ShopItemsListSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = Plastic_Types
        fields = '__all__'

class ShopItemsCreateEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plastic_Types
        fields = ['name']

    def create(self, validated_data):
        user_id = self.context["user_id"]
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        Plastic_Types = Plastic_Types.objects.create(**validated_data)
        return Plastic_Types

    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")
        instance.name = validated_data.get("name", instance.name)
        instance.updated_by_id = user_id
        instance.save()
        return instance
    
    def validate(self, data):
        if Plastic_Types.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError("Blood Group already exists")
        return data