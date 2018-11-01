import psycopg2
from instance.config import app_config


# url = "dbname='storemanager' host='localhost' port='5432' user='postgres' password='nic'"
class DbSetup(object):
    def __init__(self, config_name):
        self.url = app_config[config_name].DATABASE_URL
        self.con = psycopg2.connect(self.url)
        
    def connection(self):
        return self.con

    def init_db(self):
        con = self.connection()
        return con

    def create_tables(self):
        conn = self.connection()
        curr = conn.cursor()
        queries = self.tables()

        for query in queries:
            curr.execute(query)
        conn.commit()

    def tables(self):
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