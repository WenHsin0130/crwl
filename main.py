# import 其他 python 檔案
from crwl_album_category import fetch_language_list
from crwl_album import fetch_product_list


# 主程式
if __name__ == "__main__":
    """ 從 crwl.py 爬取語言資料並匯出 csv """
    base_url = "https://www.5music.com.tw/"

    # 取得語言類別資料
    # fetch_language_list(base_url, "language_list.csv", 1)

    # 取得所有產品(專輯唱片)資料，使用數字編號
    fetch_product_list(base_url, "album_list.csv")
