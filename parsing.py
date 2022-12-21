import requests
from bs4 import BeautifulSoup 
import csv



def get_html(url):
    response = requests.get(url)
    return response.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages_ul = soup.find('div', class_="search-results-table").find('ul')
    last_page = pages_ul.find_all('li')[-1]
    total_pages = last_page.find('a').get('href').split('=')[-1]
    return int(total_pages)


def write_to_csv(data):
    with open('project.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=' ')
        writer.writerow((data['title'], data['price'], data['img'], data['info_']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find_all('div', class_="list-item list-label")

    for product in product_list:
        try:
            title = product.find('h2').text.strip()
        except AttributeError:
            title = 'None'
        try:
            price = product.find('strong').text.strip()
        except AttributeError:
            price = 'None'
        try:
            img = product.find('div', class_="thumb-item-carousel").find('img', class_="lazy-image").get('data-src')
        except AttributeError:
            img = 'None'
        try:
            info_ = product.find('div', class_="block info-wrapper item-info-wrapper").get_text(strip=True)
        except AttributeError:
            info_ = 'None'

        data = {'title': title, 'price': price, 'img': img, 'info_': info_}
        write_to_csv(data)



def main():
    auto_url = 'https://www.mashina.kg/search/all/'
    pages = '?page='

    

    for page in range(1, 11): 
        url_page = auto_url + pages + str(page)
        html = get_html(url_page)
        get_page_data(html)

main()