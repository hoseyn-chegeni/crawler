# Crawler
<div dir="rtl">

## فهرست موضوعات
- [نحوه اجرا](#نحوه-اجرا)
- [تنظیمات دیتابیس](#تنظیمات-دیتابیس)
- [راهنمای داکر](#راهنمای-داکر)
- [اجرای دستورات و استخراج اطلاعات از jobvision و joninja](#اجرای-دستورات-و-استخراج-اطلاعات-از-jobvision-و-joninja)
- [راهنمای وب سرویس](#راهنمای-وب-سرویس)
- [ابزار های مورد استفاده](#ابزار-های-مورد-استفاده)
-  [تسک های زمان بندی شده](#تسک-های-زمان-بندی-شده)

- [Unit test & Pytest](#unit-test--pytest)

## نحوه اجرا
برای اجرای پروژه در ابتدا پروژه باید از گیت هاب کلون شود 
   ```bash
      git clone 'https://github.com/yamamoto-tsunetomo/crawler.git'
   ```

 توجه داشته باشید که پیش از اجرای پروژه تنظیمات دیتابیس باید انجام شود 
 برای تنظیم دیتابیس به بخش  [تنظیمات دیتابیس](تنظیمات-دیتابیس) مراجعه نمایید 
سپس دستور زیر را اجرا نمایید 

   ```bash
      docker-compose up --build
   ```
 سپس برای اجری تسک های زمان بندی شده از دستور زیر را اجرا نمایید 
   ```bash
      docker-compose exec web sh -c 'celery -A core beat -l info'
   ```



## تنظیمات دیتابیس
برای اجرا و اتصال دیتابیس postgresql  به پروژه دستورات  زیر را اجرا نمایید 

   ```bash
      sudo -i -u postgres
   ```
   ```bash
      psql
   ```
سپس با دستور زیر دیتابیس پروژه را ایجاد نمابیید
   ```bash
  CREATE DATABASE <db_name>;
   ```
ایجاد یوزر برای دیتابیس 
   ```bash
  CREATE USER myuser WITH PASSWORD 'mypassword';
   ```
سپس با اجرای دستورات زیر تمام دسترسی های لازم را به کاربر دیتابیس بدهید 
   ```bash
GRANT ALL PRIVILEGES ON DATABASE myproject TO myuser;
   ```
   ```bash
GRANT ALL PRIVILEGES ON SCHEMA public TO myuser;
   ```
   ```bash
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myuser;
   ```

   ```bash
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO myuser;
   ```
سپس اطلاعات دیتابیس را در فایل  .env قرار دهید 
توجه داشته باشید که در فایل settings.py تنظیمات دیتابیس باید تغییر کند تا پروژه به جای استفاده از  sqlite3  به دیتابیس مورد نظر متصل شود 

   ```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("SQL_DATABASE"),
        "USER": os.getenv("SQL_USER"),
        "PASSWORD": os.getenv("SQL_PASSWORD"),
        "HOST": os.getenv("SQL_HOST"),
        "PORT": os.getenv("SQL_PORT", "5432"),
        "ATOMIC_REQUESTS": True,
    }
}
```
برای مشاهده جداول و اطلاعات دیتابیس از طریق ترمینال مطابق دستورات زیر عمل کنید
اتصال به کانتیر دیتابیس

   ```bash
docker exec -it your_container_name psql -U <user> -d <db_name>
   ```
لیست دیتابیس های موجود
   ```bash
\l
   ```
اتصال به دیتابیس پروژه
   ```bash
\c <db_name>
   ```
لیست جدول ها
   ```bash
\dt

   ```
اجرای query 
   ```bash
SELECT * FROM table_name;
   ```


## راهنمای داکر
تنظیمات داکر در پروژه با استفاده از پیکربندی Dockerfile  و Docker Compose صورت گرفته است. 
   ```Dockerfile
# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
 ```
این اسکریپت در ابتدا محیط پایتون را در یک کانتیر راه اندازی می کند سپس  dependency ها را نصب میگند  پکیج های نام برده در فایل  requirements.txt  نصب کرده و سپس فایل های پروژه را در کانتیر کپی کرده و سرور چنگو را راه اندازی میکنید 

   ```yml
version: '3.8'

services:
  redis:
    container_name: redis
    image: redis:7.0.11-alpine

  web:
    build: ./core
    command: ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    volumes:
      - ./core/:/usr/src/app/
    ports:
      - "8000:8000"
    env_file:
      - ./core/.env
    depends_on:
      - db
      - redis

  celery:
    container_name: celery
    build:
      context: ./core
    command: celery --app=core worker -l INFO 
    env_file:
      - ./core/.env
    volumes:
      - ./core:/usr/src/app
    depends_on:
      - redis
      - db

  db:
    container_name: db
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./core/.env

volumes:
  postgres_data:

 ```
فایل Docker Compose  سرویس های به کار رفته در پروژه پیکربندی کرده و dependency  های میان سرویس ها را تنظیم و volume هایی برای ذخیره کردن داده های مهم فراهم میکند 
این فایل شامل پروژه اصلی با نام web  دیتابیس پروژه با نام  db و سرویس های  redis و  celery   برای انجام تسک های زمان بندی شده است 


## اجرای دستورات و استخراج اطلاعات از jobvision و joninja
تسک های اصلی برای استخراج داده از سایت های مورد نظر از طریق ابزار  scrapy  تعریف شده اند که دایرکتوری اصلی برنامه در پوشه  spiders قابل مشاهده می باشند 
برای اجرای scrapy دستور زیر را اجرا نمایید 
```bash
scrapy startproject <project_name>
```



برای اجرای این تسک ها دستورات  manage.py  ایجاد شده است  که در دایرکتوری اصلی پوشه scraper/management  تنظیمات این دستورات قابل مشاهده می باشند 
مدل تعریف شده در پوشه scraper/models  با عنوان ScrapedData  برای ذخیره سازی داده های استخراج شده به کار میرود که شامل فیلد های زیر می باشد 
| نام               | توضیحات                                                     |
|--------------------------|-----------------------------------------------------------------|
| title                    | عنوان شغلی استخراج شده                               |
| description              | توضیحات                      |
| employment_type          | نوع همکاری (پاره وقت٫ تمام وقت)                  |
| location                 | شهر                              |
| gender                   | جنسیت                        |
| minimum_work_experience | حداقل سابقه کاری                |
| salary                   | حقوق                           |
| skills                   | توانایی ها                                  |
| job_classification       | دسته بندی شغلی        |
| military_service_status  | نظام وظیفع     |
| hyper_link               | لینک صفحه استخراج شده|
| company_name             | نام شرکت                        |
| web_app                  |سایت استخراخ شده (jobvision  یا  joninja)|

برای اجرای تسک استخراج دیتا از سایت  jobinja دستور زیر را اجرا نمایید 


```bash
docker-compose exec web sh -c 'python manage.py runjobinjaspider'
```

همچنین برای اجرای تسک استخراج دیتا از سایت  jobvision دستور زیر را اجرا نمایید 
```bash
docker-compose exec web sh -c 'python manage.py runjobvisionspider'
```
پس از اجرای دستورات اطلاعات در دیتابیس ذخیره خواهند شده 

<table>
  <tr>
    <td><img src="images/image1.png" alt="Image 1"></td>
    <td><img src="images/image2.png" alt="Image 2"></td>
  </tr>
</table>

## راهنمای وب سرویس
توضیحات مربوط به راهنمای وب سرویس

## ابزار های مورد استفاده
توضیحات مربوط به ابزار های مورد استفاده

## Unit test & Pytest
توضیحات مربوط به Unit test & Pytest


## تسک های زمان بندی شده



</div>





