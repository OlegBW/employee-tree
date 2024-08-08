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
    ordering_fields = '__all__'
    ordering = ['id']

class EmployeesTreeView(APIView):
    def get(self, request, *args, **kwargs):
        tier_1_managers = Employee.objects.filter(position='tier_1')

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

class EmployeeDeleteView(APIView):
    def delete(self, request, pk):
        target_manager = get_object_or_404(Employee, pk=pk)
        subordinates = Hierarchy.objects.filter(manager=target_manager)
        target_position = target_manager.position
        managers = Employee.objects.filter(position=target_position).exclude(id=target_manager.id)

        total_managers = len(managers)
        for (idx, subordinate) in enumerate(subordinates):
            if idx < total_managers:
                subordinate.manager = managers[idx]
                subordinate.save()
            else:
                subordinate.manager = managers[idx % total_managers]
                subordinate.save()

        target_manager.delete()

        return Response({"detail": f"Employee {target_manager.name} deleted successfully."}, status=status.HTTP_204_NO_CONTENT)