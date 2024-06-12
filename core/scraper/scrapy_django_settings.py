import os
import django
from scrapy.utils.project import get_project_settings

# تنظیم  ماژول تنظیمات جنگو برای  اجرای کامند

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
