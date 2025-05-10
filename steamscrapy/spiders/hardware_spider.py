import scrapy
import csv
from steamscrapy.items import HardwareItem

class HardwareSpider(scrapy.Spider):
    name = "hardware"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def start_requests(self):
        urls = [
            {"url": "https://www.videocardbenchmark.net/gpu_list.php", "type": "gpu"},
            {"url": "https://www.cpubenchmark.net/cpu_list.php", "type": "cpu"},
        ]

        for item in urls:
            yield scrapy.Request(
                url=item["url"],
                callback=self.parse,
                meta={"hardware_type": item["type"]}
            )

    def parse(self, response):
        hardware_type = response.meta.get("hardware_type", "")

        filename = f"{hardware_type}_index.html" if hardware_type else "index.html"
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        if hardware_type == "gpu":
            yield from self.parse_gpu_data(response)
        elif hardware_type == "cpu":
            yield from self.parse_cpu_data(response)

    def parse_gpu_data(self, response):
        rows = response.css('table#cputable tr')

        for row in rows[1:]:
            cells = row.css('td')
            if len(cells) >= 5:
                gpu_id = row.attrib.get('id', '').replace('gpu', '')

                name_link = cells[0].css('a')
                gpu_name = name_link.css('::text').get('').strip()

                g3d_mark = cells[1].css('::text').get('').strip()
                rank = cells[2].css('::text').get('').strip()

                item = HardwareItem()
                item['hardware_type'] = 'gpu'
                item['name'] = gpu_name
                item['rank'] = int(rank) if rank.isdigit() else 0

                item['g3d_mark'] = g3d_mark
                item['id'] = int(gpu_id) if gpu_id.isdigit() else 0

                yield item

        self.log(f'Extracted GPU data for MongoDB')

    def parse_cpu_data(self, response):
        rows = response.css('table tr')

        for row in rows[1:]:
            cells = row.css('td')
            if len(cells) >= 3:
                name_link = cells[0].css('a')
                cpu_name = name_link.css('::text').get('').strip()

                cpu_mark = cells[1].css('::text').get('').strip()
                rank = cells[2].css('::text').get('').strip()

                item = HardwareItem()
                item['hardware_type'] = 'cpu'
                item['name'] = cpu_name
                item['rank'] = int(rank) if rank.isdigit() else 0

                item['cpu_mark'] = cpu_mark

                yield item

        self.log(f'Extracted CPU data for MongoDB')
