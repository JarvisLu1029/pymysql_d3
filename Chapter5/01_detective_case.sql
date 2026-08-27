-- ============================================================
-- PyMySQL 偵探教室：消失的黃金吐司
-- 適用：MySQL 8.0+
-- 建議：教師先執行本檔，再讓學生用 PyMySQL 查詢。
-- ============================================================

DROP DATABASE IF EXISTS detective_academy;
CREATE DATABASE detective_academy
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE detective_academy;

CREATE TABLE suspects (
    suspect_id INT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    job_title VARCHAR(50) NOT NULL,
    shoe_size DECIMAL(3,1) NOT NULL,
    phone_last4 CHAR(4) NOT NULL,
    has_blue_jacket BOOLEAN NOT NULL DEFAULT FALSE,
    interview_note VARCHAR(255)
);

CREATE TABLE rooms (
    room_id CHAR(3) PRIMARY KEY,
    room_name VARCHAR(50) NOT NULL,
    floor_no INT NOT NULL
);

CREATE TABLE access_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    suspect_id INT NOT NULL,
    room_id CHAR(3) NOT NULL,
    action ENUM('IN', 'OUT') NOT NULL,
    access_time DATETIME NOT NULL,
    result ENUM('SUCCESS', 'DENIED') NOT NULL,
    FOREIGN KEY (suspect_id) REFERENCES suspects(suspect_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    INDEX idx_access_time (access_time),
    INDEX idx_access_room (room_id)
);

CREATE TABLE camera_sightings (
    sighting_id INT PRIMARY KEY AUTO_INCREMENT,
    camera_code VARCHAR(10) NOT NULL,
    suspect_id INT NULL,
    seen_time DATETIME NOT NULL,
    location VARCHAR(50) NOT NULL,
    clothing_color VARCHAR(20),
    carrying VARCHAR(50),
    confidence DECIMAL(4,2) NOT NULL,
    FOREIGN KEY (suspect_id) REFERENCES suspects(suspect_id),
    INDEX idx_camera_time (seen_time)
);

CREATE TABLE cafe_orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    suspect_id INT NOT NULL,
    ordered_at DATETIME NOT NULL,
    item_name VARCHAR(50) NOT NULL,
    amount INT NOT NULL,
    payment_last4 CHAR(4) NOT NULL,
    FOREIGN KEY (suspect_id) REFERENCES suspects(suspect_id)
);

CREATE TABLE messages (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    sent_at DATETIME NOT NULL,
    message_text VARCHAR(255) NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (sender_id) REFERENCES suspects(suspect_id),
    FOREIGN KEY (receiver_id) REFERENCES suspects(suspect_id),
    INDEX idx_message_time (sent_at)
);

CREATE TABLE evidence (
    evidence_id INT PRIMARY KEY AUTO_INCREMENT,
    found_at DATETIME NOT NULL,
    location VARCHAR(50) NOT NULL,
    evidence_type VARCHAR(50) NOT NULL,
    detail VARCHAR(255) NOT NULL
);

INSERT INTO suspects VALUES
(101, '瑪奇瑪', '公安對魔特異課主管', 24.0, '1842', FALSE, '表示整晚都在貴賓室接待來賓'),
(102, '淀治', '公安惡魔獵人',       27.5, '7319', TRUE,  '表示 21:00 後都在一樓巡邏'),
(103, '早川秋', '公安惡魔獵人',     26.5, '4061', FALSE, '表示在修復室檢查展示架'),
(104, '帕瓦', '血之魔人',           23.5, '9920', TRUE,  '表示 21:10 已離開博物館'),
(105, '波奇塔', '鏈鋸惡魔',         28.0, '5537', FALSE, '表示在地下室檢查配電箱'),
(106, '洛伊德·佛傑', '西國情報員',  24.5, '2684', FALSE, '表示在辦公室整理任務清單'),
(107, '約兒·佛傑', '市政府職員',    27.5, '1158', TRUE,  '表示整晚待在貴賓室'),
(108, '安妮雅·佛傑', '伊甸學園學生', 23.0, '6421', FALSE, '表示打烊後在咖啡廳等待家人'),
(109, '彭德·佛傑', '安妮雅的狗',    26.0, '8873', TRUE,  '表示在二樓跟著氣味散步'),
(110, '達米安·戴斯蒙德', '伊甸學園學生', 27.0, '3095', FALSE, '表示在資料室歸還文件');

INSERT INTO rooms VALUES
('R01', '一樓大廳', 1),
('R02', '貴賓室', 1),
('R03', '黃金吐司保管庫', 2),
('R04', '修復室', 2),
('R05', '行政辦公室', 2),
('R06', '地下配電室', -1),
('R07', '資料室', 3),
('R08', '員工咖啡廳', 1);

-- 案發日：2026-08-20；保全在 21:25 發現黃金吐司消失。
INSERT INTO access_logs (suspect_id, room_id, action, access_time, result) VALUES
(101, 'R02', 'IN',  '2026-08-20 20:42:10', 'SUCCESS'),
(107, 'R02', 'IN',  '2026-08-20 20:45:03', 'SUCCESS'),
(106, 'R05', 'IN',  '2026-08-20 20:51:44', 'SUCCESS'),
(103, 'R04', 'IN',  '2026-08-20 20:55:12', 'SUCCESS'),
(105, 'R06', 'IN',  '2026-08-20 20:58:39', 'SUCCESS'),
(108, 'R08', 'IN',  '2026-08-20 21:01:18', 'SUCCESS'),
(110, 'R07', 'IN',  '2026-08-20 21:04:22', 'SUCCESS'),
(104, 'R01', 'OUT', '2026-08-20 21:08:51', 'SUCCESS'),
(109, 'R04', 'IN',  '2026-08-20 21:09:14', 'DENIED'),
(101, 'R03', 'IN',  '2026-08-20 21:10:42', 'SUCCESS'),
(101, 'R03', 'OUT', '2026-08-20 21:11:25', 'SUCCESS'),
(102, 'R03', 'IN',  '2026-08-20 21:12:36', 'SUCCESS'),
(107, 'R03', 'IN',  '2026-08-20 21:13:02', 'DENIED'),
(110, 'R03', 'IN',  '2026-08-20 21:14:27', 'DENIED'),
(103, 'R03', 'IN',  '2026-08-20 21:15:08', 'SUCCESS'),
(103, 'R03', 'OUT', '2026-08-20 21:16:44', 'SUCCESS'),
(106, 'R03', 'IN',  '2026-08-20 21:17:12', 'SUCCESS'),
(106, 'R03', 'OUT', '2026-08-20 21:18:03', 'SUCCESS'),
(102, 'R03', 'OUT', '2026-08-20 21:19:48', 'SUCCESS'),
(109, 'R01', 'IN',  '2026-08-20 21:20:33', 'SUCCESS'),
(105, 'R06', 'OUT', '2026-08-20 21:22:07', 'SUCCESS'),
(103, 'R04', 'OUT', '2026-08-20 21:23:11', 'SUCCESS'),
(101, 'R02', 'OUT', '2026-08-20 21:27:04', 'SUCCESS'),
(107, 'R02', 'OUT', '2026-08-20 21:28:15', 'SUCCESS');

INSERT INTO camera_sightings
(camera_code, suspect_id, seen_time, location, clothing_color, carrying, confidence) VALUES
('CAM-A1', 104, '2026-08-20 21:08:40', '一樓出口', '藍色', '相機包', 0.98),
('CAM-B2', 102, '2026-08-20 21:10:58', '二樓東側走廊', '深藍色', '空手', 0.91),
('CAM-C3', NULL,'2026-08-20 21:18:52', '展品庫外走廊', '深藍色', '銀色保溫袋', 0.67),
('CAM-B2', 102, '2026-08-20 21:20:05', '二樓安全梯', '深藍色', '銀色保溫袋', 0.88),
('CAM-D4', 109, '2026-08-20 21:20:41', '一樓大廳', '藍色', '清潔推車', 0.96),
('CAM-E5', 105, '2026-08-20 21:22:15', '地下室入口', '灰色', '工具箱', 0.94),
('CAM-F6', 103, '2026-08-20 21:23:20', '修復室門口', '白色', '畫框', 0.95),
('CAM-A1', 102, '2026-08-20 21:31:16', '員工停車場', '深藍色', '銀色保溫袋', 0.86);

INSERT INTO cafe_orders
(suspect_id, ordered_at, item_name, amount, payment_last4) VALUES
(101, '2026-08-20 20:31:20', '熱拿鐵', 120, '1842'),
(107, '2026-08-20 20:34:05', '黑咖啡', 90, '1158'),
(102, '2026-08-20 20:47:12', '冰美式', 100, '7319'),
(102, '2026-08-20 20:47:12', '銀色保溫袋', 80, '7319'),
(106, '2026-08-20 20:49:44', '紅茶', 70, '2684'),
(103, '2026-08-20 20:52:11', '三明治', 110, '4061'),
(109, '2026-08-20 20:56:38', '瓶裝水', 40, '8873'),
(110, '2026-08-20 21:00:02', '熱可可', 100, '3095');

INSERT INTO messages
(sender_id, receiver_id, sent_at, message_text, is_deleted) VALUES
(106, 101, '2026-08-20 19:42:00', '展品清冊已放在辦公室桌上。', FALSE),
(107, 101, '2026-08-20 20:10:13', '今晚我想再看一次黃金吐司。', FALSE),
(102, 105, '2026-08-20 20:38:46', '21:10 左右做一次短暫斷電測試，照原計畫。', TRUE),
(105, 102, '2026-08-20 20:40:02', '不行，正式測試排在明天，今晚不要碰線路。', TRUE),
(104, 106, '2026-08-20 20:57:19', '參觀結束，我先離開了。', FALSE),
(102, 108, '2026-08-20 21:02:33', '剛才買的保溫袋先別告訴任何人。', TRUE),
(110, 103, '2026-08-20 21:06:04', '我在三樓資料室，有看到你要的舊目錄。', FALSE),
(102, 107, '2026-08-20 21:29:51', '今晚巡邏正常，沒有異常。', FALSE);

INSERT INTO evidence (found_at, location, evidence_type, detail) VALUES
('2026-08-20 21:26:10', '黃金吐司保管庫', '鞋印', '鞋底長度推估為 27.5 號'),
('2026-08-20 21:26:35', '黃金吐司保管庫', '纖維', '深藍色外套纖維'),
('2026-08-20 21:27:11', '黃金吐司保管庫', '系統紀錄', '21:11:50 至 21:20:10 監視器訊號中斷'),
('2026-08-20 21:34:28', '員工停車場', '包裝碎片', '銀色保溫袋內襯，帶有保管櫃玻璃粉末');

-- 給學生的第一張「案情卡」可從這個 View 讀取，不直接揭露嫌犯姓名。
CREATE VIEW case_brief AS
SELECT
    '消失的黃金吐司' AS case_name,
    '2026-08-20 21:10:00' AS estimated_start,
    '2026-08-20 21:25:00' AS discovered_at,
    'R03' AS crime_room,
    '找出同時符合門禁、鞋印、衣著、攜帶物與動機線索的人' AS mission;

