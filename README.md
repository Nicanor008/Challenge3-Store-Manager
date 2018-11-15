[![Build Status](https://travis-ci.com/Nicanor008/Challenge3-Store-Manager.svg?branch=develop)](https://travis-ci.com/Nicanor008/Challenge3-Store-Manager)
[![Coverage Status](https://coveralls.io/repos/github/Nicanor008/Challenge3-Store-Manager/badge.svg?branch=develop)](https://coveralls.io/github/Nicanor008/Challenge3-Store-Manager?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/2ae2f909c47dbe872ff6/maintainability)](https://codeclimate.com/github/Nicanor008/Challenge3-Store-Manager/maintainability)


# Store Manager API - Challenge 3
This is a store manager API endpoints that implements CRUD functionality to be used in a store web application.

### What you can Achieve
1. Admin can add a product
2. Admin/store attendant can fetch all products
3. Admin/store attendant can fetch a specific product
4. Store attendant can add a sale order record
5. Admin can get all sale order records
6. Admin registers a store attendant
7. Admin and store attendant login to the system

### Starting the Application
Clone this repo and open it. Setup the environment variables below:
```
Windows
set FLASK_APP=run.py

Linux/Unix
export FLASK_APP=run.py
```
Then run this app
```flask run```
or 
```python run.py```

### API Endpoints
| API Endpoint | Functionality |
| -----------  | ------------- |
| POST /auth/signup |  Register a new user |
| POST /auth/login |  Login a user and generates a token |
| GET /products |  Fetch all products |
| POST /products |  Create a single product into products list |
| GET /products/<product_id> | Fetch a single product
| DELETE /products/<productid> |  Delete a single product |
| PUT /products/<productsid> |  update a single products |
| GET /sales |  Fetch sale records |
| GET /sales/<sales_id> | Fetch a single sale |
| POST /sales |  Add sale records |
| DELETE /sales/<sales_id> | Delete a single sale |
| GET /auth/users |  Fetch all users |
| GET /auth/users/<email> |  Get a single user |


### How to run tests
This project has been implemented using unit tests. This is how you can test the endpoints:
* `git clone https://github.com/Nicanor008/https://github.com/Nicanor008/Challenge3-Store-Manager.git`
* `cd Challenge3-Store-Manager`
* Activate the virtual environment `virtualenv venv'
* Install all dependencies required `pip install -r requirements.txt`
* Now run the unittests `nosetests` or `nosetests app/tests/v1`
* Run the local server `flask run` or `python run.py` and test the endpoints with postman


