import psycopg2
from psycopg2 import extras
from config import aws_db_config, centos_db_config

def fetch_all_tables():
    try:
        # Use the unpacking operator ** to pass the dictionary as keyword arguments
        connection = psycopg2.connect(**aws_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        all_tables_data = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            all_tables_data[table_name] = rows
        cursor.close()
        connection.close()
        return all_tables_data
    except psycopg2.Error as e:
        return {"error": str(e)}

def fetch_all_tables_centos():
    try:
        # Use the unpacking operator ** to pass the dictionary as keyword arguments
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        all_tables_data = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            all_tables_data[table_name] = rows
        cursor.close()
        connection.close()
        return all_tables_data
    except psycopg2.Error as e:
        return {"error": str(e)}