# инициализация
import requests
import re
from pprint import pprint
from bs4 import BeautifulSoup as bs

def get_hh_vacancies(url_part, page_count):
    #инициализация
    main_url = 'https://vladimir.hh.ru'
    select_list = []
    regex_temp_1 = re.compile('(\d+)-(\d+)\s(.+)')
    regex_temp_2 = re.compile('[О|о]т (\d+\s?\d+)\s(.+)')
    regex_temp_3 = re.compile('[Д|д]о (\d+\s?\d+)\s(.+)')
    headers = { "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.163 Chrome/80.0.3987.163 Safari/537.36" }
    i = 0
    url = main_url + url_part

    # пробег по страницам
    while url and (i < page_count):
        response = requests.get(url, headers=headers)
        if not response.ok:
            return select_list

        #анализ
        soup = bs(response.text, 'lxml')
        main_block = soup.find('div', {'class': 'vacancy-serp'})
        vacancy_list = main_block.findAll('div', {'class': "vacancy-serp-item"})

        for vacancy in vacancy_list:
            select_item = {}

            #Наименование вакансии
            select_item["name"] = vacancy.find('span', {"class" : 'resume-search-item__name'}).span.a.getText()
            select_item["salary_min"] = None
            select_item["salary_max"] = None
            select_item["salary_currency"] = None
            # Предлагаемую зарплату (отдельно мин. и отдельно макс. и отдельно валюта)
            salary_info = vacancy.find('span', {"data-qa": 'vacancy-serp__vacancy-compensation'})
            if salary_info:
                salary_info = salary_info.getText().replace('\xa0', '')
                match = regex_temp_1.match(salary_info)
                if match:
                    select_item["salary_min"] = match.group(1)
                    select_item["salary_max"] = match.group(2)
                    select_item["salary_currency"] = match.group(3)
                else:
                    match = regex_temp_2.match(salary_info)
                    if match:
                        select_item["salary_min"] = match.group(1)
                        select_item["salary_currency"] = match.group(2)
                    else:
                        match = regex_temp_3.match(salary_info)
                        if match:
                            select_item["salary_max"] = match.group(1)
                            select_item["salary_currency"] = match.group(2)

            # #Ссылку на саму вакансию
            select_item["link"] = vacancy.find('span', {"class" : 'resume-search-item__name'}).span.a["href"]
            # #Сайт откуда собрана вакансия
            select_item["source"] = 'hh.ru'

            select_list.append(select_item)

        #получение ссылки на следующустраницу
        i += 1
        next_link = soup.find('a', {'data-qa': 'pager-next'})
        url = main_url + next_link["href"] if next_link else None

    return select_list

if __name__ == '__main__':
    pprint(get_hh_vacancies('/search/vacancy?clusters=true&enable_snippets=true&text=Java+script+developer&schedule=remote&from=cluster_schedule&showClusters=false', 1))