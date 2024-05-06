from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from api.models import City, District, Centre, UserCentreLink
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles, get_excel_data, generate_excel_template
from .centre_serializer import  CentreListSerializer, CentreDropDownSerializer, CentreCreateSerializer, UserCentreCreateSerializer, UserCentreListSerializer, UserCentreUpdateSerializer

class CentreDropDownAPIView(APIView):
    permission_classes = [IsAuthenticated]

    #@allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        centres = Centre.objects.all()
        serializer = CentreDropDownSerializer(centres, many=True)
        return CustomResponse(message="successfully obtained Centres", data=serializer.data).success_response()

class CentreAPIView(APIView):
    permission_classes = [IsAuthenticated]

    #@allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        centres = Centre.objects.all()
        serializer = CentreListSerializer(centres, many=True)
        return CustomResponse(message="successfully obtained Centres", data=serializer.data).success_response()
    
    #@allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        user_id = get_user_id(request)
        serializer = CentreCreateSerializer(data=request.data, context={'request': request, 'user_id': user_id})

        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created Centre", data=serializer.data).success_response()
        return CustomResponse(message="failed to create Centre", data=serializer.errors).failure_reponse()
    
    #@allowed_roles([RoleList.ADMIN.value])
    def delete(self, request, Centre_id):
        Centre = Centre.objects.filter(id=Centre_id).first()
        if not Centre:
            return CustomResponse(message="Centre does not exist").failure_reponse()
        Centre.delete()
        return CustomResponse(message="successfully deleted Centre").success_response()
    
class UserCentreView(APIView):
    permission_classes = [IsAuthenticated]

    #@allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        user_centres = UserCentreLink.objects.all()
        serializer = UserCentreListSerializer(user_centres, many=True)
        return CustomResponse(message="successfully obtained User Centre", data=serializer.data).success_response()
    
    #@allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        user_id = get_user_id(request)
        serializer = UserCentreCreateSerializer(data=request.data, context={'request': request, 'user_id': user_id})

        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created User Centre", data=serializer.data).success_response()
        return CustomResponse(message="failed to create User Centre", data=serializer.errors).failure_reponse()
    
    #@allowed_roles([RoleList.ADMIN.value])
    def patch(self, request, user_centre_id):
        user_id = get_user_id(request)
        user_centre = UserCentreLink.objects.filter(id=user_centre_id).first()
        if not user_centre:
            return CustomResponse(message="user centre does not exist").failure_reponse()
        serializer = UserCentreUpdateSerializer(user_centre, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated User Centre", data=serializer.data).success_response()
        return CustomResponse(message="failed to update User Centre", data=serializer.errors).failure_reponse()
    
    #@allowed_roles([RoleList.ADMIN.value])
    def delete(self, request, user_centre_id):
        user_centre = UserCentreLink.objects.filter(id=user_centre_id).first()
        if not user_centre:
            return CustomResponse(message="user centre does not exist").failure_reponse()
        user_centre.delete()
        return CustomResponse(message="successfully deleted User Centre").success_response()