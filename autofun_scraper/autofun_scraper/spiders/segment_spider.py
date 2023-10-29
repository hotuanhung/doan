import scrapy
import os
import json

class AutofunSpiderSpider(scrapy.Spider):
    name = "segment_spider"
    allowed_domains = ["autofun.vn"]
    start_urls = ["https://www.autofun.vn/xe-oto"]
    segment_file = 'segment.json'

    def parse(self, response):
        if not os.path.isfile(self.segment_file):
            with open(self.segment_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)
        else:
            # Xóa dữ liệu trong tệp brand.json
            with open(self.segment_file, 'w', encoding='utf-8') as f: 
                json.dump([], f, ensure_ascii=False)
        for segment in response.css("div.brand-filter-item-link"):
            segment_name = brand.css("a p::text").get()
            yield scrapy.Request(brand_page, callback=self.parse_brand,
                                  meta={"brand_name": brand_name,  "brand_logo": brand_logo})

    def parse_brand(self, response):
        # Lấy thông tin từ meta
        brand_name = response.meta["brand_name"]
        brand_logo = response.meta["brand_logo"]
        brand_desc_text = response.xpath('//div[@class="brand-desc"]/p//text()').getall()
        brand_desc = ' '.join(brand_desc_text)
        # Tạo đối tượng chứa thông tin hãng xe
        brand_data = {
            "brand_name": brand_name,
            "brand_logo": brand_logo,
            "brand_desc": brand_desc
        }

        # Đọc dữ liệu từ file JSON
        with open(self.segment_file, 'r', encoding='utf-8') as f:
            brands = json.load(f)

        # Thêm thông tin hãng xe vào danh sách
        brands.append(brand_data)

        # Ghi lại dữ liệu vào file JSON
        with open(self.segment_file, 'w', encoding='utf-8') as f:
            json.dump(brands, f, ensure_ascii=False)
