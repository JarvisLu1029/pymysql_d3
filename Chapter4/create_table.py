import pymysql
import configparser

config = configparser.ConfigParser()
config.read('../Chapter1/config.ini')

conn = pymysql.connect(
    host=config.get('DB', 'host'),
    user=config.get('DB', 'user'),
    password=config.get('DB', 'password'),
    port=config.getint('DB', 'port'),
    cursorclass=pymysql.cursors.DictCursor,
    database='superstore'
)


# 建立資料表
