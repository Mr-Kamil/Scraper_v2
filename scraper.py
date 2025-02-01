import os
from websites import *
from web_functions import get_occasions
from data_functions import process_data
import argparse
import json


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--searches', required=False, help='JSON string with multiple searches')
    parser.add_argument('--filename', required=False, default='occasions', help='Filename without extension')

    global args
    args = parser.parse_args()
    return args


def get_filename():
    return args.filename
def get_unwanted_phrase(config):
    return [n for n in config['unwanted_phrase'].split('-')]


def print_init_info(json_data):
    print("json_data: ", type(json_data), "\n", json_data)

    for index, search_config in enumerate(json_data):
        print(f"\nSearch Configuration {index + 1}:")
        print(
            ' searched phrase: ', search_config["searched_phrase"], '\n',
            'min price: ', search_config["min_price"], '\n',
            'max price: ', search_config["max_price"], '\n',
            'only new: ', search_config["only_new"], '\n',
            'max page: ', search_config["max_page"], '\n',
            'unwanted phrase: ', search_config["unwanted_phrase"], '\n',
            'by_date: ', search_config["by_date"], '\n',
        )


def open_new_occasions_file(filename):
    current_directory = os.getcwd()
    os.system(r'start ' + rf"{current_directory}\new_{filename}.xlsx")


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


def main():
    HEADERS = ['TITLE', 'PRICE', 'URL', 'DATE']
    SHEET_NAME = 'Occasions'

    parse_arguments()

    search_configs = json.loads(args.searches)
    print_init_info(search_configs)
    filename = get_filename()
    all_occasion_list = []

    for config in search_configs:
        print(f"Processing search: {config}")
        print(filename)

        olx = create_website_instance(Olx, config)
        allegro_lokalnie = create_website_instance(AllegroLokalnie, config)
        allegro = create_website_instance(Allegro, config)

        occasion_list = create_occasion_list((olx, allegro_lokalnie, allegro), HEADERS, config)
        all_occasion_list.extend(occasion_list)

    process_data(filename, all_occasion_list, HEADERS, SHEET_NAME)
    open_new_occasions_file(filename)

    print('\nAll searches processed. Done')


if __name__ == '__main__':
    main()
