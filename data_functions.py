import pandas as pd
import csv
import os
import datetime


def _make_csv_file(
        exists: bool, data_file_path: str, fresh_data: list[dict], headers: list
        ) -> None:
    
    with open(data_file_path, 'a', newline='', encoding='utf-8') as data_file_csv_write:
        writer = csv.DictWriter(
            data_file_csv_write, fieldnames=headers, lineterminator='\n'
            )

        if not exists:
            writer.writeheader()
        writer.writerow({headers[3]: str(datetime.datetime.today())[:-7]})

        for output_list_row in fresh_data:
            writer.writerow(output_list_row)


def _prepare_data(
        file_exists: bool, headers: list, duplicates_data: list[dict], data_file_path: str
        ) -> list[dict]:
    
    if not file_exists:
        no_duplicates_data = duplicates_data
        return no_duplicates_data

    no_duplicates_data = []
    reader_list = _csv_to_dict_list(data_file_path, headers)

    for data_list_row in duplicates_data:
        if data_list_row[headers[2]] + str(data_list_row[headers[1]]) not in reader_list:
            no_duplicates_data.append(data_list_row)
    return no_duplicates_data


def _remove_duplicates(
        dictionary_list: list[dict], headers: list
        ) -> list[dict]:
    
    no_duplicates_list = []
    seen_value = set()

    for dictionary in dictionary_list:
        if dictionary[headers[2]] not in seen_value:
            no_duplicates_list.append(dictionary)
            seen_value.add(dictionary[headers[2]])

    return no_duplicates_list


def _csv_to_dict_list(file_path: str, headers: list) -> list:
    csv_input = open(file_path, 'r', newline='', encoding='utf-8')
    reader = csv.DictReader(csv_input)

    return [row[headers[2]] + row[headers[1]] for row in reader]


def _check_file_exists(file_path: str) -> bool:
    if os.path.exists(file_path):
        return True
    return False


def _make_xlsx_file(
        input_data: list[dict], data_file_path: str, sheet_name: str
        ) -> None:
    
    df = pd.DataFrame(input_data)
    writer = pd.ExcelWriter(
        'new_' + data_file_path.split('.')[0] + '.xlsx', engine='xlsxwriter'
        )
    df.to_excel(writer, index=False, sheet_name=sheet_name)

    for i, column in enumerate(df.columns):
        column_width = max(df[column].astype(str).map(len).max(), len(column)) + 1
        writer.sheets[sheet_name].set_column(i, i, column_width)

    writer._save()


def process_data(
        filename: str, data_with_duplicates: list, headers: list, sheet_name: str
        ) -> None:
    filename = f"{filename}.csv"
    no_duplicates_data = _remove_duplicates(data_with_duplicates, headers)
    exists = _check_file_exists(filename)
    fresh_data = _prepare_data(exists, headers, no_duplicates_data, filename)

    _make_csv_file(exists, filename, fresh_data, headers)
    _make_xlsx_file(fresh_data, filename, sheet_name)
