import sqlite3


def _create_database(db_name: str, table_name: str, headers: list) -> None:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    columns = f"({headers[0]} TEXT PRIMARY KEY, {headers[1]} TEXT, {headers[2]} TEXT, {headers[3]} TEXT)"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {columns}")
    
    conn.commit()
    conn.close()


def _insert_data(
    db_name: str, table_name: str, fresh_data: list[dict], headers: list) -> None:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    for data in fresh_data:
        cursor.execute(
            f"""
            INSERT OR IGNORE INTO {table_name} ({', '.join(headers)}) 
            VALUES (?, ?, ?, ?)
            """,
            (data[headers[0]], data[headers[1]], data[headers[2]], data[headers[3]])
        )
    
    conn.commit()
    conn.close()


def _fetch_existing_data(db_name: str, table_name: str, headers: list) -> set:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT {headers[2]}, {headers[1]} FROM {table_name}")
    
    existing_data = {f"{row[0]}{row[1]}" for row in cursor.fetchall()}
    conn.close()
    return existing_data


def _remove_duplicates(data_list: list[dict], headers: list, 
                       existing_data: set) -> list[dict]:
    no_duplicates_list = []
    seen_values = set(existing_data)
    
    for item in data_list:
        key = f"{item[headers[2]]}{item[headers[1]]}"
        if key not in seen_values:
            no_duplicates_list.append(item)
            seen_values.add(key)
    
    return no_duplicates_list


def process_data(db_name: str, table_name: str, data_with_duplicates: list[dict], 
                 headers: list) -> None:
    _create_database(db_name, table_name, headers)
    existing_data = _fetch_existing_data(db_name, table_name, headers)
    fresh_data = _remove_duplicates(data_with_duplicates, headers, existing_data)
    
    if fresh_data:
        _insert_data(db_name, table_name, fresh_data, headers)
