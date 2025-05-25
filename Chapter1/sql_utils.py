# 引入所需套件
import pymysql
from configparser import ConfigParser
from pprint import pprint

# 讀取 config.ini 檔案取得資料庫連線資訊
config = ConfigParser()
config.read('config.ini')



# 建立 function 執行 SQL 查詢
def sql_query(query):
    connection = pymysql.connect(
        host=config.get('DB', 'host'),
        user=config.get('DB', 'user'),
        password=config.get('DB', 'password'),
        port=config.getint('DB', 'port'),
        cursorclass=pymysql.cursors.DictCursor,
    )

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result