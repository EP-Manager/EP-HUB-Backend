from rest_framework import serializers
from api.models import Centre, UserCentreLink, City
from auth_setup.models import User

class CentreDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Centre
        fields = ['id', 'name']

class CentreListSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
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
        fields = ['name']

    def create(self, validated_data):
        user_id = self.context["user_id"]

        validated_data["city_id"] = validated_data.pop("city")
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        centre = Centre.objects.create(**validated_data)
        return centre
    
    def validate(self, data):
        if Centre.objects.filter(name=data['name'], city=data['city']).exists():
            raise serializers.ValidationError("Centre already exists")
        return data
    
    def validate_city(self, value):
        if not City.objects.filter(id=value).exists():
            raise serializers.ValidationError("City does not exist")
        return value
    
class CentreUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    
    class Meta:
        model = Centre
        fields = ['name', 'city']
    
    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")
        new_name = validated_data.get("name", instance.name)
        new_city = validated_data.get("city", instance.city_id)
        if Centre.objects.filter(name=new_name, city=new_city).exists():
            raise serializers.ValidationError("Centre already exists")
        instance.name = new_name
        instance.city_id = new_city
        instance.updated_by_id = user_id
        instance.save()
        return instance
    
    def validate_city(self, value):
        if not City.objects.filter(id=value).exists():
            raise serializers.ValidationError("City does not exist")
        return value