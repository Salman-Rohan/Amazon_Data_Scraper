import requests
from bs4 import BeautifulSoup
import csv

api_key = 'c72bda3707943d08c93c6c7a3f3e1778'  # ScraperAPI key বসাও
search_query = 'laptop'
url = f'https://www.amazon.com/s?k={search_query}'

scraper_url = f'http://api.scraperapi.com?api_key={api_key}&url={url}'

response = requests.get(scraper_url)
if response.status_code != 200:
    print("Failed to fetch page, status code:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

products = soup.select('div.s-main-slot div[data-component-type="s-search-result"]')

product_list = []

for product in products[:10]:
    try:
        title = product.select_one('h2 span').get_text(strip=True)
    except:
        title = 'N/A'

    try:
        price_whole = product.select_one('span.a-price-whole')
        price_fraction = product.select_one('span.a-price-fraction')
        if price_whole and price_fraction:
            price = price_whole.get_text(strip=True) + '.' + price_fraction.get_text(strip=True)
        else:
            price = product.select_one('span.a-price').get_text(strip=True)
    except:
        price = 'N/A'

    try:
        rating = product.select_one('span.a-icon-alt').get_text(strip=True)
    except:
        rating = 'N/A'

    try:
        link_suffix = product.select_one('a.a-link-normal.s-no-outline')['href']
        link = 'https://www.amazon.com' + link_suffix
    except:
        link = 'N/A'

    product_list.append({
        'title': title,
        'price': price,
        'rating': rating,
        'link': link
    })

# CSV save
keys = product_list[0].keys()
with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(product_list)

print("✅ Data saved to amazon_products.csv")




