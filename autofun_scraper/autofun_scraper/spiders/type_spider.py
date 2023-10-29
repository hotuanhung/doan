import scrapy
import os
import json
import time
from pathlib import Path

class AutofunSpiderSpider(scrapy.Spider):
    name = "type_spider"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net/oto-xe-may/v-car"]
    type_file = 'type.json'

    def parse(self, response):
        if not os.path.isfile(self.type_file):
            with open(self.type_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)
        else:
            # Xóa dữ liệu trong tệp brand.json
            with open(self.type_file, 'w', encoding='utf-8') as f: 
                json.dump([], f, ensure_ascii=False)
        new_type_data = {
            "type_name": "Van",
            "type_image": "",
            "type_desc": 'Xe Van (viết tắt của "vehicle" và "van") là một loại xe ô tô thiết kế để chở hàng hoặc hành khách. Ở Việt Nam, xe Van thường được sử dụng để chở hành khách hoặc hàng hóa trong các mục đích thương mại hoặc vận chuyển. Dòng xe Van thường có thiết kế tiện lợi với một khoang chứa hàng hoặc hành khách ở phía sau và có thể chở nhiều người hoặc hàng hóa một cách thoải mái.Xe Van thường có hình dáng hộp chữ nhật và không có các đặc điểm của dòng xe hạng sang hay thể thao. Điều này làm cho xe Van trở thành một lựa chọn phổ biến trong việc vận chuyển hành khách trong các dịp gia đình hoặc chở hàng hóa dài hạn.'
        }

        # Đọc dữ liệu hiện có từ tệp JSON
        with open(self.type_file, 'r', encoding='utf-8') as f:
            types = json.load(f)

        # Thêm dòng dữ liệu mới vào danh sách
        types.append(new_type_data)

        # Ghi lại dữ liệu vào tệp JSON
        with open(self.type_file, 'w', encoding='utf-8') as f:
            json.dump(types, f, ensure_ascii=False)
        for type in response.css("div.car "):
            type_name = type.css("a::attr(title)").get()
            type_image = type.css("img::attr(src)").get()
            link = type.css("a::attr(href)").get()
            link_page = response.urljoin(link)
            yield scrapy.Request(link_page, callback=self.parse_type,
                                 meta={"type_name": type_name,  "type_image": type_image})
            
    def parse_type(self, response):
        # Lấy thông tin từ meta
        type_name = response.meta["type_name"]
        type_image = response.meta["type_image"]

        # Tìm tất cả các phần tử <p> có class là "Normal" và lấy phần text
        p_elements = response.css('div.container.info-hang-xe.flex:not([style*="display: none;"]) div.content p.Normal')
        type_desc = ' '.join([p.css("::text").get() for p in p_elements])

        # Tạo đối tượng chứa thông tin hãng xe
        type_data = {
            "type_name": type_name,
            "type_image": type_image,
            "type_desc": type_desc
        }

        with open(self.type_file, 'r', encoding='utf-8') as f:
            types = json.load(f)

        types.append(type_data)

        with open(self.type_file, 'w', encoding='utf-8') as f:
            json.dump(types, f, ensure_ascii=False)

    