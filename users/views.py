from rest_framework import viewsets, status
from rest_framework.response import Response
from users.serializers import UserRegistrationSerializer
from users.models import CustomUser

class UserRegistrationViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully', 'user_id': user.user_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
