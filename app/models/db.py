import psycopg2
from instance.config import app_config
import os

enviroment = os.environ['ENV']

url = os.getenv('DATABASE_URL')
def connection(url):
    DATABASE_URL = os.environ['DATABASE_URL']
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    # con = psycopg2.connect(app_config[enviroment].DATABASE_URL)
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
        category_id INT,
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

def drop_tables():
    table1="""DROP TABLE IF EXISTS products CASCADE"""
    table2="""DROP TABLE IF EXISTS sales CASCADE"""
    table3="""DROP TABLE IF EXISTS users CASCADE"""
    table4="""DROP TABLE IF EXISTS product_categories CASCADE"""

    conn = connection(url)
    curr = conn.cursor()
    queries=[table1,table2,table3,table4]
    for query in queries:
        curr.execute(query)
    conn.commit()

def default_admin():
    conn = connection(url)
    curr = conn.cursor()
    query = "SELECT * FROM users WHERE email=%s"
    curr.execute(query, ('nickip@gmail.com',))
    admin_result = curr.fetchone()
    if not admin_result:
        query = "INSERT INTO users(username, email, password,role)\
            VALUES(%s,%s,%s,%s)"

        curr.execute(query, ('nickip','nickip@gmail.com', 'nickip', 'admin'))
        conn.commit()
    