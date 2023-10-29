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
with open('type.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Vòng lặp để chèn dữ liệu từ JSON vào cơ sở dữ liệu
for item in data:
    type_name = item['type_name']
    type_image = item['type_image']
    type_desc = item['type_desc']

    # Chuỗi SQL chèn dữ liệu vào bảng
    insert_query = "INSERT INTO type (type_name, type_image, type_desc) VALUES (%s, %s, %s)"

    # Thực hiện câu lệnh SQL với dữ liệu từ JSON
    cursor.execute(insert_query, (type_name, type_image, type_desc))

# Lưu thay đổi vào cơ sở dữ liệu
db_connection.commit()

# Đóng kết nối
cursor.close()
db_connection.close()
