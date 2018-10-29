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
| POST /api/v1/auth/register |  Register a new user |
| POST /api/v1/auth/login |  Logins in a user and generates a token |
| GET /api/v1/products |  Fetch all products |
| POST /api/v1/products |  Create a single product into products list |
| GET /api/v1/products/<productsId> |  Fetch a single product into products list |
| GET /api/v1/sales |  Fetch all sale records |
| POST /api/v1/sales |  Create sale records into sales list |
| GET /api/v1/sales/<salesId> |  Fetch a sale record into sale list |


### How to run tests
This project has been implemented using unit tests. This is how you can test the endpoints:
* `git clone https://github.com/Nicanor008/https://github.com/Nicanor008/Challenge3-Store-Manager.git`
* `cd Challenge3-Store-Manager`
* Activate the virtual environment `virtualenv venv'
* Install all dependencies required `pip install -r requirements.txt`
* Now run the unittests `nosetests` or `nosetests app/tests/v1`
* Run the local server `flask run` or `python run.py`


