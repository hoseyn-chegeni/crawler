from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from spiders.jobinja_update_spider import JobinjaUpdateSpider


class Command(BaseCommand):
    help = "Run Jobinja Update Scrapy spider"

    def handle(self, *args, **options):
        process = CrawlerProcess()
        process.crawl(JobinjaUpdateSpider)
        process.start()
