import psycopg2
from instance.config import app_config


# url = "dbname='storemanager' host='localhost' port='5432' user='postgres' password='nic'"
class DbSetup(object):
    '''class to setup db connection'''

    def __init__(self, config_name):

        self.url =app_config[config_name].DATABASE_URL
        self.con = psycopg2.connect(self.url)

    def init_db(self):
        return self.con

    def create_tables(self):
        conn = self.url
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

    def drop_tables(self):
        table1="""DROP TABLE IF EXISTS products CASCADE"""
        table2="""DROP TABLE IF EXISTS sales CASCADE"""
        table3="""DROP TABLE IF EXISTS users CASCADE"""
        table4="""DROP TABLE IF EXISTS product_categories CASCADE"""

        conn = self.url
        curr = conn.cursor()
        queries=[table1,table2,table3,table4]
        for query in queries:
            curr.execute(query)
        conn.commit()
        