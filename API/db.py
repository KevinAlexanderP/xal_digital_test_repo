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
    
def validate_state(state):
    return len(state) == 2 and state.isalpha()

def create_company(company_name, address, city, state, zip_code):
    if not validate_state(state):
        return {"error": "Invalid state. It must be a 2-letter code and only contain letters."}
    
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Parameterized queries are used to avoid SQL injection
        query = """
        INSERT INTO Company (company_name, address, city, state, zip)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING company_id;
        """
        cursor.execute(query, (company_name, address, city, state, zip_code))
        
        # Fetch the returned company_id of the newly created company
        company_id = cursor.fetchone()[0]
        connection.commit()
        
        cursor.close()
        connection.close()
        return {"company_id": company_id}
    except psycopg2.Error as e:
        return {"error": str(e)}

# Example usage
# response = create_company('Example Inc.', '123 Example St', 'Exampletown', 'EX', '12345')
# print(response)
