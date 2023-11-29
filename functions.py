import datetime
import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import json
import pandas as pd

today = str(datetime.datetime.today())[:-7]


def get_data_from_web(next_page: str, scrapping_dictionary: dict) -> list[dict, dict, dict]:
    results = []

    page = requests.get(next_page)

    print(page.status_code, type(page.status_code), next_page)
    soup = BeautifulSoup(page.content, 'html.parser')

    for position in scrapping_dictionary:
        data = scrapping_dictionary[position]

        if position == 'urls_allegro':
            results.append([re.split('" href="|" title="', str(a))[1] for a in soup.find_all(data[0], class_=data[1])])
        elif position == 'max_page_all_lok':
            results.append(json.loads(soup.find(scrapping_dictionary[position][0],
                                                {scrapping_dictionary[position][1]: True})[scrapping_dictionary[position][1]])[scrapping_dictionary[position][2]])
        elif position != 'urls':
            results.append([a.get_text() for a in soup.find_all(data[0], class_=data[1])])
        else:
            results.append([a['href'] for a in soup.find_all(data[0], class_=data[1])])

    return results


def remove_duplicates(dictionary_list: list[dict, dict, dict], headers: list) -> list[dict, dict, dict]:
    no_duplicates_list = []
    temp = []
    for dictionary in dictionary_list:
        if dictionary[headers[2]] not in temp:
            no_duplicates_list.append(dictionary)
            temp.append(dictionary[headers[2]])

    return no_duplicates_list


def csv_to_dict_list(file_path: str, headers: list) -> list:
    csv_input = open(file_path, 'r', newline='', encoding='utf-8')
    reader = csv.DictReader(csv_input)

    return [row[headers[2]] + row[headers[1]] for row in reader]


def write_data(data_file_path: str, data_list_with_duplicates: list, headers: list, sheet_name: str) -> None:
    data_list = remove_duplicates(data_list_with_duplicates, headers)
    output_list = []
    exists = False

    if os.path.exists(data_file_path):
        reader_list = csv_to_dict_list(data_file_path, headers)
        exists = True

    with open(data_file_path, 'a', newline='', encoding='utf-8') as data_file_csv_write:
        writer = csv.DictWriter(data_file_csv_write, fieldnames=headers, lineterminator='\n')

        if not exists:
            writer.writeheader()
        writer.writerow({headers[3]: today})

        for data_list_row in data_list:
            if exists:
                if data_list_row[headers[2]] + str(data_list_row[headers[1]]) not in reader_list:
                    output_list.append(data_list_row)
            else:
                output_list.append(data_list_row)

        make_xlsx_file(output_list, data_file_path, sheet_name)

        for output_list_row in output_list:
            writer.writerow(output_list_row)


def make_xlsx_file(input_data: list[dict, ..., dict], data_file_path: str, sheet_name: str) -> None:
    df = pd.DataFrame(input_data)
    writer = pd.ExcelWriter('new_' + data_file_path.split('.')[0] + '.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name=sheet_name)

    for i, column in enumerate(df.columns):
        column_width = max(df[column].astype(str).map(len).max(), len(column)) + 1
        writer.sheets[sheet_name].set_column(i, i, column_width)

    writer.save()


def check_titles_for_unwanted_expressions(title: str, unwanted_expressions: list) -> bool:
    for expression in unwanted_expressions:
        if re.search(expression, title, re.IGNORECASE):
            return False
    return True


def get_laptops_occasions(
        headers: list, website: object, unwanted_expressions: list
        ) -> list[dict, dict, dict]:

    page_num = 0
    occasions_list = []

    while True:
        page_num += 1
        next_page = website.get_url(page=page_num)

        titles, prices, urls, max_pages = get_data_from_web(next_page, website.get_scraping_data())
        max_page = int(max_pages[-1]) if (type(max_pages) == list and len(max_pages) > 1) else max_pages

        for n in range(len(titles)):
            if check_titles_for_unwanted_expressions(titles[n], unwanted_expressions):
                try:
                    price = int(re.match(r'\d+', prices[n].replace(' ', '')).group(0))
                except:
                    pass

                if int(website.max_price) >= price >= int(website.min_price):
                    data = {headers[0]: titles[n], headers[1]: price, headers[2]: website.base_url + str(urls[n]), headers[3]: today}
                    print(data)
                    occasions_list.append(data)

        if page_num == max_page:
            return occasions_list
