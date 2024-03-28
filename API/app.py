from flask import Flask, jsonify, request
from db import fetch_all_tables, fetch_all_tables_centos, create_company

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    data = fetch_all_tables()
    return jsonify(data)

@app.route('/data_centos', methods=['GET'])
def get_data_centos():
    data = fetch_all_tables_centos()
    return jsonify(data)

@app.route('/create_company', methods=['POST'])
def add_company():
    # Extract data from the request
    data = request.get_json()
    
    # Validate incoming JSON payload
    if not all(key in data for key in ['company_name', 'address', 'city', 'state', 'zip_code']):
        return jsonify({"error": "Missing required company information"}), 400
    
    # Call the create_company function with the data
    result = create_company(data['company_name'], data['address'], data['city'], data['state'], data['zip_code'])
    
    # Check for errors from the database operation
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    
    return jsonify({"message": "Company created successfully", "company_id": result["company_id"]}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
