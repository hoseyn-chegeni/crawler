import django_filters
from ...models import ScrapedData


class ScrapedDataFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    employment_type = django_filters.CharFilter(lookup_expr="icontains")
    location = django_filters.CharFilter(lookup_expr="icontains")
    gender = django_filters.CharFilter(lookup_expr="icontains")
    minimum_work_experience = django_filters.CharFilter(lookup_expr="icontains")
    salary = django_filters.CharFilter(lookup_expr="icontains")
    skills = django_filters.CharFilter(lookup_expr="icontains")
    job_classification = django_filters.CharFilter(lookup_expr="icontains")
    military_service_status = django_filters.CharFilter(lookup_expr="icontains")
    hyper_link = django_filters.CharFilter(lookup_expr="icontains")
    company_name = django_filters.CharFilter(lookup_expr="icontains")
    web_app = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = ScrapedData
        fields = [
            "title",
            "description",
            "employment_type",
            "location",
            "gender",
            "minimum_work_experience",
            "salary",
            "skills",
            "job_classification",
            "military_service_status",
            "hyper_link",
            "company_name",
            "web_app",
        ]
