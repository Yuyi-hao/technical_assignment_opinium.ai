import requests
import datetime
import uuid
import random

processed_data = {
    'users': [],
    'products': [],
    'transactions': [],
}
def get_phone_num(s):
    phone = ""
    for ch in s:
        if ch.isdigit():
            phone += ch
    return phone
def process_user_data(user_count=20, timeout=20):
    url = f"https://randomuser.me/api/?results={user_count}"
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            data = response.json()["results"]
            for user in data:
                timestamp = datetime.datetime.utcnow().isoformat()
                normalized_data = user
                normalized_data['phone'] = get_phone_num(normalized_data['phone'])
                processed_data['users'].append(
                    {
                        "entity_id": str(uuid.uuid4()),
                        "entity_type": "users",
                        "timestamp": timestamp,
                        "data": normalized_data,
                        "metadata": {
                            "source": url,
                            "processed_at": timestamp
                        }
                    }
                )
        else:
            print(response.status_code)
    except requests.exceptions.ReadTimeout:
        print("Time out occurs. Try again to populate data.")

def process_product_data(timeout=10):
    url = "https://fakestoreapi.com/products"
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            for product in data:
                timestamp = datetime.datetime.utcnow().isoformat()
                normalized_data = product
                normalized_data['sold_count'] = 0
                processed_data['products'].append(
                    {
                        "entity_id": str(uuid.uuid4()),
                        "entity_type": "product",
                        "timestamp": timestamp,
                        "data": normalized_data,
                        "metadata": {
                            "source": url,
                            "processed_at": timestamp
                        }
                    }
                )
        else:
            print("ERROR: ", response.status_code)
    except requests.exceptions.ReadTimeout:
        print("Time out occurs. Try again to populate data.")

def process_transaction_data(key, timeout=10):
    url = f"https://my.api.mockaroo.com/orders.json?key={key}"
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            for transaction in data:
                timestamp = datetime.datetime.utcnow().isoformat()
                normalized_data = transaction
                normalized_data['user_phone'] = normalized_data['user_phone'][4:] # NOTE: removed country code to make it detectable with user as user name can be duplicate
                product_id = random.randint(1, 20) # NOTE: did random id as transaction has no key to map with product 
                normalized_data['product_id'] = product_id
                # increase count on product
                for product in processed_data['products']:
                    if product['data']['id'] == product_id:
                        product['data']['sold_count'] += 1

                processed_data['transactions'].append(
                    {
                        "entity_id": str(uuid.uuid4()),
                        "entity_type": "transaction",
                        "timestamp": timestamp,
                        "data": normalized_data,
                        "metadata": {
                            "source": url,
                            "processed_at": timestamp
                        }
                    }
                )
        else:   
            print("ERROR: ", response.status_code)
    except requests.exceptions.ReadTimeout:
        print("Time out occurs. Try again to populate data.")





