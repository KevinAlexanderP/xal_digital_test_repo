from flask import Flask, jsonify, request
from db import fetch_all_tables, fetch_all_tables_centos, create_company, update_company, delete_company, get_company_by_id

app = Flask(__name__)

def validate_company_data(data):
    required_keys = ['company_name', 'address', 'city', 'state', 'zip_code']
    return all(key in data for key in required_keys)

@app.route('/data', methods=['GET'])
def get_data():
    data = fetch_all_tables()
    return jsonify(data)

@app.route('/data_centos', methods=['GET'])
def get_data_centos():
    data = fetch_all_tables_centos()
    return jsonify(data)

@app.route('/companies/<int:company_id>', methods=['GET'])
def get_company_route(company_id):
    result = get_company_by_id(company_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return jsonify(result), 200

@app.route('/companies', methods=['POST'])
def create_company_route():
    data = request.get_json()
    if not validate_company_data(data):
        return jsonify({"error": "Missing required company information"}), 400
    result = create_company(**data)
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    return jsonify({"message": "Company created successfully", "company_id": result["company_id"]}), 201

@app.route('/companies/<int:company_id>', methods=['PUT'])
def update_company_route(company_id):
    data = request.get_json()
    if not validate_company_data(data):
        return jsonify({"error": "Missing required company information"}), 400
    result = update_company(company_id, **data)
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    return jsonify({"message": "Company updated successfully", "company_id": company_id}), 200

@app.route('/companies/<int:company_id>', methods=['DELETE'])
def delete_company_route(company_id):
    result = delete_company(company_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return jsonify({"message": "Company deleted successfully", "company_id": company_id}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')