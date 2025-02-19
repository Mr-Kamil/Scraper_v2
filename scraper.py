# Scraper_v2 - A web scraper for OLX, Allegro, and Allegro Lokalnie
# Copyright (C) 2024 Kamil Bylinka
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


import os
from websites import *
from web_functions import get_occasions
from db_functions import process_data
import argparse
import json


def _parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--searches', required=True, 
                        help='JSON string or file path')
    parser.add_argument('--db_name', required=False, default='occasions', 
                        help='Database name without extension, to save scraped data')

    global args
    args = parser.parse_args()
    
    if os.path.exists(args.searches):
        with open(args.searches, 'r') as file:
            args.searches = json.load(file)
    else:
        args.searches = json.loads(args.searches)

    return args


def _get_db_name():
    return args.db_name


def _get_unwanted_phrases(config):
    if config["unwanted_phrases"]:
        unwanted_phrases = config["unwanted_phrases"].split("-")
    else:
        unwanted_phrases = []

    return unwanted_phrases


def _print_init_info(json_data):
    for index, search_config in enumerate(json_data):
        print(f"\nSearch Configuration {index + 1}:")
        print(
            ' searched phrase: ', search_config["searched_phrase"], '\n',
            'min price: ', search_config["min_price"], '\n',
            'max price: ', search_config["max_price"], '\n',
            'only new: ', search_config["only_new"], '\n',
            'max page: ', search_config["max_page"], '\n',
            'unwanted phrase: ', search_config["unwanted_phrases"], '\n',
            'by_date: ', search_config["by_date"],
        )


def _open_database(db_name):
    current_directory = os.getcwd()
    os.system(r'start ' + rf"{current_directory}\{db_name}.db")


def _create_website_instance(website_class, json):
    return website_class(
        json["searched_phrase"], 
        json["min_price"], 
        json["max_price"], 
        json["only_new"],
        json["by_date"],
    )


def _create_occasion_list(websites, headers, config):
    occasion_list = []
    for website in websites:
        print()
        occasions = get_occasions(
            headers, website, _get_unwanted_phrases(config), config['max_page']
            )
        for occasion in occasions:
            occasion_list.append(occasion)

    return occasion_list


def _create_table_name(raw_name):
    return raw_name.replace('-', '_')


def main():
    HEADERS = ['TITLE', 'PRICE', 'URL', 'DATE']

    _parse_arguments()

    search_configs = args.searches
    _print_init_info(search_configs)
    db_name = _get_db_name()
    print(f"\nOutput database file name: {db_name}.db")

    summary = []

    for index, config in enumerate(search_configs):
        print(f"\n\nProcessing search {index + 1}: {config}")

        olx = _create_website_instance(Olx, config)
        allegro_lokalnie = _create_website_instance(AllegroLokalnie, config)
        allegro = _create_website_instance(Allegro, config)

        occasion_list = _create_occasion_list((olx, allegro_lokalnie, allegro), HEADERS, config)

        table_name = _create_table_name(config["searched_phrase"])
        process_data(f"{db_name}.db", table_name, occasion_list, HEADERS, summary)

    print('\nAll searches processed. \nDONE\n')
    print('table name:')
    print(*summary, sep='\n')

    _open_database(db_name)


if __name__ == '__main__':
    main()
