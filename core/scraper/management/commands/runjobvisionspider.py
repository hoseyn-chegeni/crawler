from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from spiders.jobvision_spider import JobvisionSpider


class Command(BaseCommand):
    help = "Run JobVision Scrapy spider"

    def handle(self, *args, **options):
        process = CrawlerProcess()
        process.crawl(JobvisionSpider)
        process.start()
