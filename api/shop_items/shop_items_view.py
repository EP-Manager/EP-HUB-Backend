from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from tempfile import NamedTemporaryFile
from io import BytesIO
from django.http import FileResponse
from openpyxl import Workbook
from openpyxl.styles import Font

from api.models import Shop_Items
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles, get_excel_data, generate_excel_template
from .shop_items_serializer import ShopItemsDropDownSerizlizer, ShopItemsListSerializer, ShopItemsCreateEditSerializer

class Shop_Items_DropdownAPIview(APIView):
    permission_classes = [IsAuthenticated]

    #@allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        shop_items = Shop_Items.objects.all()
        serializer = ShopItemsDropDownSerizlizer(shop_items, many=True)
        return CustomResponse(message="successfully obtained shop items", data=serializer.data).success_response()
    
class Shop_Items_APIview(APIView):
    permission_classes = [IsAuthenticated]

    #@allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        shop_items = Shop_Items.objects.all()
        serializer = ShopItemsListSerializer(shop_items, many=True)
        return CustomResponse(message="successfully obtained shop items", data=serializer.data).success_response()
    
    #@allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        user_id = get_user_id(request)
        serializer = ShopItemsCreateEditSerializer(data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created shop items", data=serializer.data).success_response()
        return CustomResponse(message="failed to shop items", data=serializer.errors).failure_reponse()
    
    #@allowed_roles([RoleList.ADMIN.value])
    def patch(self, request, shop_items_id):
        user_id = get_user_id(request)
        if not Shop_Items.objects.filter(id=shop_items_id).exists():
            return CustomResponse(message="shop items not found").failure_reponse()
        shop_items = Shop_Items.objects.get(id=shop_items_id)
        serializer = ShopItemsCreateEditSerializer(shop_items, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated shop items", data=serializer.data).success_response()
        return CustomResponse(message="failed to update shop items", data=serializer.errors).failure_reponse()
    
    #@allowed_roles([RoleList.ADMIN.value])
    def delete(self, request, shop_items_id):
        if not Shop_Items.objects.filter(id=shop_items_id).exists():
            return CustomResponse(message="shop items not found").failure_reponse()
        shop_items = Shop_Items.objects.get(id=shop_items_id)
        shop_items.delete()
        return CustomResponse(message="successfully deleted shop items").success_response()