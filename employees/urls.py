from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, EmployeesTreeView, EmployeeTreeNodeView, EmployeeDeleteView, EmployeeUpdateView, EmployeeCreateView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('employees/<int:pk>/delete', EmployeeDeleteView.as_view(), name='delete-employee'),
    path('employees/<int:pk>/update', EmployeeUpdateView.as_view(), name='update-employee'),
    path('employees/create', EmployeeCreateView.as_view(), name='create-employee'),
    path('employees-tree', EmployeesTreeView.as_view(), name='employees-tree'),
    path('employees-tree/node/',EmployeeTreeNodeView.as_view(), name='employee-node')
]