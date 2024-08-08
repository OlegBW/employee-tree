from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from .models import Employee, Hierarchy
from .serializers import EmployeeSerializer, EmployeeTreeSerializer, EmployeeTreeNodeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EmployeeFilter 
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EmployeeFilter
    ordering_fields = '__all__'  # Дозволяє сортування за всіма полями
    ordering = ['id']  # Значення за замовчуванням для сортування

class EmployeesTreeView(APIView):
    def get(self, request, *args, **kwargs):
        tier_1_managers = Employee.objects.filter(position='tier_1')

        # subordinates = Hierarchy.objects.filter(manager__in=tier_1_managers).values_list('subordinate', flat=True)

        # employees = Employee.objects.filter(id__in=subordinates)

        serializer = EmployeeTreeSerializer(tier_1_managers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployeeTreeNodeView(APIView):
    def get(self, request):
        ids = request.query_params.get('ids')
        
        if not ids:
            return Response({"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        ids_list = ids.split(',')
        employees = Employee.objects.filter(id__in=ids_list)
        
        if not employees.exists():
            return Response({"error": "No employees found for the provided IDs"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeTreeNodeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)