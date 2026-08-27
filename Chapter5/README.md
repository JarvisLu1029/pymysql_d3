# PyMySQL 偵探遊戲教材

## 內容物

- `01_detective_case.sql`：建立資料庫、資料表與種子資料。
- `02_student_missions.md`：學生任務卡。
- `03_student_starter.py`：PyMySQL 起始程式。
- `04_teacher_guide.md`：解答、教學流程與評分建議。

## 快速開始

1. 建立資料：

   ```bash
   mysql -u root -p < 01_detective_case.sql
   ```

2. 建立權限受限的學生帳號（由教師以管理者執行）：

   ```sql
   CREATE USER IF NOT EXISTS 'detective_student'@'%'
     IDENTIFIED BY '請換成課堂密碼';
   GRANT SELECT ON detective_academy.* TO 'detective_student'@'%';
   FLUSH PRIVILEGES;
   ```

3. 回到專案根目錄安裝套件：

   ```bash
   pip install -r requirements.txt
   ```

4. 設定環境變數並執行：

   ```bash
   export DB_HOST=127.0.0.1
   export DB_PORT=3306
   export DB_USER=detective_student
   export DB_PASSWORD='課堂密碼'
   uvicorn Chapter5.app:app --reload
   ```

Windows PowerShell 可使用 `$env:DB_HOST="127.0.0.1"` 的形式設定。
正式提供給多人使用時，也請設定足夠長且隨機的 `SESSION_SECRET`；本機課堂練習可使用預設值。

5. 開啟 `http://127.0.0.1:8000`。學生依序完成
   `03_student_starter.py` 的六個查詢函式；每次儲存後重新整理網頁，即可看到
   function 回傳的查詢結果。查詢結果與推理答案都正確時，才會解鎖下一關。

## 網頁結構

- `app.py`：FastAPI 路由、學生 function 載入、查詢檢核與關卡 session。
- `templates/index.html`：Jinja2 遊戲頁面。
- `static/css/detective.css`：偵探小說風格與響應式版面。
- `static/js/game.js`：答案核對與逐關解鎖互動。

## 安全提醒

- 學生帳號只授予 `SELECT`，避免誤刪資料。
- 程式查詢一律使用 `%s` placeholder 與參數 tuple。
- 不要以 f-string 或字串相加拼接學生輸入。
