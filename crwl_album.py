import random
import re
import requests

from urllib.parse import urljoin
from datetime import datetime
from utils import is_data_fetched
from utils import fetch_html
from utils import export_to_csv_album
from utils import download_image


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

    # 獲取所有 藝人名稱
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


def get_product_details(product_session, product_all_elements, category):
    # 從 session 取得商品的 ID，使用正則表達式尋找 cdno 後的數字 (session 範例: CDList-C.asp?cdno=445485678796)
    parts = product_session.split('cdno=')
    cdno = parts[1].split()[0]

    # 提取 頁面的專輯名稱與藝人區塊 <h2 class="h2">  
    product_title = product_all_elements.find("h2", class_="h2")
    product_span = product_title.find_all("span")

    # 取得 商品圖片 <img class="img-responsive lazy">
    product_img = product_all_elements.find("img", class_="img-responsive lazy")
    # download_image(product_img)

    # 取得 商品條碼、商品編號、製作公司、發行公司、發行日期 區塊 <ul>
    product_ul = product_all_elements.find("ul", class_="reset specific")
    product_li_content = product_ul.find_all("div", class_="content")

    # 取得時間並轉換格是為 YY-mm-dd
    date_text = product_li_content[5].text.strip()
    formatted_date = datetime.strptime(date_text, "%Y/%m/%d").strftime("%Y-%m-%d")

    # 取得 barcode 並轉換格式為 int
    barcode_text = product_li_content[0].text.strip()
    if barcode_text:
        formatted_barcode = int(barcode_text)
    else:
        formatted_barcode = None

    # 取得 商品價錢區域
    product_price_sale = product_all_elements.find("div", class_="price sale")
    price_span = product_price_sale.find("span", class_="new").text.strip().replace("$", "")

    # 取得 商品說明 (使用 \n 保留換行)
    product_description = product_all_elements.find("div", class_="product-content-theme").text.replace("<br/>", "\n")


    # 儲存專輯詳細資訊到 product 列表
    product = []

    product.append({
        "ProductID": cdno,
        # 專輯名稱 (使用 strip() 刪除頭尾不必要的 html，使用 relace 刪除 <br> tag)
        "ProductName": product_span[1].text.strip().replace("<br>", ""),
        # 專輯藝人
        "ArtistName": product_span[0].text.strip(),
        # 專題圖片
        "ImageURL": f"image/{cdno}.jpg",
        # "ImageURL": product_img,
        # 商品編號
        "ProductCode": product_li_content[1].text.strip(),
        # 商品條碼
        "Barcode": formatted_barcode,
        # 製作廠商
        "Manufacturer" : product_li_content[3].text.strip(),
        # 發行商
        "Publisher" : product_li_content[4].text.strip(),
        # 發行日期
        "ReleaseDate" : formatted_date,
        # 商品價錢
        "Price": price_span,
        # 商品說明
        "ProductDescription": product_description,
        # 隨機產生庫存量
        "StockQuantity": random.randint(0, 2000),
        # 爬取的類別
        "CategoryID" : category
    })

    return product

def fetch_product_list(url, file_name):
    """
    爬取指定語言分類下的專輯資料並匯出至 CSV 檔案
    
    Args:
        url (str): 基本網站的 URL，用於生成專輯頁面完整連結
        file_name (str): 匯出 CSV 檔案的名稱

    """

    # 語言類別
    category = "A"

    # 頁面
    page = 1

    # 將 session 結合五大唱片主連結 (url)，轉換成有意義的 url
    product_session_list = get_product_sessions(category, page)

    # 初始化商品列表
    product_list = []

    for idx, product_session in enumerate(product_session_list):
        product_url = urljoin(url, product_session)

        # 使用自訂函式 fetch_html 取得該專輯頁面所有元件
        product_all_elements = fetch_html(product_url)

        # 處理 product_all_elements 的後續操作
        print(f"Processing product at index {idx}: {product_url}")

        # 將 "CategoryID": category 添加到 product_details 字典中
        product_details = get_product_details(product_session, product_all_elements, category)

        # 將 product 資料加入列表
        product_list.extend(product_details)
    
    # 使用爬取的資料匯出 product 的 csv 檔案
    export_to_csv_album(product_list, file_name)

