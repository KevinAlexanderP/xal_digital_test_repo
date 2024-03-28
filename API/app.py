from flask import Flask, jsonify
import psycopg2
from psycopg2 import extras

app = Flask(__name__)

def fetch_all_tables():
    try:
        ## this is for AWS productive database
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='password',
            host='database-2.ccnvwkq3ecvj.us-east-1.rds.amazonaws.com'
        )
        
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
        # this is for CentOs image deployed db
        # we can change this as needed
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='example',
            host='localhost'
        )
        
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

@app.route('/data', methods=['GET'])
def get_data():
    data = fetch_all_tables()
    return jsonify(data)

@app.route('/data_centos', methods=['GET'])
def get_data_centos():
    data = fetch_all_tables_centos()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
