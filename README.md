# Challenge3-Store-Manager
This is a store manager API endpoints that implements CRUD functionality to be used in a store web application.

### What you can Achieve
1. Admin can add a product
2. Admin/store attendant can fetch all products
3. Admin/store attendant can fetch a specific product
4. Store attendant can add a sale order record
5. Admin can get all sale order records
6. Admin registers a store attendant
7. Admin and store attendant login to the system

### API Endpoints
| API Endpoint | Functionality |
| -----------  | ------------- |
| POST /auth/signup |  Register a new user |
| POST /auth/login |  Logins in a user and generates a token |
| GET /products |  Fetch all products |
| POST /products |  Create a single product into products list |
| GET /products/<productsId> |  Fetch a single product into products list |


### How to run tests
This project has been implemented using unit tests. This is how you can test the endpoints:
* `git clone https://github.com/Nicanor008/https://github.com/Nicanor008/Challenge3-Store-Manager.git`
* `cd Challenge3-Store-Manager`
* Activate the virtual environment `virtualenv venv'
* Install all dependencies required `pip install -r requirements.txt`
* Now run the unittests `nosetests` or `nosetests app/tests/v1`
* Run the local server `flask run` or `python run.py`


