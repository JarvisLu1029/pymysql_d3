import pymysql
from configparser import ConfigParser

config = ConfigParser()
config.read('../Chapter1/config.ini')


class WebScrapingDB:
    def __init__(self, database="web_scraping"):
        self.connection = pymysql.connect(
            host=config.get('DB', 'host'),
            user=config.get('DB', 'user'),
            password=config.get('DB', 'password'),
            port=config.getint('DB', 'port'),
            cursorclass=pymysql.cursors.DictCursor,
            database=database
        )

    def create_database(self):
        with self.connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS web_scraping;")
            print("已建立資料庫: web_scraping")


    def create_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS store (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) UNIQUE,
                    url VARCHAR(255)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    keyword VARCHAR(100),
                    title VARCHAR(255),
                    price VARCHAR(50),
                    img_url TEXT,
                    link VARCHAR(255) UNIQUE,
                    init_fetch_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fetch_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    store_id INT,
                    FOREIGN KEY (store_id) REFERENCES store(id)
                );
            """)

            cursor.execute("SHOW TABLES;")            
            tables = cursor.fetchall()
            for table in tables:
                print(f"已建立TABLE: {list(table.values())[0]}")


    def insert_store(self, name, url):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO store (name, url) VALUES (%s, %s) 
                ON DUPLICATE KEY UPDATE url=VALUES(url);
            """, (name, url))
        self.connection.commit()


    def insert_product_info(self, keyword, title, price, img_url, link, store_name):
        with self.connection.cursor() as cursor:
            # 取得 store_id
            cursor.execute("SELECT id FROM store WHERE name = %s;", (store_name,))
            store = cursor.fetchone()
            if store is None:
                print(f"Store '{store_name}' not found.")
                return
            store_id = store['id']

            # 插入產品資料
            cursor.execute("""
                INSERT INTO products (keyword, title, price, img_url, link, store_id) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                ON DUPLICATE KEY UPDATE title=VALUES(title), price=VALUES(price), img_url=VALUES(img_url), fetch_at=CURRENT_TIMESTAMP;
            """, (keyword, title, price, img_url, link, store_id))
        self.connection.commit()


    def get_store_products_count(self, keyword=None):
        with self.connection.cursor() as cursor:
            if keyword:
                sql = """
                    SELECT store.name, COUNT(*) AS count FROM products
                    JOIN store ON products.store_id = store.id
                    WHERE products.keyword LIKE %s
                    GROUP BY store.id;
                """
                cursor.execute(sql, (f'%{keyword}%',))
            else:
                sql = """
                    SELECT store.name, COUNT(*) AS count FROM products
                    JOIN store ON products.store_id = store.id
                    GROUP BY store.id;
                """
                cursor.execute(sql)
            result = cursor.fetchall()
        
        data = [{'store': row['name'], 'count': row['count']} for row in result]

        return data
        

    def get_price_range_products_count(self, keyword=None):
        with self.connection.cursor() as cursor:
            if keyword:
                sql = """
                    SELECT price FROM products
                    WHERE keyword LIKE %s;
                """
                cursor.execute(sql, (f'%{keyword}%',))
            else:
                sql = """
                    SELECT price FROM products;
                """
                cursor.execute(sql)
            result = cursor.fetchall()
        
            price_ranges = {
            '~NT$1000': 0,
        }
        for i in range(1000, 9001, 1000):
            price_ranges[f'NT${i}-{i+999}'] = 0

        price_ranges['NT$10001+'] = 0

        for p in result:
            try:
                # 清理價格字串並轉換為整數
                price = int(p.get('price', '$0').replace('$', '').replace(',', ''))
                
                if price <= 1000:
                    price_ranges['~NT$1000'] += 1
                elif price >= 10001:
                    price_ranges['NT$10001+'] += 1
                else:
                    range_key = f'NT${(price // 1000) * 1000}-{(price // 1000) * 1000 + 999}'
                    price_ranges[range_key] += 1

            except ValueError:
                # 忽略價格格式不正確的資料
                continue

        # 轉換為 D3 易於處理的格式
        data = [{'range': k, 'count': v} for k, v in price_ranges.items()]

        return data

    def get_price_store_scatter_data(self, keyword=None):
        with self.connection.cursor() as cursor:
            if keyword:
                sql = """
                    SELECT products.price AS price, products.title AS title, products.link AS link, products.img_url AS img_url, store.name AS store
                    FROM products
                    JOIN store ON products.store_id = store.id
                    WHERE products.keyword LIKE %s;
                """
                cursor.execute(sql, (f'%{keyword}%',))
            else:
                sql = """
                    SELECT products.price AS price, products.title AS title, products.link AS link, products.img_url AS img_url, store.name AS store
                    FROM products
                    JOIN store ON products.store_id = store.id;
                """
                cursor.execute(sql)
            result = cursor.fetchall()

        data = []
        for p in result:
            try:
                price = int(p.get('price', '$0').replace('$', '').replace(',', ''))
                if price >= 10000:
                    continue  # 過濾掉價格超過 NT$10,000 的資料
                data.append({
                    'store': p.get('store', '未知商店'),
                    'price': price,
                    'title': p.get('title', '未知標題'),
                    'link': p.get('link', '#'),
                    'img_url': p.get('img_url', '')
                })
            except ValueError:
                # 忽略價格格式不正確的資料
                continue

        return data
