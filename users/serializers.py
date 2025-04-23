from rest_framework import serializers
from users.models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'full_name', 'email', 'contact_number',
            'company_name', 'address', 'industry'
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            contact_number=validated_data['contact_number'],
            company_name=validated_data['company_name'],
            address=validated_data['address'],
            industry=validated_data['industry'],
        )
        return user
