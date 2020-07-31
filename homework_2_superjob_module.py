# инициализация
import requests
import re
from pprint import pprint
from bs4 import BeautifulSoup as bs

def get_superjob_vacancies(url_part, page_count):
    #инициализация
    main_url = 'https://russia.superjob.ru'

    select_list = []
    regex_temp_1 = re.compile('(\d+)—(\d+)(.+)')
    regex_temp_2 = re.compile('[О|о]т(\d+\s?\d+)(.+)')
    regex_temp_3 = re.compile('[Д|д]о(\d+\s?\d+)(.+)')
    headers = { "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.163 Chrome/80.0.3987.163 Safari/537.36" }
    i = 0
    url = main_url + url_part

    # пробег по страницам
    while url and (i < page_count):
        response = requests.get(url, headers=headers)
        if not response.ok:
            return select_list

        soup = bs(response.text, 'lxml')

        # ДОПУСТИМ ЧТО КЛАССЫ АВТОГЕНЕРИРУЕМ  - то будем отталкиваться от текста "Удаленная работа"
        main_block = soup.find('span',text="Удаленная работа").parent.parent.parent.parent.parent.parent.parent
        vacancy_list = main_block.findChildren(recursive=False)

        for vacancy in vacancy_list:

            if not vacancy.find(text="Показать контакты") or not vacancy.find(text="Откликнуться"):
                continue
            select_item = {}

            #Наименование вакансии
            vacancy_tag_name = vacancy.find('a', attrs={"href": True})
            select_item["name"] = vacancy_tag_name.getText()
            #Ссылку на саму вакансию
            select_item["link"] = vacancy_tag_name['href']
            #Сайт откуда собрана вакансия
            select_item["source"] = 'superjob.ru'

            # Предлагаемую зарплату (отдельно мин. и отдельно макс. и отдельно валюта)
            select_item["salary_min"] = None
            select_item["salary_max"] = None
            select_item["salary_currency"] = None
            salary_info = vacancy_tag_name.parent.findNextSibling().getText()
            if salary_info:
                salary_info = salary_info.replace('\xa0', '')
                if salary_info and salary_info != 'По договорённости':
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


            select_list.append(select_item)

        #получение ссылки на следующустраницу
        i += 1

        next_link = main_block.findNextSibling()
        url = main_url + next_link.find('a', {'rel': 'next'})["href"] if next_link else None

    return select_list

if __name__ == '__main__':
    pprint(get_superjob_vacancies('/vacancy/search/?keywords=java%20script%20developer&remote_work_binary=2&click_from=facet', 1))