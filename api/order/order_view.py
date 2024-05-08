from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from api.models import Order 
from auth_setup.models import User
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles, get_excel_data, generate_excel_template
from .order_serializer import  OrderListSerializer, OrderCreateSerializer, OrderUpdateSerializer, OrderCountSerializer
from auth_setup.utils import send_normal_email

class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    #@allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderListSerializer(orders, many=True)
        return CustomResponse(message="successfully obtained Orders", data=serializer.data).success_response()
    
    #@allowed_roles([RoleList.ADMIN.value])
    def post(self, request):
        user_id = get_user_id(request)
        serializer = OrderCreateSerializer(data=request.data, context={'request': request, 'user_id': user_id})

        if serializer.is_valid():
            serializer.save()
            send_normal_email(
                {
                    "email_subject": "New Order Created",
                    "email_body": f"Dear admin, user {serializer.data.get('user')} has created a new order. Update the status and assign a person for delivery",
                    "to_email": [user.email for user in User.objects.filter(is_superuser=1)]
                }
            )
            return CustomResponse(message="successfully created Order", data=serializer.data).success_response()
        return CustomResponse(message="failed to create Order", data=serializer.errors).failure_reponse()
    
    #@allowed_roles([RoleList.ADMIN.value])
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
    
    #@allowed_roles([RoleList.ADMIN.value])
    def delete(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return CustomResponse(message="Order does not exist").failure_reponse()
        order.delete()
        return CustomResponse(message="successfully deleted Order").success_response()
    
class OrderCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        orders = Order.objects.filter(user=user_id).select_related('user')
        buy_count = orders.filter(order_type='BUY').count()
        sell_count = orders.filter(order_type='SELL').count()
        data = OrderCountSerializer({
            "user": orders[0].user,
            "buy_count": buy_count,
            "sell_count": sell_count
        }).data
        return CustomResponse(message="successfully obtained Order count", data=data).success_response()    