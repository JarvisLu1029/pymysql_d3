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
    # 取得所有 category 的資料

    """
    將資料整理成
    [
        {'label': 'Category 1', 'value': 100},
        {'label': 'Category 2', 'value': 200},
        ...
    ]
    """


def get_sub_category_chart_data(category):
    # 取得特定 category 的 sub_category 資料
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
    data = [
            { sales: 10, profit: 20, product_name: "A" },
            { sales: 30, profit: 40, product_name: "B" },
            { sales: 50, profit: 60, product_name: "C" },
            { sales: 70, profit: 80, product_name: "D" },
            { sales: 50, profit: 90, product_name: "C" },
            { sales: 90, profit: 100, product_name: "E" }
        ];
    """

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

