import os
from websites import *
from web_functions import get_occasions
from db_functions import process_data
import argparse
import json


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--searches', required=False, 
                        help='JSON string or file path')
    parser.add_argument('--filename', required=False, default='occasions', 
                        help='Filename without extension, to save scraped data')

    global args
    args = parser.parse_args()
    
    if os.path.exists(args.searches):
        with open(args.searches, 'r') as f:
            args.searches = json.load(f)
    else:
        args.searches = json.loads(args.searches)

    return args


def get_filename():
    return args.filename


def get_unwanted_phrase(config):
    if config["unwanted_phrase"]:
        unwanted_phrase = config["unwanted_phrase"].split("-")
    else:
        unwanted_phrase = []

    return unwanted_phrase


def print_init_info(json_data):
    for index, search_config in enumerate(json_data):
        print(f"\nSearch Configuration {index + 1}:")
        print(
            ' searched phrase: ', search_config["searched_phrase"], '\n',
            'min price: ', search_config["min_price"], '\n',
            'max price: ', search_config["max_price"], '\n',
            'only new: ', search_config["only_new"], '\n',
            'max page: ', search_config["max_page"], '\n',
            'unwanted phrase: ', search_config["unwanted_phrase"], '\n',
            'by_date: ', search_config["by_date"],
        )


def open_database(filename):
    current_directory = os.getcwd()
    os.system(r'start ' + rf"{current_directory}\{filename}.db")


def create_website_instance(website_class, json):
    return website_class(
        json["searched_phrase"], 
        json["min_price"], 
        json["max_price"], 
        json["only_new"],
        json["by_date"],
    )


def create_occasion_list(websites, headers, config):
    occasion_list = []
    for website in websites:
        print()
        occasions = get_occasions(
            headers, website, get_unwanted_phrase(config), config['max_page']
            )
        for occasion in occasions:
            occasion_list.append(occasion)

    return occasion_list


def _create_table_name(raw_name):
    return raw_name.replace('-', '_')


def main():
    HEADERS = ['TITLE', 'PRICE', 'URL', 'DATE']

    parse_arguments()

    search_configs = args.searches
    print_init_info(search_configs)
    filename = get_filename()
    print(f"\nOutput database file name: {filename}")

    summary = []

    for index, config in enumerate(search_configs):
        print(f"\n\nProcessing search {index + 1}: {config}")

        olx = create_website_instance(Olx, config)
        allegro_lokalnie = create_website_instance(AllegroLokalnie, config)
        allegro = create_website_instance(Allegro, config)

        # occasion_list = create_occasion_list((olx, allegro_lokalnie, allegro), HEADERS, config)
        occasion_list = create_occasion_list((olx, allegro_lokalnie), HEADERS, config)

        table_name = _create_table_name(config["searched_phrase"])
        process_data(f"{filename}.db", table_name, occasion_list, HEADERS, summary)

    print('\nAll searches processed. \nDONE\n')
    print('table name:')
    print(*summary, sep='\n')

    open_database(filename)


if __name__ == '__main__':
    main()
