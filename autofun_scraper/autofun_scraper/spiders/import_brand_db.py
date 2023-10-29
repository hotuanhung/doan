import mysql.connector
import json

# Kết nối đến cơ sở dữ liệu MySQL
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='car_autofun'
)

# Tạo một đối tượng cursor
cursor = db_connection.cursor()

# Đọc dữ liệu từ tệp JSON
with open('brand.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Vòng lặp để chèn dữ liệu từ JSON vào cơ sở dữ liệu
for item in data:
    brand_name = item['brand_name']
    brand_logo = item['brand_logo']
    brand_desc = item['brand_desc']

    # Chuỗi SQL chèn dữ liệu vào bảng
    insert_query = "INSERT INTO brand (brand_name, brand_logo, brand_desc) VALUES (%s, %s, %s)"

    # Thực hiện câu lệnh SQL với dữ liệu từ JSON
    cursor.execute(insert_query, (brand_name, brand_logo, brand_desc))

# Lưu thay đổi vào cơ sở dữ liệu
db_connection.commit()

# Đóng kết nối
cursor.close()
db_connection.close()
