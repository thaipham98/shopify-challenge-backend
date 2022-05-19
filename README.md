# Shopify challenge - Production engineer intern Fall 22

## Summary
This is an attempt for Shopify Production Engineer Intern - Fall 22 application. Specifically, it contains: 
- All required basic functionalities as stated in the challenge including basic CRUD and additional requirements regarding cities that items are located and their current weather.
- An easy to use UI (implemented with React): https://shopify-challenge-frontend.thaipham98.repl.co/. Link to the repo is: https://github.com/thaipham98/shopify-challenge-frontend
- README and easy dependency installations.

## Installation guide
1. First we'll need to install dependencies by entering:
```bash
pip install -r requirements.txt
```
2. To run the application (user instructions available upon opening), enter:
```bash
python app.py
```

## Repo content
1. `README`:
Containing information about the repo and its usage.
2. `app.py`: Main file to handle user interactions and route to correct API functions.
3. `model.py`: File to handle inialize database connection and handle basic query from RESTful requests.

## API documentations
The server is currently hosted on Replit per requirement. The URL is: https://shopify-challenge-backend.thaipham98.repl.co
### REST API
The sample request and response of REST API is described below
1. View list of items
`GET /items`

##### Request
```
curl --location --request GET 'https://shopify-challenge-backend.thaipham98.repl.co/items'
```
##### Response
```
  [
    {
        "item_id": 1,
        "location": "Seattle",
        "name": "abc",
        "weather": "51.5°F | Clouds, overcast clouds"
    },
    {
        "item_id": 2,
        "location": "New York",
        "name": "abc",
        "weather": "58.7°F | Clouds, overcast clouds"
    },
    {
        "item_id": 3,
        "location": "San Francisco",
        "name": "fau",
        "weather": "65.9°F | Clouds, scattered clouds"
    }
]
```

2. Create an item
`POST /items/add`
##### Request
```
curl --location --request POST 'https://shopify-challenge-backend.thaipham98.repl.co/items/add' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "abc",
    "location": "San Francisco"
}'
```
##### Response
```
{
    "item_id": 4,
    "location": "San Francisco",
    "name": "abc"
}
```
3. Delete an item
`DELETE /items/delete/<item_id>`
##### Request
```
curl --location --request DELETE 'https://shopify-challenge-backend.thaipham98.repl.co/items/delete/1'
```
##### Response
```
{
    "status": "Item deleted successfully"
}
```
4. Edit an item
`PUT /items/edit
##### Request
```
curl --location --request PUT 'https://shopify-challenge-backend.thaipham98.repl.co/items/edit' \
--header 'Content-Type: application/json' \
--data-raw '{
    "item_id": 3,
    "name": "abefae",
    "location": "Boston"
}'
```
##### Response
```
{
    "item_id": 3,
    "location": "Boston",
    "name": "abefae"
}
```

## Additional requirement
I chose the feature: Push a button export product data to a CSV. The feature is avaialble at the client side: https://shopify-challenge-frontend.thaipham98.repl.co/

## Running application
- Client side is deployed on Replit. The URL is: https://shopify-challenge-frontend.thaipham98.repl.co/
- Server side is deployed on Replit. The URL is: https://shopify-challenge-backend.thaipham98.repl.co


