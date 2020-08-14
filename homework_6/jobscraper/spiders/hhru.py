import scrapy
from scrapy.http import HtmlResponse
from homework_6.jobscraper.items import JobscraperItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://vladimir.hh.ru/search/vacancy?clusters=true&enable_snippets=true&schedule=remote&text=Java+script+developer&only_with_salary=true&salary=225000&from=cluster_compensation&showClusters=true']

    def parse(self, response:HtmlResponse):
        print(response.url)
        next_link = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        job_links = response.xpath("//a[contains(@data-qa,'vacancy-serp__vacancy-title')]/@href").extract()
        for job_link in job_links:
            yield response.follow(job_link, callback=self.vacansy_parse)
        if next_link:
           yield response.follow(next_link, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
         # *Наименование вакансии
         name = response.css('h1.bloko-header-1::text').extract_first()
         # *Зарплата
         salary_text = list(map(str.strip, response.css('p.vacancy-salary > span::text').extract()))
         # *Ссылку на саму вакансию
         url = response.url
         # *Сайт откуда собрана вакансия
         source = 'hh.ru'

         yield JobscraperItem(name=name, url=url, salary_text=salary_text, source=source)
