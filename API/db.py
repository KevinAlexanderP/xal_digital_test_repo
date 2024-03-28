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
    print(f"Attempting to create a new company with name: {company_name}")

    if not validate_state(state):
        print(f"Invalid state provided for company: {company_name}")
        return {"error": "Invalid state. It must be a 2-letter code and only contain letters."}

    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = """
        INSERT INTO Company (company_name, address, city, state, zip)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING company_id;
        """
        cursor.execute(query, (company_name, address, city, state, zip_code))

        company_id = cursor.fetchone()[0]
        connection.commit()
        print(company_id)
        print(f"Company created successfully with company_id: {company_id}")

    except psycopg2.IntegrityError as e:
        print("IntegrityError encountered:", e)
        if "company_pkey" in str(e):
            return {"error": "Company with the provided company_id already exists."}
        else:
            return {"error": str(e)}
    except psycopg2.Error as e:
        print("Database error encountered:", e)
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

    return {"company_id": company_id}


def update_company(company_id, company_name, address, city, state, zip_code):
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = """
        UPDATE Company
        SET company_name = %s, address = %s, city = %s, state = %s, zip = %s
        WHERE company_id = %s;
        """
        cursor.execute(query, (company_name, address, city, state, zip_code, company_id))
        updated_rows = cursor.rowcount
        connection.commit()
        
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

    if updated_rows == 0:
        return {"error": "Company not found"}
    
    return {"message": "Company updated successfully", "company_id": company_id}

def delete_company(company_id):
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "DELETE FROM Company WHERE company_id = %s;"
        cursor.execute(query, (company_id,))
        deleted_rows = cursor.rowcount
        connection.commit()

    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()
        
    if deleted_rows == 0:
        return {"error": "Company not found"}
    
    return {"message": "Company deleted successfully", "company_id": company_id}

def get_company_by_id(company_id):
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "SELECT * FROM Company WHERE company_id = %s;"
        cursor.execute(query, (company_id,))
        company = cursor.fetchone()

    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()
        
    if company is None:
        return {"error": "Company not found"}
    
    return dict(company)