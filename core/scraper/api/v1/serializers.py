from rest_framework import serializers
from ...models import ScrapedData


class ScrapedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = [
            "id",
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
            "company_name",
            "hyper_link",
            "web_app",
        ]
