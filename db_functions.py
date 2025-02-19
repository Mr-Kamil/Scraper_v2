import sqlite3


def _create_database(db_name: str, table_name: str, headers: list) -> None:
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    columns = f"({headers[0]} TEXT, {headers[1]} TEXT, {headers[2]} TEXT, {headers[3]} TEXT, "
    columns += f"PRIMARY KEY ({headers[1]}, {headers[2]}))"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {columns}")
    
    connection.commit()
    connection.close()


def _insert_data(
    db_name: str, table_name: str, fresh_data: list[dict], headers: list) -> int:
    connenction = sqlite3.connect(db_name)
    cursor = connenction.cursor()
    
    inserted_data_count = 0

    for data in fresh_data:
        cursor.execute(
            f"""
            INSERT OR IGNORE INTO {table_name} ({', '.join(headers)}) 
            VALUES (?, ?, ?, ?)
            """,
            (data[headers[0]], data[headers[1]], data[headers[2]], data[headers[3]])
        )
        
        inserted_data_count += cursor.rowcount

    connenction.commit()
    connenction.close()
    return inserted_data_count


def process_data(db_name: str, table_name: str, data: list[dict], 
                 headers: list, summary: list) -> None:
    _create_database(db_name, table_name, headers)
    inserted_data_count = _insert_data(db_name, table_name, data, headers)

    summary.append(f"{table_name:<20} {inserted_data_count} new items")