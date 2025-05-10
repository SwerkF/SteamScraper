# etl/extract/hardware_spider.py

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_hardware_spider():
    class HardwareSpider(scrapy.Spider):
        name = "hardware"
        custom_settings = {
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

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
            results = []

            if hardware_type == "gpu":
                rows = response.css('table#cputable tr')[1:]
                for row in rows:
                    cells = row.css('td')
                    if len(cells) >= 5:
                        gpu_id = row.attrib.get('id', '').replace('gpu', '')
                        name = cells[0].css('a::text').get('').strip()
                        g3d_mark = cells[1].css('::text').get('').strip()
                        rank = cells[2].css('::text').get('').strip()

                        results.append({
                            "hardware_type": "gpu",
                            "id": int(gpu_id) if gpu_id.isdigit() else None,
                            "name": name,
                            "g3d_mark": g3d_mark,
                            "rank": int(rank) if rank.isdigit() else None
                        })

            elif hardware_type == "cpu":
                rows = response.css('table tr')[1:]
                for row in rows:
                    cells = row.css('td')
                    if len(cells) >= 3:
                        name = cells[0].css('a::text').get('').strip()
                        cpu_mark = cells[1].css('::text').get('').strip()
                        rank = cells[2].css('::text').get('').strip()

                        results.append({
                            "hardware_type": "cpu",
                            "name": name,
                            "cpu_mark": cpu_mark,
                            "rank": int(rank) if rank.isdigit() else None
                        })

            filename = f"hardware_{hardware_type}.json"
            with open(filename, "w", encoding="utf-8") as f:
                import json
                json.dump(results, f, indent=4, ensure_ascii=False)
            self.log(f"✅ {hardware_type.upper()} sauvegardé dans {filename}")

    process = CrawlerProcess()
    process.crawl(HardwareSpider)
    process.start()
