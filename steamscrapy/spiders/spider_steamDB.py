import scrapy
from scrapy_playwright.page import PageCoroutine


class SteamDBConfigSpider(scrapy.Spider):
    name = "steamdb_config"
    start_urls = ["https://steamdb.info/charts/"]

    custom_settings = {
        "PLAYWRIGHT_PAGE_COROUTINES": [PageCoroutine("wait_for_selector", "tr.app")],
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={"playwright": True, "playwright_page_coroutines": [PageCoroutine("wait_for_selector", "tr.app")]},
            callback=self.parse_charts
        )

    def parse_charts(self, response):
        rows = response.css("tr.app")
        for row in rows:
            relative_link = row.css("td a::attr(href)").get()
            if relative_link and relative_link.startswith("/app/"):
                app_id = relative_link.split("/")[2]
                config_url = f"https://steamdb.info/app/{app_id}/config/"
                yield scrapy.Request(
                    url=config_url,
                    meta={"playwright": True},
                    callback=self.parse_config
                )

    def parse_config(self, response):
        app_name = response.css("h1::text").get()
        config_text = " | ".join(response.css(".table-responsive::text").getall()).strip()

        yield {
            "name": app_name,
            "url": response.url,
            "config": config_text
        }