from django_filters import (
    FilterSet,
    DateFilter,
    ChoiceFilter,
    CharFilter,
    OrderingFilter,
)
from datetime import datetime, timedelta
from django import forms


class BaseFilter(FilterSet):
    created_by_email = CharFilter(field_name="created_by__email", lookup_expr="exact")

    date = DateFilter(
        field_name="created_at",
        label="Date (yyyy-mm-dd)",
        method="filter_by_date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    # Filter by date range (today, this week, this month)
    date_range = ChoiceFilter(
        label="Date Range",
        method="filter_by_date_range",
        choices=(
            ("today", "Today"),
            ("this_week", "This Week"),
            ("this_month", "This Month"),
        ),
    )

    def filter_by_date(self, queryset, name, value):
        return queryset.filter(created_at__date=value)

    def filter_by_date_range(self, queryset, name, value):
        today = datetime.now().date()
        if value == "today":
            return queryset.filter(created_at__date=today)
        elif value == "this_week":
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(created_at__date__range=[start_of_week, end_of_week])
        elif value == "this_month":
            start_of_month = today.replace(day=1)
            end_of_month = start_of_month.replace(
                month=start_of_month.month + 1, day=1
            ) - timedelta(days=1)
            return queryset.filter(
                created_at__date__range=[start_of_month, end_of_month]
            )

    order_by = OrderingFilter(
        fields=(("created_at", "created_at"),),
        field_labels={
            "created_at": "Creation Date",
        },
    )
