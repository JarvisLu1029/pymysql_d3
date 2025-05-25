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
        database="chapter2"
    )

    with connection.cursor() as cursor:
        # 使用 SQL 查詢語句
        query = "SELECT name, age FROM user WHERE name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchall()
    connection.close()
    return result


def insert_user(name, age, username, password):
    connection = pymysql.connect(
        host=config.get('DB', 'host'),
        user=config.get('DB', 'user'),
        password=config.get('DB', 'password'),
        port=config.getint('DB', 'port'),
        cursorclass=pymysql.cursors.DictCursor,
        database="chapter2"
    )

    with connection.cursor() as cursor:
        sql = """
        INSERT INTO user (name, age, username, password)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (name, age, username, password))
        connection.commit()
    connection.close()
    