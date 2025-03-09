# Data Processing API
## Setup Instructions
- Clone the repository
```console
$ git clone https://github.com/Yuyi-hao/technical_assignment_opinium.ai.git
$ cd technical_assignment
```
- Set environment variable copy `sample.env` into `.env` and set the value of variables
```console
$ cp sample.env .env
```

- Create a virtual environment
```console
$ python -m venv .venv
# activate environment
$ .venv\Script\activate # windows
$ . .venv/bin/activate # linux/mac
```

- Install dependencies
```console
$ pip install -r requirements.txt
```
- Run the application
```console
$ python main.py
```

## Data Pipeline Architecture
- User Data: Fetched from randomuser.me.
- Product Data: Fetched from FakeStore API.
- Transaction Data: Fetched from Mockaroo API.

## Processing Steps:
- Normalize and store data in memory.
- Map transactions to users via phone numbers.
- Assign random product IDs to transactions (due to missing mapping).

## API Endpoints

1. Retrieve Processed Data
```
GET /data/{entity_type}
entity_type: users, products, transactions
Response: JSON array of requested data
```

2. User Spending Insights
```
GET /insights/users
Response: json
{"user": "John Doe", "total_spent": 250.5}
```
3. Product Popularity Insights
```
GET /insights/products
Response:json
{"category": "electronics", "top_selling": "Wireless Earbuds"}
```








