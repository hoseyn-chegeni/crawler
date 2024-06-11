from django.db import models


# Create your models here.
class ScrapedData(models.Model):
    title = models.CharField(max_length=2550)
    description = models.TextField()
    employment_type = models.CharField(max_length=2550, null=True, blank=True)
    location = models.CharField(max_length=2550, null=True, blank=True)
    gender = models.CharField(max_length=2550, null=True, blank=True)
    minimum_work_experience = models.CharField(max_length=2550, null=True, blank=True)
    salary = models.CharField(max_length=2550, null=True, blank=True)
    skills = models.CharField(max_length=1024, null=True, blank=True)
    job_classification = models.CharField(max_length=1024, null=True, blank=True)
    military_service_status = models.CharField(max_length=1024, null=True, blank=True)
    hyper_link = models.CharField(max_length=2550, null=True, blank=True)
    company_name = models.CharField(max_length=2550, null=True, blank=True)
    web_app = models.CharField(max_length=2550, null=True, blank=True)

    def __str__(self):
        return self.title
