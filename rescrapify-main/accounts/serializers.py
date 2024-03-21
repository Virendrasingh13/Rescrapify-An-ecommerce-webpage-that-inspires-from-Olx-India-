from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import CustomUser


class UserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','slug','first_name']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user:
        # Add custom claims
            user_obj = CustomUser.objects.filter(email = user.email).first()
            user_serialized = UserSeralizer(user_obj, many=False)
            token['user'] = user_serialized.data

        return token
    
