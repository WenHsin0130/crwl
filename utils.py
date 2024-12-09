import os
import csv
import string
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_html(url, timeout=60):
    """
    發送 GET 請求並返回網頁的 BeautifulSoup 物件。

    Args:
        url (str): 網頁的 URL
        timeout (int, optional): 請求的超時時間，默認為 60 秒

    Returns:
        soup: 包含 HTML 結構的 BeautifulSoup 物件
        None: 如果請求失敗，返回 None
    """
    try:
        response = requests.get(url, timeout=timeout) # 取得回應
        response.raise_for_status()  # 檢查 HTTP 回應碼是否為 200
        response.encoding = "utf-8"  # 設置正確的編碼(避免中文亂碼)

        # 將內容轉換成 html.parser
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    
    except requests.exceptions.RequestException as e:
        print(f"HTTP 請求失敗: {e}")
        return None


def is_data_fetched(data):
    """
    檢查是否成功取得資料。

    Param: 
        data 要檢查的資料（例如列表或字典）
    Return: 
        如果資料存在且不為空，返回 True，否則返回 False
    """
    if len(data) > 0:
        print("資料取得成功", end=" ")
        return True
    else:
        print("未取得任何資料")
        return False


def download_image(img):
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
            image_save_dir="image"
            image_name = os.path.basename(image_url)

            save_path = os.path.join(image_save_dir, image_name)

            # 保存圖片到指定路徑
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

        except requests.RequestException as e:
            print(f"下載圖片失敗: {e}")
    else:
        print("未找到圖片")


def get_categoryID_from_csv():
    # Specify the input CSV path
    input_csv_path = 'csv/category_list_for_album.csv'

    # Read CSV and get all CategoryID values
    category_ids = []

    with open(input_csv_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            category_id = row['CategoryID']
            category_ids.append(category_id)

    # Print all CategoryID values
    print("Successfully Get CategoryID values")

    return category_ids


def export_to_csv(data_list, file_name):
    """
    匯出 專輯類別 CSV 檔案。
    """

    # 設定被爬蟲網站 (url) 與匯出 csv 檔案的資料夾的位置 (folder_path)
    output_path = os.path.join(os.getcwd(), "csv", file_name)

    # 確保資料夾存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 匯出 CSV 檔案
    with open(output_path, mode="w", newline="", encoding="utf-8-sig") as file:
        # 寫入標題列
        writer = csv.writer(file)
        writer.writerow(["CategoryID", "Category"])

        # 使用字母索引
        for index, name in zip(string.ascii_uppercase, data_list):
            writer.writerow([index, name])

    print(f"'{file_name}' 檔案已成功匯出到 '{output_path}'")

def export_to_csv_album(data_list, file_name):
    """
    匯出 CSV 檔案。
    """

    # print(data_list)

    # 設定被爬蟲網站 (url) 與匯出 csv 檔案的資料夾的位置 (folder_path)
    output_path = os.path.join(os.getcwd(), "csv", file_name)

    # 確保資料夾存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode="w", newline="", encoding="utf-8-sig") as file:
        # 寫入標題列
        writer = csv.writer(file)
        writer.writerow([
            "ProductID", 
            "ProductName", 
            "ProductDescription",
            "ImageURL",
            "ArtistID", 
            "ProductCode",
            "Barcode", 
            "Manufacturer", 
            "Publisher", 
            "ReleaseDate",
            "CategoryID",
            "StockQuantity",
            "Price"
        ])
        
        # 寫入資料列
        for item in (data_list):
            writer.writerow([
                item.get("ProductID", ""),
                item.get("ProductName", ""),
                item.get("ProductDescription", ""),
                item.get("ImageURL"),
                item.get("ArtistName", ""),
                item.get("ProductCode", ""),
                item.get("Barcode", ""),
                item.get("Manufacturer", ""),
                item.get("Publisher", ""),
                item.get("ReleaseDate", ""),
                item.get("CategoryID", ""),
                item.get("StockQuantity", ""),
                item.get("Price")
            ])


    print(f"'{file_name}' 檔案已成功匯出到 '{output_path}'")


def export_to_csv_artist(data_list, file_name):
    """
    匯出 藝人 CSV 檔案。
    """

    # 設定被爬蟲網站 (url) 與匯出 csv 檔案的資料夾的位置 (folder_path)
    output_path = os.path.join(os.getcwd(), "csv", file_name)


    # 確保資料夾存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 匯出 CSV 檔案
    with open(output_path, mode="w", newline="", encoding="utf-8-sig") as file:
        # 寫入標題列
        writer = csv.writer(file)
        writer.writerow([
            "ArtistID",
            "ArtistName",
            "ArtistType",
            "ArtistCategory"
        ])

        # 寫入資料列
        for index, item in enumerate(data_list, start=1): 
            writer.writerow([
                index,
                item.get("ArtistName", ""),
                item.get("ArtistType", ""),
                item.get("ArtistCategory", "")
            ])

    print(f"'{file_name}' 檔案已成功匯出到 '{output_path}'")