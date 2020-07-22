from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

response = requests.get('http://127.0.0.1:5000/')
soup = bs(response.text,'lxml')   #html.parser

link = soup.find_all('a')
parent_a = link[0].parent.parent

children = parent_a.findChildren(recursive=False)
child = parent_a.findChild()

#child.find_next_sibling()   -s
#child.find_previous_sibling()    -s

link[0].getText()

elem = soup.find_all(attrs={'class':'red'})
elem2 = soup.find_all(attrs={'class':'paragraph'})

elem3 = soup.find('div',{'id':'d2'})
top3 = soup.find_all('p',limit=3)


text_tag = soup.find(text='Шестой параграф')
pprint(text_tag.parent.findNextSibling())












