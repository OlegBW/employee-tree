from rest_framework import serializers
from .models import Employee, Hierarchy
from django.contrib.auth.models import User

class EmployeeSerializer(serializers.ModelSerializer):
    manager_id = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'position', 'hiring_date', 'manager_id']

    def get_manager_id(self, obj):
        manager_id = Hierarchy.objects.filter(subordinate = obj).values_list('manager_id', flat=True).first()
        return manager_id

class EmployeeTreeNodeSerializer(serializers.ModelSerializer):
    subordinate_ids = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'position', 'hiring_date', 'subordinate_ids']

    def get_subordinate_ids(self, obj):
        subordinate_ids = Hierarchy.objects.filter(manager=obj).values_list("subordinate_id", flat=True)
        return list(subordinate_ids)

class EmployeeTreeSerializer(serializers.ModelSerializer):
    subordinate = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'position', 'hiring_date', 'subordinate']
    
    def get_subordinate(self, obj):
        subordinates = Hierarchy.objects.filter(manager=obj)
        subordinates = map(lambda subordinate: subordinate.subordinate, subordinates)
        subordinates = EmployeeTreeNodeSerializer(subordinates, many=True).data
        return list(subordinates)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user