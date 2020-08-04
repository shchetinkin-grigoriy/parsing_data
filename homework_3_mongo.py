#1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД
from pymongo import MongoClient
from pprint import pprint
import pandas as pd

client = MongoClient('127.0.0.1', 27017)
db = client['vacancy_db']
vacancies = db.vacancies
print(db)

#функция инициализации базы на основе csv
def init_db_from_csv(csv_name, collection):
    collection.drop()
    df = pd.read_csv(csv_name)
    df.drop(columns=[df.columns[0]], inplace=True)
    df_dict = df.to_dict('records')
    pprint (df_dict)
    collection.insert_many(df_dict)

init_db_from_csv('homework_2_vacancies.csv', vacancies)

#2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы. Поиск по двум полям (мин и макс зарплату)
# Данная функция возвращает
def get_vacancies(collection, sum_rubl, curs_usd, curs_eur):
    return list(collection.find({'$or': [{'salary_min': {'$gte' : sum_rubl}, 'salary_currency': {'$nin': ['EUR', 'USD']}}, {'salary_max':{'$gte': sum_rubl}, 'salary_currency': {'$nin': ['EUR', 'USD']}}, \
                                       {'salary_min': {'$gte' : sum_rubl / (22 * 8)}, 'salary_currency': {'$regex': '.*руб.*\/час', '$options':'i'}}, {'salary_max':{'$gte': sum_rubl / (22 * 8)}, 'salary_currency': {'$regex': '.*руб.*\/час', '$options':'i'}}, \
                                       {'salary_min': {'$gte' : sum_rubl / curs_eur}, 'salary_currency': 'EUR'}, {'salary_max':{'$gte': sum_rubl / curs_eur}, 'salary_currency': 'EUR'},
                                       {'salary_min': {'$gte' : sum_rubl / curs_usd}, 'salary_currency': 'USD'}, {'salary_max':{'$gte': sum_rubl / curs_usd}, 'salary_currency': 'USD'}]}))
salary = int(input(f'Please, input Salary: '))
#salary = 100000
pprint(get_vacancies(vacancies, salary, 73, 82))
# for vacancy in vacancies.find({'$or': [{'salary_min': {'$gte' : 100000}, 'salary_currency': {'$nin': ['EUR', 'USD']}}, {'salary_max':{'$gte': 100000}, 'salary_currency': {'$nin': ['EUR', 'USD']}}, \
#                                        {'salary_min': {'$gte' : 100000 / (22 * 8)}, 'salary_currency': {'$regex': '.*руб.*\/час', '$options':'i'}}, {'salary_max':{'$gte': 100000 / (22 * 8)}, 'salary_currency': {'$regex': '.*руб.*\/час', '$options':'i'}}, \
#                                        {'salary_min': {'$gte' : 100000 / 80}, 'salary_currency': 'EUR'}, {'salary_max':{'$gte': 100000 / 80}, 'salary_currency': 'EUR'},
#                                        {'salary_min': {'$gte' : 100000 / 70}, 'salary_currency': 'USD'}, {'salary_max':{'$gte': 100000 / 70}, 'salary_currency': 'USD'}]}):

#3) Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта
from homework_2 import get_current_vacancies
new_vacancies = get_current_vacancies()
for new_vacancy in new_vacancies:
    is_not_found = vacancies.count_documents({'$or': [{'link': new_vacancy['link'], 'source': new_vacancy['source']}]}, limit=1) == 0
    if is_not_found:
        vacancies.insert_one(new_vacancy)
