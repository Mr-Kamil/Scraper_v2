import os
from websites import *
from web_functions import get_occasions
from data_functions import process_data
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--searched_phrase', help='for multi phrase: tag1-tag2-...')
    parser.add_argument('--min_price', type=int)
    parser.add_argument('--max_price', type=int)
    parser.add_argument('--only_new', default=False, help='True or False')
    parser.add_argument('--max_page', type=int, default=99, help='default 99')
    parser.add_argument('--unwanted_phrase', required=False, help='for multi phrase: tag1-tag2-...')
    parser.add_argument(
        '--filename', required=False, default='occasions', 
        help='for downloaded occasions, without extension'
        )
    parser.add_argument('--by_date', default=False, help='True or False')


    global args
    args = parser.parse_args()
    return args


def get_searched_phrase():
    return args.searched_phrase
def get_min_price():
    return args.min_price
def get_max_price():
    return args.max_price
def get_only_new():
    return args.only_new
def get_max_page():
    return args.max_page
def get_unwanted_phrase():
    return [n for n in args.unwanted_phrase.split('-')]
def get_filename():
    return args.filename
def get_by_date():
    return args.by_date


def print_init_info():
    print(
        ' searched phrase: ', get_searched_phrase(), '\n',
        'min price: ', get_min_price(), '\n',
        'max price: ', get_max_price(), '\n',
        'only new: ', get_only_new(), '\n',
        'max page: ', get_max_page(), '\n',
        'unwanted phrase: ', get_unwanted_phrase(), '\n',
        'filename: ', get_filename(), '\n',
        'by_date: ', get_by_date(), '\n',
        )


def open_new_occasions_file(filename):
    current_directory = os.getcwd()
    os.system(r'start ' + rf"{current_directory}\new_{filename}.xlsx")


def create_website_instance(website_class):
    return website_class(
        get_searched_phrase(), 
        get_min_price(), 
        get_max_price(), 
        get_only_new(),
        get_by_date(),
    )


def create_occasion_list(websites, headers):
    occasion_list = []
    for website in websites:
        occasions = get_occasions(headers, website, get_unwanted_phrase(), get_max_page())
        for occasion in occasions:
            occasion_list.append(occasion)

    return occasion_list


def main():
    HEADERS = ['TITLE', 'PRICE', 'URL', 'DATE']
    SHEET_NAME = 'Occasions'

    parse_arguments()
    print_init_info()

    olx = create_website_instance(Olx)
    allegro_lokalnie = create_website_instance(AllegroLokalnie)
    occasion_list = create_occasion_list((olx, allegro_lokalnie), HEADERS)

    process_data(get_filename(), occasion_list, HEADERS, SHEET_NAME)
    open_new_occasions_file(get_filename())
    print('\nDone.')


if __name__ == '__main__':
    main()
