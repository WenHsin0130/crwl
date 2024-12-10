import random

from urllib.parse import urljoin
from datetime import datetime
from utils import is_data_fetched
from utils import fetch_html
from utils import export_to_csv_album
from utils import download_image
from utils import get_productID_from_csv

# 初始化光碟列表
disc_list = []

def get_disc_details(product_url, cdno):

    all_elements = fetch_html(product_url)

    # 提取 頁面的專輯名稱與藝人區塊 <h2 class="h2">  
    all_discs = all_elements.find("div", class_="products-view-table-theme")

    print(all_discs)

    # cdno = 445485678796
    # disc_type = "CD"
    # serial_num = 1
    # song = "初心Love"

    # disc_list.append({
    #     # 專輯 ID (從 csv 獲取)
    #     "ProductID": cdno,
    #     # 專輯類別 BD/CD/DVD...
    #     "DiscType": disc_type,
    #     # 第幾張光碟 Ex: BD"1", CD"2"
    #     "SerialNumber": serial_num,
    #     # 曲目內容
    #     "Songs": song
    # })

    # return disc_list


def fetch_product_list(url, file_name):
    """
    爬取指定語言分類下的專輯資料並匯出至 CSV 檔案
    
    Args:
        url (str): 基本網站的 URL，用於生成專輯頁面完整連結
        file_name (str): 匯出 CSV 檔案的名稱

    """

    # 取得所有專輯類別
    cdno_ids = get_productID_from_csv()


    # 根據不同專輯類別取得唱片資訊
    # for cdno in cdno_ids:
    cdno = 445485678796
    print(f"---------------- product: {cdno} ----------------")

    # 使用自訂函式 fetch_html 取得該專輯頁面所有元件
    product_url = urljoin(url, "CDList-C.asp?cdno=", cdno)

    # 處理 product_all_elements 的後續操作
    print(f"Processing product {cdno} : {product_url}")

    # 使用 "productID" 取得該商品/專輯下所有資訊
    get_disc_details(product_url, cdno)

    # 使用爬取的資料匯出 product 的 csv 檔案
    # export_to_csv_album(disc_details, file_name)




fetch_product_list("https://www.5music.com.tw/", "disc.csv")

