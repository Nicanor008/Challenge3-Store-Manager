import psycopg2

url = "dbname='storemanager' host='localhost' port='5432' user='postgres' password='nic'"

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
    users = """CREATE TABLE IF NOT EXISTS users(
        employee_no serial PRIMARY KEY NOT NULL,
        username TEXT NOT NULL,
        email CHAR(64) UNIQUE NOT NULL,
        password CHAR(64) NOT NULL,
        role TEXT NOT NULL
    )"""

    products = """CREATE TABLE IF NOT EXISTS products(
        product_id serial PRIMARY KEY NOT NULL,
        category_id TEXT NOT NULL,
        product_name TEXT NOT NULL,
        product_quantity TEXT NOT NULL,
        price INT NOT NULL
    )"""
    
    sales = """CREATE TABLE IF NOT EXISTS sales(
        sales_id serial PRIMARY KEY NOT NULL,
        category_id INT NOT NULL,
        product_id INT NOT NULL,
        product_quantity TEXT NOT NULL,
        price INT NOT NULL,
        attended_by INT NOT NULL
    )"""

    product_categories = """CREATE TABLE IF NOT EXISTS product_categories(
        category_id serial PRIMARY KEY NOT NULL,
        category_name TEXT NOT NULL
    )"""

    queries = [users, products, sales, product_categories]
    return queries