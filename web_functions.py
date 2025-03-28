import datetime
import re
import sys
from typing import Generator


if sys.flags.debug:
    DEBUG = True
else:
    DEBUG = False


def debug(data):
    if DEBUG:
        print(data)


class CaptchaRequiredException(Exception):
    pass


def _get_data_from_web(next_url: str, website: object) -> list[dict]:
    soup = website.get_soup(next_url)
    # debug(soup)
    _ensure_soup_is_correct(soup)
    data_list = []

    data_list.append(website.read_titles(soup))
    data_list.append(website.read_prices(soup))
    data_list.append(website.read_urls(soup))
    data_list.append(website.read_max_page(soup))
    debug(data_list)
    
    return data_list


def _validate_unwanted_phrases(
        title: str, unwanted_phrases: list
        ) -> bool:
    
    if not unwanted_phrases:
        return True
    
    for expression in unwanted_phrases:
        if re.search(expression, title, re.IGNORECASE):
            return False
    return True


def _validate_searched_phrase(
        title: str, website: object
        ) -> bool:
    searched_phrases = website.get_searched_phrase_list()

    for phrase in searched_phrases:
        if phrase.lower() not in title.lower():
            return False
        
    return True


def _format_data(
        data_headers: list, titles: list, price: list, website: object, urls: list, n: int
        ) -> dict:
    
    data =  {
        data_headers[0]: titles[n], 
        data_headers[1]: price, 
        data_headers[2]: website.pre_url + str(urls[n]), 
        data_headers[3]: str(datetime.datetime.today())[:-7]
        }
    
    return data


def _validate_data(
        titles: list, website: object, data_headers: list, unwanted_phrases: str, 
        prices: list, urls: list) -> Generator[dict, dict, dict]:
    
    for n in range(len(titles)):
        if _validate_unwanted_phrases(titles[n], unwanted_phrases):
            if _validate_searched_phrase(titles[n], website):
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
    print(f"Website real max page: {web_max_page}")

    return max_page


def _ensure_data_are_correct(titles, prices, urls):
    if not (len(titles) == len(prices) == len(urls)):
        raise Exception(
            f"Incorrect scraped data:\n"
            f"titles len = {len(titles)}\n"
            f"prices len = {len(prices)}\n"
            f"urls len = {len(urls)}"
        )


def _ensure_soup_is_correct(soup):
    if "geo.captcha-delivery.com" in str(soup):
        raise CaptchaRequiredException("CAPTCHA solving is required !!")


def get_occasions(
        data_headers: list, website: object, unwanted_phrase: list, max_page: int,
        ) -> list[dict]:

    page_num = 0
    occasions_list = []

    while True:
        page_num += 1
        print(f"{website} {page_num}/{max_page}")

        next_url = website.get_url(page_num)
        debug(next_url)
        website.pause()

        try:
            titles, prices, urls, web_max_pages = _get_data_from_web(
                next_url, website
                )
            if page_num == 1:
                max_page = _get_max_page(web_max_pages, max_page)

            _ensure_data_are_correct(titles, prices, urls)

            for data in _validate_data(
                titles=titles, 
                website=website, 
                data_headers=data_headers, 
                unwanted_phrases=unwanted_phrase, 
                prices=prices, 
                urls=urls
                ):
                occasions_list.append(data)

        except CaptchaRequiredException as e:
            print(f"ERROR: {e} - skipping this website")
            return occasions_list
            # if a CAPTCHA is required, it will be required on all pages of this site

        except Exception as e:
            print(f"ERROR \n{next_url} \n{e}")

        if page_num == max_page:
            return occasions_list
        