import csv
import os

# 設定輸入和輸出檔案的路徑
input_csv_path = os.path.join('csv', 'album_list_with_id.csv')
output_sql_path = os.path.join('SQL', 'insert_product.sql')

# 確保 SQL 資料夾存在
os.makedirs(os.path.dirname(output_sql_path), exist_ok=True)


# 讀取 CSV 檔案並生成 INSERT 語句
with open(input_csv_path, 'r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    with open(output_sql_path, 'w', encoding='utf-8-sig') as sql_file:
        for row in csv_reader:
            # 用變數來預處理欄位值，避免在 f-string 中使用複雜的運算
            product_id = row.get('ProductID', 'NULL')  # 預設值設為 'NULL' 適用於 SQL
            product_name = row.get('ProductName', '').replace("'", "''")  # 處理單引號以防止 SQL 注入
            description = row.get('ProductDescription', "").strip()
            image_url = row.get('ImageURL').replace("'", "''") 
            product_code = row.get('ProductCode', '').replace("'", "''")  # 處理單引號以防止 SQL 注入
            artist_id = row.get('ArtistID', '').replace("'", "''")    # 修正變數名從 product_type 改為 artist_name
            price = row.get('Price', 0)
            barcode = row.get('Barcode', 'NULL')  # 處理空條碼，設為 'NULL'
            manufacturer = row.get('Manufacturer', '').replace("'", "''")
            publisher = row.get('Publisher', '').replace("'", "''")
            release_date = row.get('ReleaseDate', '0000-00-00')  # 預設日期格式
            category_id = row.get('CategoryID', 'NULL')  # 預設值為 'NULL'
            stock_quantity = row.get('StockQuantity', 0)
            
            # 生成單行 INSERT 語句
            sql_line = f"""
            INSERT IGNORE INTO product 
                (ProductID, ProductCode, Barcode, ProductName, ProductDescription, ImageURL , Price, ProductCategory, Manufacturer, ArtistID, Publisher, ReleaseDate, StockQuantity) 
            VALUES ({product_id}, '{product_code}', '{barcode}', '{product_name}', '{description}',
                        '{image_url}', {price}, '{category_id}', {manufacturer}, {artist_id}, {publisher}, '{release_date}', {stock_quantity});"""

            # 去掉每行的縮排
            sql_line = ''.join([line.lstrip() for line in sql_line.splitlines(True)])
            # 在每個 INSERT 語句之後加上空行
            sql_line += '\n\n'

            # 寫入到 SQL 檔案中
            sql_file.write(sql_line)

print(f"SQL INSERT 語句已生成並寫入 '{output_sql_path}'")
