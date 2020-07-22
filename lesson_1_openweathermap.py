#https://api.openweathermap.org/data/2.5/weather
#e5e4cd692a72b0b66ea0a6b80255d1c3
import requests
from pprint import pprint
# main_link = 'https://img.gazeta.ru/files3/845/7947845/upload-shutterstock_117062077-pic905v-895x505-99863.jpg'
# response = requests.get(main_link)
#
# print(1)
#
# if response.status_code == 200:
#     with open('sea.jpg','wb') as f:
#         f.write(response.content)


# if response.ok:
#     pass

city = 'Noyabrsk,ru'
appid= 'e5e4cd692a72b0b66ea0a6b80255d1c3'

main_link = 'https://api.openweathermap.org/data/2.5/weather'
weather_params = {'q':city,
          'appid':appid}

response = requests.get(main_link,params=weather_params)
data = response.json()
# pprint(response.json())
print(f'В городе {data["name"]} температура {data["main"]["temp"] - 273.15} градусов')


