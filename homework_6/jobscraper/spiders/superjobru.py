import scrapy
from scrapy.http import HtmlResponse
from homework_6.jobscraper.items import JobscraperItem

class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=java%20script&remote_work_binary=2&payment_defined=1&click_from=facet']

    def parse(self, response: HtmlResponse):
        print(response.url)
        next_link = response.xpath("//a[contains(@class,'f-test-button-dalshe')]/@href").extract_first()
        job_links = response.xpath("//a[contains(@class,'_6AfZ9')]/@href").extract()
        for job_link in job_links:
            yield response.follow(job_link, callback=self.vacansy_parse)
        if next_link:
            yield response.follow(next_link, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):

         # *Наименование вакансии
         name = response.css('h1::text').extract_first()
         # *Зарплата
         salary_text = response.xpath("//span[@class = '_1OuF_ ZON4b']//span[contains(@class,'_2Wp8I')]/text()").extract()
         # *Ссылку на саму вакансию
         url = response.url
         # *Сайт откуда собрана вакансия
         source = 'superjob.ru'

         yield JobscraperItem(name=name, url=url, salary_text=salary_text, source=source)
