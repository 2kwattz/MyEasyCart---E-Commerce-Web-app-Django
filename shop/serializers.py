from rest_framework import serializers
from .models import Contact
# serializers.py
from .models import User


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)

    class Meta:
        model= User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only': True}
        }
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Passwords are not the same")
        return attrs
        # return super().validate(attrs)
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = User
        fields = ['email','password']