import django_filters
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    position = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    hiring_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Employee
        fields = ['name', 'position', 'email', 'hiring_date']
