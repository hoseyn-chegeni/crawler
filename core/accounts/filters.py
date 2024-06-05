import django_filters
from .models import User
from base.filters import BaseFilter


class UserFilter(BaseFilter):
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = User
        fields = {
            "id": ["exact"],
            "email": ["exact", "icontains"],
            "is_active": ["exact"],
        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(first_name__icontains=value) | queryset.filter(
            last_name__icontains=value
        )
