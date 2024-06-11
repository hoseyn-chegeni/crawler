from django.urls import path, include

app_name = "scraper"

urlpatterns = [
    path(
        "api/v1/",
        include("scraper.api.v1.urls"),
    )
]
