from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, EmployeesTreeView, EmployeeTreeNodeView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('employees-tree', EmployeesTreeView.as_view(), name='employees-tree'),
    path('employees-tree/node/',EmployeeTreeNodeView.as_view(), name='employee-node')
]