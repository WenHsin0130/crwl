from utils import is_data_fetched
from utils import fetch_html
from utils import export_to_csv_artist
from urllib.parse import urljoin

# 定義 session_list 並加入分類標記
session_list = [
    # 華語男藝人
    {"url": "sclasca.asp?mut=A&s2=1&h=1", "category": "A", "type": "男藝人"},
    {"url": "sclasca.asp?mut=A&s2=1&h=1&gh=1", "category": "A", "type": "男藝人"},
    {"url": "sclasca.asp?mut=A&s2=1&h=1&gh=11", "category": "A", "type": "男藝人"},
    {"url": "sclasca.asp?mut=A&s2=1&h=1&gh=12", "category": "A", "type": "男藝人"},
    {"url": "sclasca.asp?mut=A&s2=1&h=1&gh=13", "category": "A", "type": "男藝人"},

    # 華語女藝人
    {"url": "sclasca.asp?mut=A&s2=2&h=3", "category": "A", "type": "女藝人"},
    {"url": "sclasca.asp?mut=A&s2=2&h=3&gh=1", "category": "A", "type": "女藝人"},
    {"url": "sclasca.asp?mut=A&s2=2&h=3&gh=11", "category": "A", "type": "女藝人"},
    {"url": "sclasca.asp?mut=A&s2=2&h=3&gh=12", "category": "A", "type": "女藝人"},
    {"url": "sclasca.asp?mut=A&s2=2&h=3&gh=13", "category": "A", "type": "女藝人"},

    # 華語樂團
    {"url": "sclasca.asp?mut=A&s2=3&h=2", "category": "A", "type": "樂團團體"},
    {"url": "sclasca.asp?mut=A&s2=3&h=2&gh=1", "category": "A", "type": "樂團團體"},
    {"url": "sclasca.asp?mut=A&s2=3&h=2&gh=11", "category": "A", "type": "樂團團體"},
    {"url": "sclasca.asp?mut=A&s2=3&h=2&gh=12", "category": "A", "type": "樂團團體"},
    {"url": "sclasca.asp?mut=A&s2=3&h=2&gh=13", "category": "A", "type": "樂團團體"},

    # 華語相聲表演團體
    {"url": "sclasca.asp?mut=A&s2=4&h=4", "category": "A", "type": "相聲表演團體"},
    {"url": "sclasca.asp?mut=A&s2=4&h=4&gh=1", "category": "A", "type": "相聲表演團體"},
    {"url": "sclasca.asp?mut=A&s2=4&h=4&gh=11", "category": "A", "type": "相聲表演團體"},
    
    # 韓語男藝人
    {"url": "listartam.asp?mut=M&art=A&stp=1&h=1", "category": "M", "type": "男藝人"},
    {"url": "listartam.asp?mut=M&art=A&stp=1&h=3", "category": "M", "type": "女藝人"},
    {"url": "listartam.asp?mut=M&art=A&stp=1&h=2", "category": "M", "type": "樂團團體"},

    # 台語男藝人
    {"url": "sclasca.asp?mut=C&s2=1&h=1", "category": "C", "type": "男藝人"},
    {"url": "sclasca.asp?mut=C&s2=1&h=1&gh=1", "category": "C", "type": "男藝人"},
    {"url": "sclasca.asp?mut=C&s2=1&h=1&gh=11", "category": "C", "type": "男藝人"},

    # 台語女藝人
    {"url": "sclasca.asp?mut=C&s2=2&h=3", "category": "C", "type": "男藝人"},
    {"url": "sclasca.asp?mut=C&s2=2&h=3&gh=1", "category": "C", "type": "男藝人"},
    {"url": "sclasca.asp?mut=C&s2=2&h=3&gh=11", "category": "C", "type": "男藝人"},

    # 台語團體
    {"url": "sclasca.asp?mut=C&s2=3&h=2", "category": "C", "type": "樂團團體"},
    {"url": "sclasca.asp?mut=C&s2=3&h=2&gh=1", "category": "C", "type": "樂團團體"},    
    {"url": "sclasca.asp?mut=C&s2=3&h=2&gh=11", "category": "C", "type": "樂團團體"},    
    {"url": "sclasca.asp?mut=C&s2=3&h=2&gh=12", "category": "C", "type": "樂團團體"},

    # 西洋
    {"url": "listartame.asp?mut=B&art=A&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=B&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=C&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=B&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=E&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=F&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=G&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=H&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=I&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=J&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=B&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=L&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=M&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=N&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=O&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=P&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=Q&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=R&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=S&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=T&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=U&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=V&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=W&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=X&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=Y&stp=1", "category": "B", "type": ""},
    {"url": "listartame.asp?mut=B&art=Z&stp=1", "category": "B", "type": ""},

    
    # 日語
    {"url": "sclas_A6.asp?mut=F&s2=1", "category": "F", "type": "男藝人"},
    {"url": "sclas_A7.asp?mut=F&s2=2", "category": "F", "type": "女藝人"},
    {"url": "sclas_A8.asp?mut=F&s2=3", "category": "F", "type": "樂團團體"},
]

# 初始化空的 language_list 列表，用於儲存爬蟲下來的值
artist_list = []

def get_artist(artist_all_elements, file_name, artist_type, category):
    """
    爬取網頁中的藝人。

    Args:
        url (str): 五大的主要 URL

    Returns:
    """
    if category=="F":
        list_elements = artist_all_elements.find("div", class_="list")
        td_elements = list_elements.find_all("input", type="button") # 藝人名稱

        
        for s in td_elements:
            # 提取 span_elements 提取純文本並去掉前後的空白字符
            artist = s.get("value", "").strip()

            if artist:  # 確保不是空字符串
                artist_list.append({
                    "ArtistName": artist,
                    "ArtistType": artist_type,
                    "ArtistCategory": category
                })
                # print(language)

    else:
        # 找到特定的 <ul> 標籤，然後選取其中的 <span class="ch">
        list_elements = artist_all_elements.find("div", class_="list")
        td_elements = list_elements.find_all("a", class_="box") # 藝人名稱

        for s in td_elements:
            # 提取 span_elements 提取純文本並去掉前後的空白字符
            artist = s.text.strip()

            if artist:  # 確保不是空字符串
                artist_list.append({
                    "ArtistName": artist,
                    "ArtistType": artist_type,
                    "ArtistCategory": category
                })
                # print(language)

    # print(artist_list)

    # 檢查是否有資料
    if is_data_fetched(artist_list):
        # 當資料數 > 1 筆回傳整個資料內容
        export_to_csv_artist(artist_list, file_name)
    else:
        # 否則回傳 None
        return None
    
def fetch_artist_list(url, file_name):
    # mut="分類" 下的 藝人列表
    for session in session_list:
        artist_list_session = session['url']
        artist_type = session['type']
        category = session['category']

        # 進入處理階段
        print(f"session:{artist_list_session} | astist_type:{artist_type} | category:{category}")

        # 取得本頁面所有元件
        artist_list_url = urljoin(url, artist_list_session)

        # 使用自訂函式 fetch_html 取得該專輯頁面所有元件
        artist_all_elements = fetch_html(artist_list_url)

        # 取得所有藝人並代入 list
        get_artist(artist_all_elements, file_name, artist_type, category)