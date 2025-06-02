import pymysql
import configparser

config = configparser.ConfigParser()
config.read('../Chapter1/config.ini')

def create_superstore_tables(database):
    conn = pymysql.connect(
        host=config.get('DB', 'host'),
        user=config.get('DB', 'user'),
        password=config.get('DB', 'password'),
        port=config.getint('DB', 'port'),
        cursorclass=pymysql.cursors.DictCursor,
        database=database
    )

    # Create tables
    with conn.cursor() as cursor:
        # 建立 Customers


        # 建立 Orders


        # 建立 Products


        # 建立 OrderDetails

