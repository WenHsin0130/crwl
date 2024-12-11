import random
import os
import requests

from urllib.parse import urljoin
from datetime import datetime
from utils import is_data_fetched
from utils import fetch_html
from utils import export_to_csv_album
from utils import download_image
from utils import get_categoryID_from_csv
from utils import get_productID_from_csv


# 初始化商品列表
product_list = []


def get_product_sessions(category, page):
    """
    爬取指定網頁並返回所有專輯的 Session
    
    Args:
        url (str): 網頁的 URL。

    Returns:
        product_session_list: 包含所有專輯 Session 的列表。
    """
    # 取得本頁面所有元件
    all_elements = fetch_html(f"https://www.5music.com.tw/cdmus-c.asp?mut={category}&nowPage={page}")

    # 獲取所有 專輯 session
    product_session = all_elements.find_all("div", class_="record-box")

    # 初始化所有專輯詳細資訊的連結清單
    product_session_list = []

    # 從每個 record-box 中提取 <a> 標籤的 href 屬性
    for box in product_session:
        # a_element: <a> 標籤連結詳細資訊的 Session (Session 範例：CDList-C.asp?cdno=445485678569)
        a_element = box.find("a")

        if a_element and 'href' in a_element.attrs:
            # 將連結加入 product_session_list
            product_session_list.append(a_element['href'])
            # print(a_element['href'])

    return product_session_list

def main(url):

    # 根據不同專輯類別取得唱片資訊
    cdno_ids = get_productID_from_csv()

    # 根據不同專輯類別取得唱片資訊
    for cdno in cdno_ids:
        # 網址商品的 session 設定
        query = f"CDList-C.asp?cdno={cdno}"

        print(f"---------------- product: {cdno} ----------------")

        # 使用自訂函式 fetch_html 取得該專輯頁面所有元件
        product_url = urljoin(url, query)

        # 處理 product_all_elements 的後續操作
        print(f"Processing product {cdno} : {product_url}")

        # 使用自訂函式 fetch_html 取得該專輯頁面所有元件
        product_all_elements = fetch_html(product_url)

        # 取得 商品圖片 <img class="img-responsive lazy">
        img = product_all_elements.find("img", class_="img-responsive lazy")
        
        # 檢查是否找到圖片
        if img and 'data-src' in img.attrs:
            image_src = img['data-src']

            # 圖片 url 範例：https://www.5music.com.tw/cdpic/zn2/35202411134881.jpg
            base_url = "https://www.5music.com.tw/"
            image_url = urljoin(base_url, image_src)
            # print("圖片 URL:", image_url)

            # 下載圖片
            try:
                # requests.get() img_url 發送一個 GET 請求，該請求會取得網頁或資源的內容
                response = requests.get(image_url, stream=True)
                response.raise_for_status()  # 檢查請求是否成功

                # 保存圖片的路徑
                image_save_dir = "image/img"
                image_name = f"{cdno}.jpg"

                # 自動建立資料夾
                os.makedirs(image_save_dir, exist_ok=True)

                # 生成完整儲存路徑
                save_path = os.path.join(image_save_dir, image_name)

                # 保存圖片到指定路徑
                with open(save_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)

            except requests.RequestException as e:
                print(f"下載圖片失敗: {e}")
        else:
            print("未找到圖片")

if __name__ == "__main__":
    main("https://www.5music.com.tw/")

