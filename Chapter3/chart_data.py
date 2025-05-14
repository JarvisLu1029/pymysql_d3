import pymysql
from configparser import ConfigParser

# 讀取 .env 檔案取得資料庫連線資訊
config = ConfigParser()
config.read('.env')


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
    )

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchall()
    
    # connection.close()
    return result


def get_category_chart_data() -> list[dict[str, int]]:
    # 取得所有 category 的資料
    category_query = """
        SELECT P.category, COUNT(*) as count FROM superstore.Products as P 
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
        SELECT P.sub_category, COUNT(*) as count FROM superstore.Products as P 
        JOIN superstore.OrderDetails as O ON P.product_id = O.product_id
        WHERE P.category = %s
        GROUP BY sub_category; 
    """

    sub_category_count_result = sql_query(sub_category_query, (category,))

    sub_category_pie_data = [{'label': item['sub_category'], 'value': item['count']} for item in sub_category_count_result]

    return sub_category_pie_data

def get_profit_data():
    profit_query = """
        SELECT 
            P.category,
            P.sub_category, 
            SUM(O.quantity) AS profit
        FROM 
            superstore.Products AS P
        JOIN 
            superstore.OrderDetails AS O 
            ON P.product_id = O.product_id
        GROUP BY 
            P.category, P.sub_category;

        """
    profit_count_result = sql_query(profit_query)
    print(profit_count_result)

    result = {
        "name": "Profit",
        "children": []
    }

    for profit_count in profit_count_result:
        category = profit_count["category"]
        sub_category = profit_count["sub_category"]
        profit = profit_count["profit"]
        
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