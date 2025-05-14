import pymysql

# Connect to the database
conn = pymysql.connect(
    host='192.168.168.51',
    user='root',
    password='mca_ems',
    port=3307,
    cursorclass=pymysql.cursors.DictCursor,
    database='superstore'
)

# Create tables
with conn.cursor() as cursor:
    # Create a new table
    sql = """
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id VARCHAR(20) PRIMARY KEY,
            customer_name VARCHAR(100),
            segment VARCHAR(50)
        );
    """
    cursor.execute(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS Orders (
            order_id VARCHAR(20) PRIMARY KEY,
            order_date DATE,
            ship_date DATE,
            ship_mode VARCHAR(50),
            customer_id VARCHAR(20),
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        );
    """
    cursor.execute(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS Products (
            product_id VARCHAR(20) PRIMARY KEY,
            category VARCHAR(50),
            sub_category VARCHAR(50),
            product_name VARCHAR(255)
        );
    """
    cursor.execute(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS OrderDetails (
            row_id INT PRIMARY KEY,
            order_id VARCHAR(20),
            product_id VARCHAR(20),
            sales DECIMAL(10,2),
            quantity INT,
            discount DECIMAL(4,2),
            profit DECIMAL(10,2),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        );
    """
    cursor.execute(sql)

    # Commit the changes
    conn.commit()

    sql = """
        SHOW TABLES;
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
