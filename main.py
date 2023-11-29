
import os
from classes import *
from functions import *
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('--searched_phrase')
parser.add_argument('--min_price')
parser.add_argument('--max_price')
parser.add_argument('--only_new')

args = parser.parse_args()

def get_searched_phrase():
    # return args.searched_phrase
    return 'Laptop'
def get_min_price():
    # return args.min_price
    return '1000'
def get_max_price():
    # return args.max_price
    return '10000'
def get_only_new():
    # return args.only_new
    return False


def main():
    HEADERS = ['TYTUŁ', 'CENA', 'LINK', 'DATA']
    SHEET_NAME = 'Laptopy'

    unwanted_expressions_in_titles = ['3050u', 'komputer', 'karta graficzna', 'stacjonarny', 'N3060']
    data_file = 'test.csv'

    occasion_list = []

    olx = Olx(get_searched_phrase(), get_min_price(), get_max_price(), get_only_new())
    allegro_lokalnie = AllegroLokalnie(get_searched_phrase(), get_min_price(), get_max_price(), get_only_new())


    occasions = get_laptops_occasions(HEADERS, olx, unwanted_expressions_in_titles)
    for occasion in occasions:
        occasion_list.append(occasion)

    occasions = get_laptops_occasions(HEADERS, allegro_lokalnie, unwanted_expressions_in_titles)
    for occasion in occasions:
        occasion_list.append(occasion)


    write_data(data_file, occasion_list, HEADERS, SHEET_NAME)
    os.system(r'start ' + r"C:\Users\Dom\Desktop\new_occassions.xlsx.lnk")
    print('ALL DONE')


if __name__ == '__main__':
    main()
