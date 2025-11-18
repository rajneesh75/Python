import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
# find all book containers
books = soup.find_all('article', class_='product_pod')

with open('books.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Price'])
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        print(title, '-', price)
        writer.writerow([title, price])
