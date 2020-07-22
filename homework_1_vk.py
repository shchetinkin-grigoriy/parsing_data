
#https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=V
import requests
import json
from pprint import pprint
# инициализация
vk_url = 'https://api.vk.com/method/'
access_token = "..."
version = 5.52

# получение друзей онлайн
method_friends = 'friends.getOnline'
method_friends_params = {"v": version, "access_token": access_token}

response = requests.get(vk_url + method_friends, params=method_friends_params)
response_json = response.json()
pprint(f'Response body is: {response_json}')

# получение более детальной информации о друзьях
method_users_get = 'users.get'
method_users_param = {"v": version, "access_token": access_token, "user_ids[]" : response_json['response']}

response = requests.get(vk_url + method_users_get, params=method_users_param)
print(response.ok)
print(response.url)
pprint(response.json())
with open('lesson_1_vk.json','w') as f:
    json.dump(response.json(), f)

