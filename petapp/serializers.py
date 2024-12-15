from rest_framework import serializers
from .models import Customer_details

class customerserializer(serializers.ModelSerializer):
    class Meta:
        model=Customer_details
        fields='__all__'
