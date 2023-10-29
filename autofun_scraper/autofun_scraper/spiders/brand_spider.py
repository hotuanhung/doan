import scrapy
import os
import json

class AutofunSpiderSpider(scrapy.Spider):
    name = "brand_spider"
    allowed_domains = ["autofun.vn"]
    start_urls = ["https://www.autofun.vn/xe-oto"]
    brand_file = 'brand.json'

    def parse(self, response):
        if not os.path.isfile(self.brand_file):
            with open(self.brand_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)
        else:
            # Xóa dữ liệu trong tệp brand.json
            with open(self.brand_file, 'w', encoding='utf-8') as f: 
                json.dump([], f, ensure_ascii=False)
        for brand in response.css("div.brand-filter-item-link"):
            brand_name = brand.css("a p::text").get()
            brand_link = brand.css("a::attr(href)").get()
            brand_logo = brand.css("img::attr(src)").get()
            brand_page = response.urljoin(brand_link)
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
        with open(self.brand_file, 'r', encoding='utf-8') as f:
            brands = json.load(f)

        # Thêm thông tin hãng xe vào danh sách
        brands.append(brand_data)

        # Ghi lại dữ liệu vào file JSON
        with open(self.brand_file, 'w', encoding='utf-8') as f:
            json.dump(brands, f, ensure_ascii=False)
