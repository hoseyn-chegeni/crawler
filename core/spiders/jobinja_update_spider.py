import scrapy
from scraper.models import ScrapedData
import re


class JobinjaUpdateSpider(scrapy.Spider):
    name = "latest_jobinja"
    allowed_domains = ["jobinja.ir"]
    start_urls = [
        "https://jobinja.ir/jobs/latest-job-post-%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%DB%8C-%D8%AC%D8%AF%DB%8C%D8%AF?preferred_before=1718097096&sort_by=published_at_desc"
    ]

    def parse(self, response):
        job_links = response.css(".c-jobListView__titleLink")
        for job in job_links:
            title = job.css("::text").get()
            link = job.css("::attr(href)").get()
            if link is not None:
                link = response.urljoin(link)
                yield scrapy.Request(
                    link, callback=self.parse_job_details, meta={"title": title}
                )

    def parse_job_details(self, response):
        title = response.meta["title"]
        job_description_parts = response.css(
            ".o-box__text::text, .o-box__text.s-jobDesc.c-pr40p::text"
        ).getall()
        job_description = (
            " ".join([part.strip() for part in job_description_parts if part.strip()])
            if job_description_parts
            else "N/A"
        )
        company_name = response.css(".c-companyHeader__name::text").get()
        unique_url = response.css(".c-sharingJobOnMobile__uniqueURL::text").get()

        info_items = response.css(".c-infoBox__item")
        employment_type = location = gender = minimum_work_experience = salary = (
            skills
        ) = job_classification = military_service_status = None
        for item in info_items:
            key = item.css(".c-infoBox__itemTitle::text").get().strip()
            values = item.css(".tags span::text").getall()
            value = ", ".join([v.strip() for v in values if v.strip()])

            if key == "نوع همکاری":
                employment_type = value
            elif key == "موقعیت مکانی":
                location = value
            elif key == "جنسیت":
                gender = value
            elif key == "حداقل سابقه کار":
                minimum_work_experience = value
            elif key == "حقوق":
                salary = value
            elif key == "مهارت‌های مورد نیاز":
                skills = value
            elif key == "دسته‌بندی شغلی":
                job_classification = value
            elif key == "وضعیت نظام وظیفه":
                military_service_status = value

        if not ScrapedData.objects.filter(
            title=title, company_name=company_name
        ).exists():
            ScrapedData.objects.create(
                title=title,
                hyper_link=unique_url,
                description=job_description,
                employment_type=employment_type,
                location=location,
                gender=gender,
                minimum_work_experience=minimum_work_experience,
                salary=salary,
                skills=skills,
                job_classification=job_classification,
                military_service_status=military_service_status,
                company_name=company_name,
                web_app="Jobinja",
            )
