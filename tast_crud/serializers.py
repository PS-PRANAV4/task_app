from rest_framework import serializers
from .models import SheduledTask



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheduledTask
        fields = '__all__'