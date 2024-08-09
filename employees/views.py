from rest_framework import viewsets, filters
from rest_framework.views import APIView
from .models import Employee, Hierarchy
from .serializers import (
    EmployeeSerializer,
    EmployeeTreeSerializer,
    EmployeeTreeNodeSerializer,
    RegisterSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from .filters import EmployeeFilter
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Subquery, OuterRef
from .data import position_value, positions


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all().annotate(
        manager_id=Subquery(
            Hierarchy.objects.filter(subordinate=OuterRef('pk')).values('manager_id')[:1]
        )
    )

    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EmployeeFilter
    ordering_fields = "__all__"
    ordering = ["id"]


class EmployeesTreeView(APIView):
    def get(self, request, *args, **kwargs):
        tier_1_managers = Employee.objects.filter(position="tier_1")

        serializer = EmployeeTreeSerializer(tier_1_managers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeTreeNodeView(APIView):
    def get(self, request):
        ids = request.query_params.get("ids")

        if not ids:
            return Response(
                {"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        ids_list = ids.split(",")
        employees = Employee.objects.filter(id__in=ids_list)

        if not employees.exists():
            return Response(
                {"error": "No employees found for the provided IDs"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = EmployeeTreeNodeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeDeleteView(APIView):
    def delete(self, request, pk):
        target_manager = get_object_or_404(Employee, pk=pk)
        subordinates = Hierarchy.objects.filter(manager=target_manager)
        target_position = target_manager.position
        managers = Employee.objects.filter(position=target_position).exclude(
            id=target_manager.id
        )
        if not managers:
            return Response(
                {"error": "There are no other managers to redirect subordinates"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_managers = len(managers)
        for idx, subordinate in enumerate(subordinates):
            if idx < total_managers:
                subordinate.manager = managers[idx]
                subordinate.save()
            else:
                subordinate.manager = managers[idx % total_managers]
                subordinate.save()

        target_manager.delete()

        return Response(
            {"detail": f"Employee {target_manager.name} deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class EmployeeUpdateView(APIView):
    def put(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)

        data = request.data

        print(data)
        manager_id = data.get("manager_id")
        position = data.get("position")

        if manager_id:
            if not Employee.objects.filter(pk=manager_id).exists():
                raise ValidationError({"manager_id": "Invalid manager ID"})

        if position:
            if position not in positions:
                raise ValidationError({"position": "Invalid position"})

            new_manager = Employee.objects.get(pk=manager_id)
            print(new_manager)
            if position_value[new_manager.position] - position_value[position] != 1:
                print(new_manager.position, position, position_value[new_manager.position] - position_value[position])
                raise ValidationError({"position": "Invalid hierarchy connection"})
            
            employee_hierarchy = Hierarchy.objects.filter(subordinate=employee).first()
            employee_hierarchy.manager = new_manager
            employee_hierarchy.save()

        if employee.position != position:
            subordinates = Hierarchy.objects.filter(manager=employee)
            target_position = employee.position
            managers = Employee.objects.filter(position=target_position).exclude(
                id=employee.id
            )
            if not managers:
                return Response(
                    {"error": "There are no other managers to redirect subordinates"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            total_managers = len(managers)
            for idx, subordinate in enumerate(subordinates):
                if idx < total_managers:
                    subordinate.manager = managers[idx]
                    subordinate.save()
                else:
                    subordinate.manager = managers[idx % total_managers]
                    subordinate.save()

        serializer = EmployeeSerializer(employee, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeCreateView(APIView):
    def post(self, request):
        data = request.data

        manager_id = data.get("manager_id")
        position = data.get("position")

        if manager_id:
            if not Employee.objects.filter(pk=manager_id).exists():
                raise ValidationError({"manager_id": "Invalid manager ID"})
        
        if position:
            if position not in positions:
                raise ValidationError({"position": "Invalid position"})

            new_manager = Employee.objects.get(pk=manager_id)
            
            if position_value[new_manager.position] - position_value[position] != 1:
                raise ValidationError({"position": "Invalid hierarchy connection"})

        serializer = EmployeeSerializer(data=data)

        if serializer.is_valid():
            new_employee = serializer.save()
            
            if manager_id:
                Hierarchy.objects.create(manager=new_manager, subordinate=new_employee)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)