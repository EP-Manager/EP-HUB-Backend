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
    
class UserCentreListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name')
    centre = serializers.CharField(source='centre.city.name')
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = UserCentreLink
        fields = '__all__'

class UserCentreCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)
    centre = serializers.CharField(required=True)
    
    class Meta:
        model = UserCentreLink
        fields = ['user', 'centre']

    def create(self, validated_data):
        user_id = self.context["user_id"]

        validated_data["user_id"] = validated_data.pop("user")
        validated_data["centre_id"] = validated_data.pop("centre")
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        user_centre = UserCentreLink.objects.create(**validated_data)
        return user_centre
    
    def validate(self, data):
        if UserCentreLink.objects.filter(user=data['user'], centre=data['centre']).exists():
            raise serializers.ValidationError("User Centre already exists")
        return data
    
    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value
    
    def validate_centre(self, value):
        if not Centre.objects.filter(id=value).exists():
            raise serializers.ValidationError("Centre does not exist")
        return value
    
class UserCentreUpdateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)
    centre = serializers.CharField(required=True)
    
    class Meta:
        model = UserCentreLink
        fields = ['user', 'centre']

    def update(self, instance, validated_data):
        user_id = self.context["user_id"]
        instance.user_id = validated_data.pop("user")
        instance.centre_id = validated_data.pop("centre")
        instance.updated_by_id = user_id
        instance.save()
        return instance
    
    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value
    
    def validate_centre(self, value):
        if not Centre.objects.filter(id=value).exists():
            raise serializers.ValidationError("Centre does not exist")
        return value