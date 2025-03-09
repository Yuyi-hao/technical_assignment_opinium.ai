from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from data_processing import *

app = Flask(__name__)

@app.route('/data/<string:entity_type>', methods=['GET'])
def get_data(entity_type):
    if entity_type in processed_data:
        return jsonify(processed_data[entity_type])
    return jsonify({'error': 'Invalid entity type'}), 400

@app.route('/insights/users', methods=['GET'])
def user_insights():
    user_spending = {}
    for transaction in processed_data['transactions']:
        user_phone = transaction['data']['user_phone']
        product_id = transaction['data'].get('product_id', -1)  # Assuming 'amount' exists
        if product_id == -1:
            continue
        else:
            for product in processed_data['products']:
                if product['data']['id'] == product_id:
                    amount = product['data']['price']
                    break
        user_spending[user_phone] = user_spending.get(user_phone, 0) + amount
    
    insights = [{'user_phone': k, 'total_spent': v} for k, v in user_spending.items()]
    return jsonify(insights)

@app.route('/insights/products', methods=['GET'])
def product_insights():
    product_stats = []
    for product in processed_data['products']:
        product_data = product['data']
        product_stats.append({
            'product_id': product_data['id'],
            'name': product_data['title'],
            'sold_count': product_data['sold_count'],
            'rating': product_data['rating']
        })
    
    product_stats.sort(key=lambda x: x['sold_count'], reverse=True)
    return jsonify(product_stats)

if __name__ == '__main__':
    # process data
    load_dotenv()
    process_user_data()
    process_product_data()
    process_transaction_data(key=os.getenv('MOCKAROO_API_KEY'))
    app.run(debug=True)