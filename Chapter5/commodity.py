from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
from sql_utils import WebScrapingDB


class ProductScrap:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized") # Chrome 瀏覽器在啟動時最大化視窗
        self.options.add_argument("--incognito") # 無痕模式
        self.options.add_argument("--disable-popup-blocking") # 停用 Chrome 的彈窗阻擋功能。

    def get_pchome_products(self, product_name):
        driver = webdriver.Chrome(options=self.options)
        driver.get(f"https://24h.pchome.com.tw/search/?q={product_name}")
        db = WebScrapingDB()

        all_products = []
        cnt = 1
        print(f"\033[33m[Start]\033[0m 開始抓取 PChome - {product_name}")
        while True:
            time.sleep(2)
            
            info_cards = driver.find_elements(By.CSS_SELECTOR, ".c-prodInfoV2--gridCard")
            
            if info_cards == []:
                print("找不到商品資訊，結束程式")
                break
            
            print(f"Page: {cnt} - {len(info_cards)} 個商品資訊")
            
            page_products = []
            for card in info_cards:
                img_url = card.find_element(By.CSS_SELECTOR, ".c-prodInfoV2__img img").get_attribute("src")
                link = card.find_element(By.CSS_SELECTOR, ".c-prodInfoV2__link").get_attribute("href")
                title = card.find_element(By.CSS_SELECTOR, ".c-prodInfoV2__title").text
                price = card.find_element(By.CSS_SELECTOR, ".c-prodInfoV2__priceValue").text

                # 如果有載入中的圖片，就重新抓取
                if img_url.endswith("mobile_loading.svg"):
                    continue

                db.insert_product_info(product_name, title, price, img_url, link, "PChome")
                page_products.append({
                    "img_url": img_url,
                    "link": link,
                    "title": title,
                    "price": price,
                    "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            all_products.extend(page_products)
            # 判斷是否已經是最後一頁
            disabled_btn = driver.find_elements(By.CSS_SELECTOR, ".c-pagination__button.is-next button[disabled]")
            if disabled_btn != []:
                print("[\033[33mEnd\033[0m] PChome 已經是最後一頁，無法點擊下一頁按鈕")
                break

            next_page_btn = driver.find_element(By.CSS_SELECTOR, ".c-pagination__button.is-next button")
            next_page_btn.click()
            cnt += 1
        
        driver.quit()

        return all_products
    

    def get_momo_products(self, product_name):
        driver = webdriver.Chrome(options=self.options)
        driver.get(f"https://www.momoshop.com.tw/search/{product_name}?_isFuzzy=0&searchType=1")

        all_products = []
        db = WebScrapingDB()

        while True:
            time.sleep(2)
            info_cards = driver.find_elements(By.CSS_SELECTOR, "li.listAreaLi")
            if info_cards == []:
                print("找不到商品資訊，結束程式")
                break

            print(f"找到 {len(info_cards)} 個商品資訊")

            page_products = []
            for card in info_cards:
                img_url = card.find_element(By.CSS_SELECTOR, "img.goods-img").get_attribute("src")
                link = card.find_element(By.CSS_SELECTOR, "div.goods-img-url > a").get_attribute("href")
                title = card.find_element(By.CSS_SELECTOR, "h3.prdName").text
                price = card.find_element(By.CSS_SELECTOR, "span.price > b").text

                db.insert_product_info(product_name, title, price, img_url, link, "Momo")
                page_products.append({
                    "img_url": img_url,
                    "link": link,
                    "title": title,
                    "price": price,
                    "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            all_products.extend(page_products)

            next_page_btn = driver.find_elements(By.CSS_SELECTOR, ".page-btn.page-next")
            if next_page_btn == []:
                print("已經是最後一頁，無法點擊下一頁按鈕")
                break
            else:
                next_page_btn[1].click()

        driver.quit()

        return all_products