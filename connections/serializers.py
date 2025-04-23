from rest_framework import serializers
from connections.models import Connection
from users.models import CustomUser

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name', 'email', 'contact_number', 'company_name']

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['id', 'from_user', 'to_user', 'status', 'timestamp']
