import pandas as pd
from pprint import pprint
from homework_2_hh_module import get_hh_vacancies
from homework_2_superjob_module import get_superjob_vacancies

page_count = int(input(f'Введите количество страниц: '))

vacancy_list = []
vacancy_list = vacancy_list + get_hh_vacancies('/search/vacancy?clusters=true&enable_snippets=true&text=Java+script+developer&schedule=remote&from=cluster_schedule&showClusters=false', page_count)
vacancy_list = vacancy_list + get_superjob_vacancies('/vacancy/search/?keywords=java%20script%20developer&remote_work_binary=2&click_from=facet', page_count)
columns = ["source", "name", "link", "source", "salary_min", "salary_max", "salary_currency"]

data_frame = pd.DataFrame({column : [vacancy[column] for vacancy in vacancy_list] for column in columns})
print(data_frame.info())
data_frame.to_csv("homework_2_vacancies.csv")