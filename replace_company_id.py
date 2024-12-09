import csv
import os

# 檔案路徑
album_list_path = os.path.join('csv', 'album_list.csv')
company_list_path = os.path.join('csv', 'company_list.csv')
artist_list_path = os.path.join('csv', 'artist.csv')
output_album_list_path = os.path.join('csv', 'album_list_with_id.csv')

# 載入公司清單並建立字典映射
company_mapping = {}
with open(company_list_path, 'r', encoding='utf-8-sig') as company_file:
    company_reader = csv.DictReader(company_file)
    for row in company_reader:
        company_mapping[row['CompanyName']] = row['CompanyID']

# 載入藝人清單並建立字典映射
artist_mapping = {}
with open(artist_list_path, 'r', encoding='utf-8-sig') as artist_file:
    artist_reader = csv.DictReader(artist_file)
    for row in artist_reader:
        artist_mapping[row['ArtistName']] = row['ArtistID']

# 替換專輯清單中的 Publisher 和 Manufacturer 欄位為對應的 CompanyID
with open(album_list_path, 'r', encoding='utf-8-sig') as album_file:
    album_reader = csv.DictReader(album_file)
    
    # 準備輸出檔案
    fieldnames = album_reader.fieldnames

    with open(output_album_list_path, 'w', encoding='utf-8-sig', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        # 讀取每一筆資料，進行資料更新並寫入輸出檔案
        for row in album_reader:
            publisher_name = row.get('Publisher', '')
            manufacturer_name = row.get('Manufacturer', '')
            
            # 根據 Publisher 和 Manufacturer 找出對應的 CompanyID
            publisher_company_id = company_mapping.get(publisher_name, 'NULL')  # 若未找到則設為 'NULL'
            manufacturer_company_id = company_mapping.get(manufacturer_name, 'NULL')  # 若未找到則設為 'NULL'

            # 將 Publisher 和 Manufacturer 欄位替換為對應的 CompanyID
            row['Publisher'] = publisher_company_id
            row['Manufacturer'] = manufacturer_company_id

            # 如果需要將 ArtistID 替換為對應的 ArtistID，請加上以下程式碼
            artist_name = row.get('ArtistID', '')
            artist_id = artist_mapping.get(artist_name, 'NULL')
            row['ArtistID'] = artist_id

            # 將更新後的資料寫入輸出檔案
            if row['ArtistID'] != 'NULL':
                writer.writerow(row)

print(f"已將更新後的專輯清單寫入至: {output_album_list_path}")
