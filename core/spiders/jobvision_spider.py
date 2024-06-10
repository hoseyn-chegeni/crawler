import scrapy
import json
from scraper.models import ScrapedData

class JobvisionSpider(scrapy.Spider):
    name = 'jobvision'
    allowed_domains = ['jobvision.ir']
    start_urls = ['https://jobvision.ir/jobs/700000/']

    def parse(self, response):
        post_id = response.meta.get('post_id', 700000)

        script_text = response.xpath('//script[@id="serverApp-state"]/text()').get()
        if script_text:
            try:
                json_data = json.loads(script_text)
            except json.JSONDecodeError:
                self.logger.error("Failed to decode JSON data")
                return

            job_data = json_data.get(f'https://candidateapi.jobvision.ir/api/v1/JobPost/Detail?jobPostId={post_id}')
            if job_data:
                title = job_data.get('title', 'N/A')
                description = job_data.get('description', 'N/A')
                employment_type = job_data.get('workType', {}).get('titleFa', 'N/A')
                location_data = job_data.get('location')
                if location_data:
                    city = location_data.get('city', {}).get('titleFa', 'N/A') if location_data.get('city') else 'N/A'
                    region = location_data.get('region', {}).get('titleFa', 'N/A') if location_data.get('region') else 'N/A'
                    location = f"{city}, {region}"
                else:
                    location = 'N/A, N/A'
                gender = job_data.get('gender', {}).get('titleFa', 'N/A')
                minimum_work_experience = job_data.get('scoreOfWorkExperienceInJobCategory', {}).get('expectedValue', 'N/A')
                salary_data = job_data.get('salary')
                salary = salary_data.get('titleFa', 'N/A') if salary_data else 'N/A'
                job_classification = ', '.join([category.get('titleFa', 'N/A') for category in job_data.get('jobCategories', [])])
                military_service_status_required = job_data.get('shouldDoneMilitaryService', False)
                military_service_status = 'Required' if military_service_status_required else 'Not Required'
                hyper_link = response.url
                company_name = job_data.get('company', {}).get('name', {}).get('titleFa', 'N/A')

                skills_list = job_data.get('softwareRequirements') or []
                skills = ', '.join([f"{skill.get('software', {}).get('titleFa', 'N/A')} ({skill.get('skill', {}).get('titleFa', 'N/A')})" for skill in skills_list])

                ScrapedData.objects.create(
                    title=title,
                    description=description,
                    employment_type=employment_type,
                    location=location,
                    gender=gender,
                    minimum_work_experience=minimum_work_experience,
                    salary=salary,
                    skills=skills,
                    job_classification=job_classification,
                    military_service_status=military_service_status,
                    hyper_link=hyper_link,
                    company_name=company_name,
                    web_app = 'JobVision'

                )
                self.logger.info(f"Saved job post: {title}")

        for i in range(700001, 770000):
            next_page = f'https://jobvision.ir/jobs/{i}/'
            yield scrapy.Request(next_page, callback=self.parse, meta={'post_id': i})
