import psycopg2

url = "dbname='storemanager' host='localhost' port='5432' user='postgres' password=''"

def connection(url):
    con = psycopg2.connect(url)
    return con
def init_db():
    con = connection(url)
    return con

def create_tables():
    conn = connection(url)
    curr = conn.cursor()
    queries = tables()

    for query in queries:
        curr.execute(query)
    conn.commit()

def tables():
    users = """CREATE TABLE users(
        employeeno INT PRIMARY KEY NOT NULL,
        username TEXT NOT NULL,
        email CHAR(64) NOT NULL,
        password CHAR(64) NOT NULL
    )"""

    products = """CREATE TABLE products(
        productid INT PRIMARY KEY NOT NULL,
        product_category TEXT NOT NULL,
        product_name TEXT NOT NULL,
        product_quantity TEXT NOT NULL,
        price INT NOT NULL,
        added_by INT NOT NULL
    )"""
    
    sales = """CREATE TABLE sales(
        salesid INT PRIMARY KEY NOT NULL,
        productid INT NOT NULL,
        product_quantity TEXT NOT NULL,
        total_price INT NOT NULL,
        attended_by INT NOT NULL
    )"""

    queries = [users, products, sales]
    return queries