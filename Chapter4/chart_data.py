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
        database='superstore'
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
    # 計算每個主類別的產品訂單數量
    category_query = """

    """

    """
    將資料整理成
    [
        {'label': 'Category 1', 'value': 100},
        {'label': 'Category 2', 'value': 200},
        ...
    ]
    """


    return ""

def get_sub_category_chart_data(category):
    # 計算某個主類別，其子類別的產品訂單數量
    sub_category_query = """

    """

    """
    將資料整理成
    [
        {'label': 'Category 1', 'value': 100},
        {'label': 'Category 2', 'value': 200},
        ...
    ]
    """



def get_products_and_order_details():
    # 取得 products 和 order_details 的資料
    products_order_details_query = """

    """

    """
    將資料整理成
    products_and_order_details_result = [
        {'category': 'Furniture', 'sub_category': 'Bookcases', 'product_name': 'Bush Birmingham Collection Bookcase, Dark Cherry', 'sales': Decimal('825.17'), 'profit': Decimal('-14.29')}, 
        {'category': 'Furniture', 'sub_category': 'Bookcases', 'product_name': 'Sauder Camden County Barrister Bookcase, Planked Cherry Finish', 'sales': Decimal('1064.62'), 'profit': Decimal('2.27')},
        {'category': 'Furniture', 'sub_category': 'Bookcases', 'product_name': 'Sauder Inglewood Library Bookcases', 'sales': Decimal('2154.35'), 'profit': Decimal('14.44')}, 
        {'category': 'Furniture', 'sub_category': 'Bookcases', 'product_name': "O'Sullivan 2-Shelf Heavy-Duty Bookcases", 'sales': Decimal('723.85'), 'profit': Decimal('-18.39')},      
        {'category': 'Furniture', 'sub_category': 'Bookcases', 'product_name': 'Hon Metal Bookcases, Gray', 'sales': Decimal('851.76'), 'profit': Decimal('27.00')}
    ];
    """



    # 回傳 products_and_order_details_result 以及 所有的 子類別名稱
    return ""


def get_quantity_data():
    # 取得所有產品的銷售數量資料
    quantity_query = """

    """

    """
    將資料整理成
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




    return result