from rest_framework import serializers
from .models import Contact
# serializers.py
# from shop.models import User


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        