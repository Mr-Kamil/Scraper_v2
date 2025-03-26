import sqlite3


def _create_database(db_name: str, table_name: str, headers: list, erase=False) -> None:
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    if erase:
        cursor.execute(f"DELETE FROM {table_name}") 
    
    columns = f"({headers[0]} TEXT, {headers[1]} TEXT, {headers[2]} TEXT, {headers[3]} TEXT, "
    columns += f"PRIMARY KEY ({headers[1]}, {headers[2]}))"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {columns}")
    
    connection.commit()
    connection.close()


def _insert_data(
    db_name: str, table_name: str, fresh_data: list[dict], headers: list, 
    inserted_data: list
    ) -> int:

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    inserted_data_count = 0

    for data in fresh_data:
        cursor.execute(
            f"""
            INSERT OR IGNORE INTO {table_name} ({', '.join(headers)}) 
            VALUES (?, ?, ?, ?) 
            RETURNING *
            """,
            (data[headers[0]], data[headers[1]], data[headers[2]], data[headers[3]])
        )
        
        row = cursor.fetchone()
        if row:
            inserted_data.append(data)
            inserted_data_count += 1

    connection.commit()
    connection.close()
    
    return inserted_data_count


def process_data(db_name: str, table_name: str, data: list[dict], 
                 headers: list, summary: list, inserted_data, erase=False) -> None:
    _create_database(db_name, table_name, headers, erase)
    inserted_data_count = _insert_data(db_name, table_name, data, headers, inserted_data)

    summary.append(f"{table_name:<20} {inserted_data_count} new items")