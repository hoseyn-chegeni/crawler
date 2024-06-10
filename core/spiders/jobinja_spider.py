import scrapy
from scraper.models import ScrapedData
import re



class JobinjaSpider(scrapy.Spider):
    name = 'jobinja'
    allowed_domains = ['jobinja.ir']
    start_urls = ['https://jobinja.ir/jobs?&b=&filters%5Bjob_categories%5D%5B0%5D=&filters%5Bkeywords%5D%5B0%5D=&filters%5Blocations%5D%5B0%5D=&page=1']

    def parse(self, response):
        # Extract all <a> tags containing the page attribute
        page_numbers = []
        a_tags = response.css('a[href*="page="]').getall()
        for a_tag in a_tags:
            # Extract the page number from the href attribute
            page_number = re.search(r'page=(\d+)', a_tag)
            if page_number:
                page_numbers.append(int(page_number.group(1)))

        job_titles = response.css('.c-jobListView__titleLink::text').getall()
        for title in job_titles:
            ScrapedData.objects.create(title=title)
        
        for i in range(max(page_numbers)):
            next_page = f'https://jobinja.ir/jobs?&b=&filters%5Bjob_categories%5D%5B0%5D=&filters%5Bkeywords%5D%5B0%5D=&filters%5Blocations%5D%5B0%5D=&page={i + 1}'
            yield scrapy.Request(next_page, callback=self.parse)

