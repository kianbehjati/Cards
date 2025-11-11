from rest_framework import serializers
from .models import myUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = myUser
        fields = ['username','email','phone_number']


