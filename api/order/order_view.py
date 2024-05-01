from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from api.models import Order 
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles, get_excel_data, generate_excel_template
from .order_serializer import  OrderListSerializer, OrderCreateSerializer

class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderListSerializer(orders, many=True)
        return CustomResponse(message="successfully obtained Orders", data=serializer.data).success_response()
    
    @allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        user_id = get_user_id(request)
        serializer = OrderCreateSerializer(data=request.data, context={'request': request, 'user_id': user_id})

        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully created Order", data=serializer.data).success_response()
        return CustomResponse(message="failed to create Order", data=serializer.errors).failure_reponse()
