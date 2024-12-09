import csv
import os

# 設定輸入和輸出檔案的路徑
input_csv_path = os.path.join('csv', 'artist.csv')
output_sql_path = os.path.join('SQL', 'insert_artist.sql')

# 確保 SQL 資料夾存在
os.makedirs(os.path.dirname(output_sql_path), exist_ok=True)


# 讀取 CSV 檔案並生成 INSERT 語句
with open(input_csv_path, 'r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    with open(output_sql_path, 'w', encoding='utf-8-sig') as sql_file:
        for row in csv_reader:
            # 用變數來預處理欄位值，避免在 f-string 中使用複雜的運算
            artist_id = row['ArtistID']
            artist_name = row['ArtistName'].replace("'", "''")
            artist_type = row['ArtistType'].replace("'", "''")
            artist_category = row['ArtistCategory'].replace("'", "''")
            
            # 生成單行 INSERT 語句
            sql_line = f"INSERT INTO artist (ArtistID, ArtistName, ArtistType, ArtistCategory) VALUES ({artist_id}, '{artist_name}', '{artist_type}', '{artist_category}');\n"
            
            # 寫入到 SQL 檔案中
            sql_file.write(sql_line)

print(f"SQL INSERT 語句已生成並寫入 '{output_sql_path}'")
