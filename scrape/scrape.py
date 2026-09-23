from bs4 import BeautifulSoup
import requests

url = 'https://www.banni.es/en/outdoor-furniture/outdoor-furniture-outdoor-sofa/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

links = soup.select('.rl-gallery-item')
data = []
for link in links:
    data.append({
        'href': link.find('a')['href'],
        'src': link.find('img')['src'],
        'alt': link.find('img')['alt']
    })

# export to json
import json
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

# links = soup.select('rl-gallery-item a')
# print(links)