import random
import re

from urllib.parse import urljoin
from datetime import datetime
from utils import is_data_fetched
from utils import fetch_html
from utils import export_to_csv_disk
from utils import get_productID_from_csv

# 初始化光碟列表
disk_list = []

def get_disk_details(product_url, cdno):

    all_elements = fetch_html(product_url)

    # 提取 頁面的專輯名稱與藝人區塊 <h2 class="h2">  
    all_disks = all_elements.find("div", class_="products-view-table-theme")

    # 光碟編號與張數 [Disc 1 CD, Disc 2 CD, Disc1 BD ...]
    table_titles = all_disks.find_all("div", class_="table-ti")

    # 找到所有曲目表，[table1 html ..., table2 html ...]
    tables = all_disks.find_all("table", class_="table-striped")

    # 根據 table_titles 判斷有幾張光碟，並且使用迴圈抓取該光碟下所有曲目
    for idx, title in enumerate(table_titles):

        # 將光碟編號與類別分開 範例 ['DISK', '2', 'CD']
        title = title.text.strip().split()

        # 確保 title 符合範例，如果不符合則使用法 2 取得 disk_type 與 serial_number
        if len(title) < 3:
            # 取得 商品條碼、商品編號、製作公司、發行公司、發行日期 區塊 <ul>
            product_ul = all_elements.find("ul", class_="reset specific")
            product_li_content = product_ul.find_all("div", class_="content")

            # 取得 第3項包含光碟類別的 li
            disk_type = product_li_content[2].text.strip()
            disk_type = re.findall(r'[A-Z]+', disk_type)
            # print(disk_type)
            serial_number = 1

        else: 
            disk_type = title[2]
            serial_number = title[1]

        # 取得目前 table 下的所有曲目
        rows = tables[idx].find_all("tr")[1:] 

        # 設定 song 字串為空
        songs = ""

        for row in rows:
            cells = row.find_all("td")
            song_number = cells[0].get_text(strip=True)

            # 取得每列歌曲
            song_name = cells[1].get_text(strip=True)
            format_song_name = song_number + song_name.replace('\xa0', ' ') + "\n"
            songs += format_song_name

        disk_list.append({
            # 專輯 ID (從 csv 獲取)
            "ProductID": cdno,
            # 專輯類別 BD/CD/DVD...
            "DiskType": disk_type[0],
            # 第幾張光碟 Ex: BD"1", CD"2"
            "SerialNumber": serial_number,
            # 曲目內容
            "Songs": songs
        })

    return disk_list


def fetch_disk_list(url, file_name):
    """
    爬取指定語言分類下的專輯資料並匯出至 CSV 檔案
    
    Args:
        url (str): 基本網站的 URL，用於生成專輯頁面完整連結
        file_name (str): 匯出 CSV 檔案的名稱

    """

    # 取得所有專輯類別
    cdno_ids = get_productID_from_csv()


    # 根據不同專輯類別取得唱片資訊
    for cdno in cdno_ids[:20]:
        cdno = 425425698242
        # 網址商品的 session 設定
        query = f"CDList-C.asp?cdno={cdno}"

        print(f"---------------- product: {cdno} ----------------")

        # 使用自訂函式 fetch_html 取得該專輯頁面所有元件
        product_url = urljoin(url, query)

        # 處理 product_all_elements 的後續操作
        print(f"Processing product {cdno} : {product_url}")

        # 使用 "productID" 取得該商品/專輯下所有資訊
        disk_details = get_disk_details(product_url, cdno)

        # print(disk_details)

    # 使用爬取的資料匯出 product 的 csv 檔案
    export_to_csv_disk(disk_details, file_name)



