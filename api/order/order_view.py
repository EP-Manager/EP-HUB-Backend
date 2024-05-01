from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from api.models import Order 
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles, get_excel_data, generate_excel_template
from .order_serializer import  OrderListSerializer, OrderCreateSerializer, OrderUpdateSerializer

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
    
    @allowed_roles([RoleList.ADMIN.value])
    def patch(self, request, order_id):
        user_id = get_user_id(request)
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return CustomResponse(message="Order does not exist").failure_reponse()
        serializer = OrderUpdateSerializer(order, data=request.data, context={'request': request, 'user_id': user_id})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="successfully updated Order", data=serializer.data).success_response()
        return CustomResponse(message="failed to update Order", data=serializer.errors).failure_reponse()
    
    @allowed_roles([RoleList.ADMIN.value])
    def delete(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return CustomResponse(message="Order does not exist").failure_reponse()
        order.delete()
        return CustomResponse(message="successfully deleted Order").success_response()