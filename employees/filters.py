import django_filters
from .models import Employee, Hierarchy

class EmployeeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    position = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    hiring_date = django_filters.CharFilter(lookup_expr='icontains')
    id=django_filters.NumberFilter()
    manager_id = django_filters.NumberFilter(method='filter_by_manager_id')

    class Meta:
        model = Employee
        fields = ['name', 'position', 'email', 'hiring_date', 'id', 'manager_id']

    def filter_by_manager_id(self, queryset, name, value):
        if value is not None:
            employee_ids = Hierarchy.objects.filter(manager_id=value).values_list('subordinate_id', flat=True)
            return queryset.filter(id__in=employee_ids)
        return queryset
