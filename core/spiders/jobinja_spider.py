import scrapy
from scraper.models import ScrapedData
import re


class JobinjaSpider(scrapy.Spider):
    name = "jobinja"
    allowed_domains = ["jobinja.ir"]
    start_urls = [
        "https://jobinja.ir/jobs?&b=&filters%5Bjob_categories%5D%5B0%5D=&filters%5Bkeywords%5D%5B0%5D=&filters%5Blocations%5D%5B0%5D=&page=1"
    ]  

    def parse(self, response):
        page_numbers = []
        # استخراج تمام لینک های موجود در صفحه
        a_tags = response.css('a[href*="page="]').getall()
        for a_tag in a_tags:
            # دریافت لینک صفحه آخر برای پیمایش در صفحات
            page_number = re.search(r"page=(\d+)", a_tag)
            if page_number:
                page_numbers.append(int(page_number.group(1)))

        # استخراج لینک صفحات جزییات برای دریافت اطلاعات شغلی
        job_links = response.css(".c-jobListView__titleLink")
        for job in job_links:
            title = job.css("::text").get()
            link = job.css("::attr(href)").get()
            if link is not None:
                link = response.urljoin(link)
            #  ایجاد ریکویست برای صفحه جزییات
                yield scrapy.Request(
                    link, callback=self.parse_job_details, meta={"title": title}
                )
        # پیمایش تمام صفحات لیست 
        for i in range(max(page_numbers)):
            next_page = f"https://jobinja.ir/jobs?&b=&filters%5Bjob_categories%5D%5B0%5D=&filters%5Bkeywords%5D%5B0%5D=&filters%5Blocations%5D%5B0%5D=&page={i + 1}"
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_job_details(self, response):
    #   دریافت اطلاعات مشاغل از صفجه جزییات 
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
        ) = job_classification = None
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
