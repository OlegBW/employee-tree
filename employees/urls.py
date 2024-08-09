from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet,
    EmployeesTreeView,
    EmployeeTreeNodeView,
    EmployeeDeleteView,
    EmployeeUpdateView,
    EmployeeCreateView,
    RegisterView,
)
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "employees/<int:pk>/delete",
        EmployeeDeleteView.as_view(),
        name="delete-employee",
    ),
    path(
        "employees/<int:pk>/update",
        EmployeeUpdateView.as_view(),
        name="update-employee",
    ),
    path("employees/create", EmployeeCreateView.as_view(), name="create-employee"),
    path("employees-tree", EmployeesTreeView.as_view(), name="employees-tree"),
    path("employees-tree/node/", EmployeeTreeNodeView.as_view(), name="employee-node"),
    path(
        "token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("register/", RegisterView.as_view(), name="register"),
]
