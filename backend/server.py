from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import mysql.connector
import json
import traceback

import products_dao
import orders_dao
import uom_dao

app = Flask(__name__)

@app.before_request
def log_request_info():
    print('Received request:', request.method, request.path)

def get_connection():
    """Get a fresh database connection for each request"""
    return get_sql_connection()

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

@app.errorhandler(Exception)
def handle_exception(error):
    # Log full traceback to console for debugging
    print('Exception in request:')
    traceback.print_exc()
    response = jsonify({'error': str(error)})
    response.status_code = 500
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

@app.route('/getUOM', methods=['GET'])
def get_uom():
    print('Handling /getUOM')
    connection = get_connection()
    print('Got DB connection for /getUOM')
    response = uom_dao.get_uoms(connection)
    print('uom_dao returned', response)
    connection.close()
    response = jsonify(response)
    return response

@app.route('/getProducts', methods=['GET'])
def get_products():
    print('Handling /getProducts')
    connection = get_connection()
    print('Got DB connection for /getProducts')
    response = products_dao.get_all_products(connection)
    print('products_dao returned', response)
    connection.close()
    response = jsonify(response)
    return response

@app.route('/insertProduct', methods=['POST', 'OPTIONS'])
def insert_product():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    request_payload = json.loads(request.form.get('data', '{}'))
    if not request_payload.get('product_name'):
        return jsonify({'error': 'Product name is required'}), 400
    if not request_payload.get('uom_id'):
        return jsonify({'error': 'Unit of measure is required'}), 400
    if not request_payload.get('price_per_unit'):
        return jsonify({'error': 'Price per unit is required'}), 400

    connection = get_connection()
    product_id = products_dao.insert_new_product(connection, request_payload)
    connection.close()
    return jsonify({'product_id': product_id})

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    connection = get_connection()
    response = orders_dao.get_all_orders(connection)
    connection.close()
    response = jsonify(response)
    return response

@app.route('/insertOrder', methods=['POST', 'OPTIONS'])
def insert_order():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    request_payload = json.loads(request.form.get('data', '{}'))
    connection = get_connection()
    order_id = orders_dao.insert_order(connection, request_payload)
    connection.close()
    return jsonify({'order_id': order_id})

@app.route('/deleteProduct', methods=['POST', 'OPTIONS'])
def delete_product():
    connection = get_connection()
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    connection.close()
    response = jsonify({
        'product_id': return_id
    })
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(host='127.0.0.1', port=5000, use_reloader=False)

