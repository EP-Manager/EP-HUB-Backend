from rest_framework import serializers
from api.models import Centre, UserCentreLink, City
from auth_setup.models import User

class CentreDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Centre
        fields = ['id', 'city']

class CentreListSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name')
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = Centre
        fields = '__all__'

class CentreCreateSerializer(serializers.ModelSerializer):
    city = serializers.CharField(required=True)
    
    class Meta:
        model = Centre
        fields = ['city']

    def create(self, validated_data):
        user_id = self.context["user_id"]

        validated_data["city_id"] = validated_data.pop("city")
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        centre = Centre.objects.create(**validated_data)
        return centre
    
    def validate(self, data):
        if Centre.objects.filter(city=data['city']).exists():
            raise serializers.ValidationError("Centre already exists")
        return data
    
    def validate_city(self, value):
        if not City.objects.filter(id=value).exists():
            raise serializers.ValidationError("City does not exist")
        return value