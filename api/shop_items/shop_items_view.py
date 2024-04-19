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

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        shop_items = Shop_Items.objects.all()
        serializer = ShopItemsDropDownSerizlizer(shop_items, many=True)
        return CustomResponse(message="successfully obtained blood groups", data=serializer.data).success_response()
    
class Shop_Items_APIview(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        shop_items = Shop_Items.objects.all()
        serializer = ShopItemsListSerializer(shop_items, many=True)
        return CustomResponse(message="successfully obtained blood groups", data=serializer.data).success_response()
    
    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        user_id = get_user_id(request)
        serializer = ShopItemsCreateEditSerializer(data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created blood group", data=serializer.data).success_response()
        return CustomResponse(message="failed to blood group", data=serializer.errors).failure_reponse()
    
    @allowed_roles([RoleList.ADMIN.value])
    def patch(self, request, shop_items_id):
        user_id = get_user_id(request)
        if not Shop_Items.objects.filter(id=shop_items_id).exists():
            return CustomResponse(message="blood group not found").failure_reponse()
        shop_items = Shop_Items.objects.get(id=shop_items_id)
        serializer = ShopItemsCreateEditSerializer(shop_items, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated blood group", data=serializer.data).success_response()
        return CustomResponse(message="failed to update blood group", data=serializer.errors).failure_reponse()
    
    @allowed_roles([RoleList.ADMIN.value])
    def delete(self, request, shop_items_id):
        if not Shop_Items.objects.filter(id=shop_items_id).exists():
            return CustomResponse(message="blood group not found").failure_reponse()
        shop_items = Shop_Items.objects.get(id=shop_items_id)
        shop_items.delete()
        return CustomResponse(message="successfully deleted blood group").success_response()
    
class Shop_Items_Bulk_Import_APIview(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        try:
            excel_file = request.FILES["shop_items"]
        except:
            return CustomResponse(message="file not found").failure_reponse()
        if not excel_file.name.endswith('.xlsx'):
            return CustomResponse(message="file type not supported").failure_reponse()
        excel_data = get_excel_data(excel_file)
        
        headers = ['name']
        if not excel_data:
            return CustomResponse(message="The file is empty.").failure_reponse()
        for header in headers:
            if header not in excel_data[0]:
                return CustomResponse(message=f"Please provide the {header} in the file.").failure_reponse()
            
        user_id = get_user_id(request)
        serializer = ShopItemsCreateEditSerializer(data=excel_data[1:], context={'request': request, 'user_id': user_id}, many=True)
        with transaction.atomic():
            if serializer.is_valid():
                if len(serializer.data) != len(excel_data[1:]):
                    transaction.set_rollback(True)
                    return CustomResponse(message="something went wrong, please try again", data=serializer.errors).failure_reponse()
                serializer.save()
                return CustomResponse(message="successfully imported blood groups", data=serializer.data).success_response()
        errors_with_indices = []
        for index, error in enumerate(serializer.errors):
            errors_with_indices.append({"row_index": index + 2, "error": error if error else "no error"})  # Adjust index for headers
        return CustomResponse(message="failed to import blood groups", data=errors_with_indices).failure_reponse()

class Shop_Items_Base_Template_APIview(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        sheet_names = ['Sheet1']
        headers = [['name']]
        column_widths = {'A': 20}
        filename = "shop_items_base_template.xlsx"

        response = generate_excel_template(sheet_names, filename, headers, column_widths)
        return response