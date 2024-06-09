from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from spiders.jobinja_spider import JobinjaSpider

class Command(BaseCommand):
    help = 'Run Scrapy spider'

    def handle(self, *args, **options):
        process = CrawlerProcess()
        process.crawl(JobinjaSpider)
        process.start()
