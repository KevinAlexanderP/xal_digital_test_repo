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
def create_new_company():
    # Parse data from request
    payload = request.json
    # Validate and sanitize input as needed before passing to the database function
    if not all(key in payload for key in ['company_name', 'address', 'city', 'state', 'zip_code']):
        return jsonify({"error": "Missing required company information"}), 400
    
    # Use the unpacking operator ** to pass the dictionary as keyword arguments
    response = create_company(**payload)
    
    if "error" in response:
        # You could further customize the response based on the specific error
        return jsonify(response), 500
    return jsonify(response), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
