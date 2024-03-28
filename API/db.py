import psycopg2
from psycopg2 import extras
from config import aws_db_config, centos_db_config

## FETCH ALL TABLES OPS
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

## CRUD OPS FOR COMPANIES
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
## CRUD OPS FOR DEPARTMENTS
def create_department(department_name):
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = """
        INSERT INTO department (department_name)
        VALUES (%s)
        RETURNING department_id;
        """
        cursor.execute(query, (department_name,))

        department_id = cursor.fetchone()[0]
        connection.commit()

    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

    return {"department_id": department_id}

def get_department_by_id(department_id):
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "SELECT * FROM department WHERE department_id = %s;"
        cursor.execute(query, (department_id,))
        department = cursor.fetchone()

    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()
        
    if department is None:
        return {"error": "Department not found"}
    
    return dict(department)

def update_department(department_id, department_name):
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = """
        UPDATE department
        SET department_name = %s
        WHERE department_id = %s;
        """
        cursor.execute(query, (department_name, department_id))
        updated_rows = cursor.rowcount
        connection.commit()

    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()
        
    if updated_rows == 0:
        return {"error": "Department not found"}
    
    return {"message": "Department updated successfully", "department_id": department_id}

def delete_department(department_id):
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "DELETE FROM department WHERE department_id = %s;"
        cursor.execute(query, (department_id,))
        deleted_rows = cursor.rowcount
        connection.commit()

    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()
        
    if deleted_rows == 0:
        return {"error": "Department not found"}
    
    return {"message": "Department deleted successfully", "department_id": department_id}

def create_employee(first_name, last_name, phone1, phone2, email, company_id, department_id):
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = """
        INSERT INTO employee (first_name, last_name, phone1, phone2, email, company_id, department_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING employee_id;
        """
        cursor.execute(query, (first_name, last_name, phone1, phone2, email, company_id, department_id))

        employee_id = cursor.fetchone()[0]
        connection.commit()

    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

    return {"employee_id": employee_id}

def get_employee_by_id(employee_id):
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "SELECT * FROM employee WHERE employee_id = %s;"
        cursor.execute(query, (employee_id,))
        employee = cursor.fetchone()

    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()
        
    if employee is None:
        return {"error": "Employee not found"}
    
    return dict(employee)

def update_employee(employee_id, first_name, last_name, phone1, phone2, email, company_id, department_id):
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = """
        UPDATE employee
        SET first_name = %s, last_name = %s, phone1 = %s, phone2 = %s, email = %s, company_id = %s, department_id = %s
        WHERE employee_id = %s;
        """
        cursor.execute(query, (first_name, last_name, phone1, phone2, email, company_id, department_id, employee_id))
        updated_rows = cursor.rowcount
        connection.commit()

    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()
        
    if updated_rows == 0:
        return {"error": "Employee not found"}
    
    return {"message": "Employee updated successfully", "employee_id": employee_id}

def delete_employee(employee_id):
    try:
        connection = psycopg2.connect(**centos_db_config)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "DELETE FROM employee WHERE employee_id = %s;"
        cursor.execute(query, (employee_id,))
        deleted_rows = cursor.rowcount
        connection.commit()

    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()
        
    if deleted_rows == 0:
        return {"error": "Employee not found"}
    
    return {"message": "Employee deleted successfully", "employee_id": employee_id}