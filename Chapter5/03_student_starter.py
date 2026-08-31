"""學生任務檔：完成各關卡函式，讓偵探網頁取得查詢結果。

每個函式都必須呼叫 run_query 並回傳 list[dict]。有外部參數時一律
使用 %s placeholder，禁止用 f-string 拼 SQL，也不可把密碼提交到 Git。
"""

import os
import pymysql
from configparser import ConfigParser

config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

def get_connection():
    return pymysql.connect(
        host=config.get("DB", "DB_HOST"),
        port=config.getint("DB", "DB_PORT"),
        user=config.get("DB", "DB_USER"),
        password=config.get("DB", "DB_PASSWORD"),
        database="detective_academy",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def run_query(connection, sql, params=None):
    """執行 SELECT 並回傳由 dict 組成的 list。"""
    with connection.cursor() as cursor:
        cursor.execute(sql, params or ())
        return cursor.fetchall()


def load_case_brief(connection):
    """第一關：回傳 case_brief 的所有欄位。"""
    # TODO：使用 SELECT 查詢 case_brief View。
    query = "SELECT * FROM case_brief;"
    return run_query(connection, query)


def find_successful_r03_entries(connection, start_time, end_time):
    """第二關：回傳指定晚間成功進入 R03 的 suspect_id、access_time。"""
    # TODO：使用 WHERE、BETWEEN、ORDER BY，找出六名訪客並以 %s 傳入起訖時間。
    query = """
        SELECT suspect_id, access_time
        FROM access_logs
        WHERE result = 'SUCCESS'
        AND action = 'IN'
        AND room_id = 'R03'
        AND access_time BETWEEN %s AND %s
        ORDER BY access_time;
    """
    return run_query(connection, query, (start_time, end_time))


def find_physical_matches(connection):
    """第三關：回傳有橘色痕跡者的 name、shoe_size、has_orange_trace。"""
    # TODO：查出四名橘色痕跡嫌疑人，並依 suspect_id 排序以比較足跡尺寸。
    raise NotImplementedError("請完成 find_physical_matches()")


def find_camera_and_purchase_clues(connection, start_time, end_time):
    """第四關：回傳姓名、seen_time、location、carrying、item_name。

    只保留監視器攜帶物與消費品項相同的人，使用 JOIN 串連三張表。
    """
    # TODO：JOIN suspects、camera_sightings、cafe_orders，並參數化時間。
    raise NotImplementedError("請完成 find_camera_and_purchase_clues()")


def find_deleted_messages(connection, keyword):
    """第五關：回傳已刪除且含關鍵字訊息的雙方姓名與訊息內容。

    欄位：sender_name、receiver_name、sent_at、message_text、is_deleted。
    """
    # TODO：同一張 suspects 表要 JOIN 兩次；LIKE 的值也要當作參數。
    raise NotImplementedError("請完成 find_deleted_messages()")


def find_prime_suspect(connection, start_time, end_time):
    """最終關：回傳唯一嫌犯的 suspect_id、name、job_title。"""
    # TODO：以多表 JOIN 同時驗證五項條件；起訖時間用 %s 參數化。
    raise NotImplementedError("請完成 find_prime_suspect()")


def main():
    connection = get_connection()
    try:
        rows = load_case_brief(connection)
        for row in rows:
            print(row)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
