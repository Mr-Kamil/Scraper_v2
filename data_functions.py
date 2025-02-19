import sqlite3


def _create_database(db_name: str, table_name: str, headers: list) -> None:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    columns = f"({headers[0]} TEXT, {headers[1]} TEXT, {headers[2]} TEXT, {headers[3]} TEXT, "
    columns += f"PRIMARY KEY ({headers[1]}, {headers[2]}))"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {columns}")
    
    conn.commit()
    conn.close()


def _insert_data(
    db_name: str, table_name: str, fresh_data: list[dict], headers: list) -> int:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    inserted_count = 0

    for data in fresh_data:
        cursor.execute(
            f"""
            INSERT OR IGNORE INTO {table_name} ({', '.join(headers)}) 
            VALUES (?, ?, ?, ?)
            """,
            (data[headers[0]], data[headers[1]], data[headers[2]], data[headers[3]])
        )
        
        inserted_count += cursor.rowcount

    conn.commit()
    conn.close()
    return inserted_count


def process_data(db_name: str, table_name: str, data: list[dict], 
                 headers: list, summary: list) -> None:
    _create_database(db_name, table_name, headers)
    inserted_count = _insert_data(db_name, table_name, data, headers)

    summary.append(f"{table_name:<20} {inserted_count} new items")