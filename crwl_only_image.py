import random

from urllib.parse import urljoin
from datetime import datetime
from utils import is_data_fetched
from utils import fetch_html
from utils import export_to_csv_album
from utils import download_image
from utils import get_categoryID_from_csv

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

    # 取得所有專輯類別
    category_ids = get_categoryID_from_csv()

    # 根據不同專輯類別取得唱片資訊
    for category in category_ids:
        # 該類別下共 5 頁的資料
        for page in range(1, 6):
            print(f"---------------- Category: {category} | Page {page} ----------------")

            # 將 session 結合五大唱片主連結 (url)，轉換成有意義的 url
            product_session_list = get_product_sessions(category, page)

            # 取得指定專輯的連結，並且進入指定連結爬取內容
            for idx, product_session in enumerate(product_session_list):
                product_url = urljoin(url, product_session)

                # 使用自訂函式 fetch_html 取得該專輯頁面所有元件
                product_all_elements = fetch_html(product_url)

                # 處理 product_all_elements 的後續操作
                print(f"Processing category {category} at index {idx}: {product_url}")

                # 取得 商品圖片 <img class="img-responsive lazy">
                product_img = product_all_elements.find("img", class_="img-responsive lazy")
                download_image(product_img)

if __name__ == "__main__":
    main("https://www.5music.com.tw/")

