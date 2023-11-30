import datetime
import requests
from bs4 import BeautifulSoup
import re
import json


def _get_data_from_page(
        scrapping_dictionary: dict, position: int, soup: object
        ) -> str:

    data = scrapping_dictionary[position]

    if position == 'urls_allegro':
        return(
            [re.split('" href="|" title="', str(a))[1] 
             for a in soup.find_all(data[0], class_=data[1])]
            )
    elif position == 'max_page_all_lok':
        return(
            json.loads(soup.find(scrapping_dictionary[position][0],
            {scrapping_dictionary[position][1]: True})[scrapping_dictionary[position][1]])
            [scrapping_dictionary[position][2]]
                                            )
    elif position != 'urls':
        return(
            [a.get_text() for a in soup.find_all(data[0], class_=data[1])]
            )
    else:
        return(
            [a['href'] for a in soup.find_all(data[0], class_=data[1])]
               )


def _get_data_from_web(
        next_page: str, scrapping_dictionary: dict, parser='html.parser'
        ) -> list[dict]:
    
    data_list = []

    page = requests.get(next_page)
    soup = BeautifulSoup(page.content, parser)

    if page.status_code != 200:
        print("The next page is not loaded: ", page.status_code)

    for position in scrapping_dictionary:
        data = _get_data_from_page(scrapping_dictionary, position, soup)
        data_list.append(data)

    return data_list


def _validate_unwanted_phrase(
        title: str, unwanted_phrase: list
        ) -> bool:
    
    if not unwanted_phrase:
        return True
    
    for expression in unwanted_phrase:
        if re.search(expression, title, re.IGNORECASE):
            return False
    return True


def _format_data(
        data_headers: list, titles: list, price: list, website: object, urls: list, n: int
        ) -> dict:
    
    data =  {
        data_headers[0]: titles[n], 
        data_headers[1]: price, 
        data_headers[2]: website.base_url + str(urls[n]), 
        data_headers[3]: str(datetime.datetime.today())[:-7]
        }
    
    return data


def _validate_data(
        titles: list, website: object, data_headers: list, unwanted_phrase: str, 
        prices: list, urls: list) -> dict:
    
    for n in range(len(titles)):
        if _validate_unwanted_phrase(titles[n], unwanted_phrase):
            try:
                price = int(re.match(r'\d+', prices[n].replace(' ', '')).group(0))
            except:
                price = 0

            if int(website.max_price) >= price >= int(website.min_price):
                data = _format_data(data_headers, titles, price, website, urls, n)
                yield data


def _get_max_page(web_max_page: list, inserted_max_page: int) -> int:
    if (type(web_max_page) == list and len(web_max_page) > 1):
        web_max_page = int(web_max_page[-1]) 
    elif web_max_page == []:
        web_max_page = 1
        
    max_page = min(inserted_max_page, web_max_page)
    return max_page


def get_occasions(
        data_headers: list, website: object, unwanted_phrase: list, max_page: int,
        ) -> list[dict]:

    page_num = 0
    occasions_list = []

    while True:
        page_num += 1
        next_url = website.get_url(page_num)

        titles, prices, urls, web_max_pages = _get_data_from_web(
            next_url, website.get_scraping_tags()
            )

        max_page = _get_max_page(web_max_pages, max_page)

        print(website, f"{page_num}/{max_page}")

        for data in _validate_data(
            titles=titles, 
            website=website, 
            data_headers=data_headers, 
            unwanted_phrase=unwanted_phrase, 
            prices=prices, 
            urls=urls
            ):
            occasions_list.append(data)

        if page_num == max_page:
            return occasions_list
