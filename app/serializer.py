from rest_framework import serializers
from .models import App, User, TaskCompletion

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TaskCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCompletion
        fields = '__all__'


