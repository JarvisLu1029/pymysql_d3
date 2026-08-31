# 教師指南與解答（請勿先提供給學生）

## 教學目標

| 關卡 | SQL 技能 | 預期推理 |
|---|---|---|
| 1 | `SELECT` | 認識 schema 與案情 |
| 2 | `WHERE`、`BETWEEN`、`ORDER BY` | 先重建整晚 R03 訪客，再縮小案發時間 |
| 3 | `AND`、布林與數值條件 | 以物證形成嫌疑人交集 |
| 4 | `INNER JOIN` | 把人、門禁、監視器、訂單串起來 |
| 5 | `LIKE`、自我 JOIN | 還原數位訊息與動機 |
| 最終 | 多表 JOIN、`DISTINCT` | 形成唯一且可重現的證據鏈 |

## 真相

唯一符合所有條件者是 **淀治（suspect_id = 102）**。

關鍵證據：

- 2026 年 8 月 20 日晚上 18:00 至 22:00，早川秋、洛伊德、帕瓦、波奇塔、彭德與淀治都曾成功進入 R03。早川秋與洛伊德在 20:40 前已離開；縮到案發區間 21:10 至 21:25 後，優先調查對象才剩帕瓦、波奇塔、彭德與淀治。帕瓦在金庫前玩按鈕尤其可疑，但不是最終犯人。
- 四組足跡依資料庫分別為波奇塔 12.0、帕瓦 23.5、淀治與彭德 27.5；四者又分別具有橘色本體、布質腕帶、深橘帽 T 與南瓜圍巾，都可能留下現場的橘色痕跡，因此第三關仍不能定案。
- 監視器拍到一名不露臉、穿深橘色連帽衣者攜帶銀色保溫袋離開；後續步態辨識指向淀治。
- 淀治曾購買銀色保溫袋，並傳訊要求安妮雅保密。
- 淀治企圖請波奇塔斷電，好讓他進入保管庫拿食物；波奇塔明確拒絕。
- 尋回的吐司有明顯咬痕，尺寸排除波奇塔與彭德；咬痕是輔助線索，定案仍以多表數位證據鏈為主。

注意：資料能證明他是唯一符合所有數位線索的人；訊息中的「可能」推論不應被說成資料庫已直接證明的事實。

## 參考 SQL

```sql
-- 第二關
SELECT *
FROM access_logs
WHERE result = 'SUCCESS'
  AND action = 'IN'
  AND room_id = 'R03'
  AND access_time BETWEEN '2026-08-20 18:00:00' AND '2026-08-20 22:00:00'
ORDER BY access_time;

-- 第二關延伸：縮小到真正的案發區間，結果只剩四人
SELECT suspect_id, access_time
FROM access_logs
WHERE result = 'SUCCESS'
  AND action = 'IN'
  AND room_id = 'R03'
  AND access_time BETWEEN '2026-08-20 21:10:00' AND '2026-08-20 21:25:00'
ORDER BY access_time;

-- 第四關：展品庫成功門禁
SELECT s.name, s.job_title, a.access_time, a.action
FROM access_logs AS a
JOIN suspects AS s ON s.suspect_id = a.suspect_id
WHERE a.room_id = 'R03' AND a.result = 'SUCCESS'
ORDER BY a.access_time;

-- 第五關：可疑訊息與雙方姓名
SELECT sender.name AS sender_name,
       receiver.name AS receiver_name,
       m.sent_at,
       m.message_text,
       m.is_deleted
FROM messages AS m
JOIN suspects AS sender ON sender.suspect_id = m.sender_id
JOIN suspects AS receiver ON receiver.suspect_id = m.receiver_id
WHERE m.message_text LIKE '%斷電%'
   OR m.message_text LIKE '%保溫袋%'
   OR m.message_text LIKE '%巡邏%'
ORDER BY m.sent_at;

-- 最終關：五項條件同時成立
SELECT DISTINCT s.suspect_id, s.name, s.job_title
FROM suspects AS s
JOIN access_logs AS a ON a.suspect_id = s.suspect_id
JOIN camera_sightings AS c ON c.suspect_id = s.suspect_id
JOIN cafe_orders AS o ON o.suspect_id = s.suspect_id
WHERE s.shoe_size = 27.5
  AND s.has_orange_trace = TRUE
  AND a.room_id = 'R03'
  AND a.action = 'IN'
  AND a.result = 'SUCCESS'
  AND a.access_time BETWEEN '2026-08-20 21:10:00' AND '2026-08-20 21:25:00'
  AND c.seen_time BETWEEN '2026-08-20 21:10:00' AND '2026-08-20 21:35:00'
  AND c.carrying = '銀色保溫袋'
  AND o.item_name = '銀色保溫袋';
```

## 建議課程節奏（90 分鐘）

- 0–10 分鐘：公布案情、介紹資料表。
- 10–30 分鐘：第一、二關，確認 PyMySQL 連線與結果讀取。
- 30–50 分鐘：第三、四關，兩人一組比對線索。
- 50–70 分鐘：第五關與最終 SQL。
- 70–85 分鐘：各組提交嫌犯、SQL 與證據鏈。
- 85–90 分鐘：揭曉並討論 SQL Injection 與參數化查詢。

## 評分建議（100 分）

- 查詢正確性：40 分。
- 使用參數化查詢：15 分。
- 證據鏈完整性：25 分。
- 結案報告表達：10 分。
- 加分挑戰或查詢可讀性：10 分。

