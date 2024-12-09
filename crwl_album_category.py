from utils import is_data_fetched
from utils import fetch_html
from utils import export_to_csv

def fetch_language_list(url, file_name):
    """
    爬取網頁中的語言名稱。

    Args:
        url (str): 網頁的 URL

    Returns:
        language_list: 爬蟲後的語言資料內容
        None: 如果請求失敗，返回 None
    """
    # 取得本頁面所有元件
    all_elements = fetch_html(url)

    # 找到特定的 <ul> 標籤，然後選取其中的 <span class="ch">
    ul_elements = all_elements.find("ul", class_="reset cat-list")
    span_elements = ul_elements.find_all("span", class_="ch")

    # 初始化空的 language_list 列表，用於儲存爬蟲下來的值
    language_list = []

    for s in span_elements:
        # 提取 span_elements 提取純文本並去掉前後的空白字符
        language = s.text.strip()

        if language:  # 確保不是空字符串
            language_list.append(language)
            # print(language)

    # 檢查是否有資料
    if is_data_fetched(language_list):
        # 當資料數 > 1 筆回傳整個資料內容
        export_to_csv(language_list, file_name)
    else:
        # 否則回傳 None
        return None