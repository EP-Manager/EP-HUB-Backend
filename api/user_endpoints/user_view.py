from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.models import User
from api.utils import CustomResponse, get_user_id, RoleList, allowed_roles
from .user_serializer import UserListSerializer

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    #@allowed_roles([RoleList.ADMIN.value])
    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return CustomResponse(message="successfully obtained users", data=serializer.data).success_response()