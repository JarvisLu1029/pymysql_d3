import pymysql
from configparser import ConfigParser

# 讀取 .env 檔案取得資料庫連線資訊
config = ConfigParser()
config.read('../Chapter1/config.ini')


def sql_query(query, params=None):
    """
    執行 SQL 查詢並返回結果
    """
    # 建立資料庫連線
    connection = pymysql.connect(
        host=config.get('DB', 'host'),
        user=config.get('DB', 'user'),
        password=config.get('DB', 'password'),
        port=config.getint('DB', 'port'),
        cursorclass=pymysql.cursors.DictCursor,
        database='superstore3'
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()

    except Exception as e:
        print(f"Error executing query: {e}")
        
    finally:
        # 確保連線被關閉
        connection.close()

    return result


def get_category_chart_data() -> list[dict[str, int]]:
    # 取得所有 category 的資料
    category_query = """
        SELECT P.category, COUNT(*) as count FROM Products as P 
        JOIN superstore.OrderDetails as O ON P.product_id = O.product_id
        GROUP BY category;
    """
    category_count_result = sql_query(category_query)

    """
    將資料整理成
    [
        {'label': 'Category 1', 'value': 100},
        {'label': 'Category 2', 'value': 200},
        ...
    ]
    """
    category_pie_data = [{'label': item['category'], 'value': item['count']} for item in category_count_result]

    return category_pie_data


def get_sub_category_chart_data(category):
    sub_category_query = """
        SELECT P.sub_category, COUNT(*) as count FROM Products as P 
        JOIN superstore.OrderDetails as O ON P.product_id = O.product_id
        WHERE P.category = %s
        GROUP BY sub_category; 
    """

    sub_category_count_result = sql_query(sub_category_query, (category,))

    sub_category_pie_data = [{'label': item['sub_category'], 'value': item['count']} for item in sub_category_count_result]

    return sub_category_pie_data

def get_quantity_data():
    quantity_query = """
        SELECT 
            P.category,
            P.sub_category, 
            SUM(O.quantity) AS quantity
        FROM 
            superstore.Products AS P
        JOIN 
            superstore.OrderDetails AS O 
            ON P.product_id = O.product_id
        GROUP BY 
            P.category, P.sub_category;
        """
    
    profit_count_result = sql_query(quantity_query)

    # 將資料整理成
    """
    data = {
        name: "Root",
        children: [
            {
                name: "Group A",
                children: [
                    { name: "Item A1", value: 100 },
                    { name: "Item A2", value: 300 }
                ]
            },
            {
                name: "Group B",
                children: [
                    { name: "Item B1", value: 200 },
                    { name: "Item B2", value: 150 },
                    { name: "Item B3", value: 80 }
                ]
            }
        ]
    };
    """

    result = {
        "name": "Quantity",
        "children": []
    }

    for profit_count in profit_count_result:
        category = profit_count["category"]
        sub_category = profit_count["sub_category"]
        profit = profit_count["quantity"]
        
        # 檢查 category 是否已存在於 result 中
        category_found = False
        for child in result["children"]:
            if child["name"] == category:
                category_found = True
                break
        
        # 如果 category 不存在，則新增一個
        if not category_found:
            result["children"].append({
                "name": category,
                "children": []
            })
        
        # 將 sub_category 和 profit 新增到對應的 category 中
        for child in result["children"]:
            if child["name"] == category:
                child["children"].append({
                    "name": sub_category,
                    "value": profit
                })

    return result


def get_products_and_order_details():
    products_and_order_details_query = """
    SELECT category, sub_category, product_name, SUM(sales) AS sales, SUM(profit) AS profit FROM OrderDetails AS O
    JOIN superstore.Products AS P ON O.product_id = P.product_id
    GROUP BY category, sub_category, product_name
    """

    products_and_order_details_result = sql_query(products_and_order_details_query)

    products_and_order_details_result = [{**i, 'profit': round(i['profit']/i['sales'], 2)*100} for i in products_and_order_details_result]

    return products_and_order_details_result