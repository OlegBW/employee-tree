from rest_framework import serializers
from .models import Employee, Hierarchy

class EmployeeSerializer(serializers.ModelSerializer):
    manager_id = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'position', 'hiring_date', 'manager_id']

    def get_manager_id(self, obj):
        manager_id = Hierarchy.objects.filter(subordinate = obj).values_list('id', flat=True).first()
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