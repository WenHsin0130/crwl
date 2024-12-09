import csv
import os

# 設定輸入和輸出檔案的路徑
input_csv_path = os.path.join('csv', 'product.csv')
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
            artist_name = row.get('ArtistName', '').replace("'", "''")    # 修正變數名從 product_type 改為 artist_name
            barcode = row.get('Barcode', 'NULL')  # 處理空條碼，設為 'NULL'
            manufacturer = row.get('Manufacturer', '').replace("'", "''")
            publisher = row.get('Publisher', '').replace("'", "''")
            release_date = row.get('ReleaseDate', '0000-00-00')  # 預設日期格式
            category_id = row.get('CategoryID', 'NULL')  # 預設值為 'NULL'
            
            # 生成單行 INSERT 語句
            sql_line = f"INSERT INTO product (productID, productName, productType, productCategory) VALUES ({product_id}, '{product_name}', '{product_type}', '{product_category}');\n"
            
            # 寫入到 SQL 檔案中
            sql_file.write(sql_line)

print(f"SQL INSERT 語句已生成並寫入 '{output_sql_path}'")
