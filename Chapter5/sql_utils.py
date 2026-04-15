import pymysql

def insert_product_info(keyword, title, price, img_url, link, store_name):
    connection = pymysql.connect(
        host='192.168.168.72',
        user='root',
        password='mca_ems',
        port=3308,
        cursorclass=pymysql.cursors.DictCursor,
        database='web_scraping'
    )
    with connection.cursor() as cursor:
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
    connection.commit()


def get_store_products_count(keyword=None):
    connection = pymysql.connect(
        host='192.168.168.72',
        user='root',
        password='mca_ems',
        port=3308,
        cursorclass=pymysql.cursors.DictCursor,
        database='web_scraping'
    )
    with connection.cursor() as cursor:
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
    

def get_price_range_products_count(keyword=None):
    connection = pymysql.connect(
        host='192.168.168.72',
        user='root',
        password='mca_ems',
        port=3308,
        cursorclass=pymysql.cursors.DictCursor,
        database='web_scraping'
    )
    with connection.cursor() as cursor:
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

def get_price_store_scatter_data(keyword=None):
    connection = pymysql.connect(
        host='192.168.168.72',
        user='root',
        password='mca_ems',
        port=3308,
        cursorclass=pymysql.cursors.DictCursor,
        database='web_scraping'
    )
    with connection.cursor() as cursor:
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
                'title': p.get('title', '無標題'), # 新增：產品標題
                'link': p.get('link', '#'),        # 新增：產品連結
                'img_url': p.get('img_url', '')   # 新增：產品圖片連結
            })
        except ValueError:
            continue

    return data