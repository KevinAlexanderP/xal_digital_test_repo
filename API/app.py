from flask import Flask, jsonify, request
from db import fetch_all_tables, fetch_all_tables_centos, create_company, update_company, delete_company, get_company_by_id, create_department, get_department_by_id, update_department, delete_department, create_employee, get_employee_by_id, update_employee, delete_employee

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

@app.route('/departments', methods=['POST'])
def create_department_route():
    data = request.get_json()
    result = create_department(data['department_name'])
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    return jsonify({"message": "Department created successfully", "department_id": result["department_id"]}), 201

@app.route('/departments/<int:department_id>', methods=['GET'])
def get_department_route(department_id):
    result = get_department_by_id(department_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return jsonify(result), 200

@app.route('/departments/<int:department_id>', methods=['PUT'])
def update_department_route(department_id):
    data = request.get_json()
    result = update_department(department_id, data['department_name'])
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    return jsonify({"message": "Department updated successfully", "department_id": department_id}), 200

@app.route('/departments/<int:department_id>', methods=['DELETE'])
def delete_department_route(department_id):
    result = delete_department(department_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return jsonify({"message": "Department deleted successfully", "department_id": department_id}), 200

@app.route('/employees', methods=['POST'])
def create_employee_route():
    data = request.get_json()
    result = create_employee(**data)
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    return jsonify({"message": "Employee created successfully", "employee_id": result["employee_id"]}), 201

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee_route(employee_id):
    result = get_employee_by_id(employee_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return jsonify(result), 200

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee_route(employee_id):
    data = request.get_json()
    result = update_employee(employee_id, **data)
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    return jsonify({"message": "Employee updated successfully", "employee_id": employee_id}), 200

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee_route(employee_id):
    result = delete_employee(employee_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return jsonify({"message": "Employee deleted successfully", "employee_id": employee_id}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')