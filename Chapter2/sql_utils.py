import pymysql
import configparser 

config = configparser.ConfigParser()
config.read('../Chapter1/config.ini')


def search_user_by_name(name):
    connection = pymysql.connect(
        host=config.get('DB', 'host'),
        user=config.get('DB', 'user'),
        password=config.get('DB', 'password'),
        port=config.getint('DB', 'port'),
        cursorclass=pymysql.cursors.DictCursor,
        database="employee_management"
    )

    with connection.cursor() as cursor:
        # 使用 SQL 查詢語句
        sql = "SELECT * FROM main_user WHERE name = %s"
        cursor.execute(sql, (name,))
        result = cursor.fetchall()
    connection.close()
    return result


# 將 SQL 查詢寫成 Function 
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
    
    connection.close()
    return result
