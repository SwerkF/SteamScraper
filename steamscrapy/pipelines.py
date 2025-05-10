# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from steamscrapy.mongodb import db
import datetime


class SteamscrapyPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        adapter['timestamp'] = datetime.datetime.now()

        if spider.name == "hardware":
            hardware_type = adapter.get('hardware_type', '')

            if hardware_type == "gpu":
                db.gpu.insert_one(dict(item))
                spider.logger.info(f"GPU saved to MongoDB: {adapter.get('name')}")
            elif hardware_type == "cpu":
                db.cpu.insert_one(dict(item))
                spider.logger.info(f"CPU saved to MongoDB: {adapter.get('name')}")

        return item
