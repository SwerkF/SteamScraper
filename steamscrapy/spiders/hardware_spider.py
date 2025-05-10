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

        # Sauvegarde du fichier HTML original
        filename = f"{hardware_type}_index.html" if hardware_type else "index.html"
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        if hardware_type == "gpu":
            self.parse_gpu_data(response)
        elif hardware_type == "cpu":
            self.parse_cpu_data(response)

    def parse_gpu_data(self, response):
        # Extraction des données GPU
        gpu_data = []

        # Sélection de toutes les lignes du tableau
        rows = response.css('table#cputable tr')

        # Pour chaque ligne (sauf l'en-tête)
        for row in rows[1:]:  # Skip header row
            # Extraction des cellules
            cells = row.css('td')
            if len(cells) >= 5:
                gpu_id = row.attrib.get('id', '').replace('gpu', '')

                # Extraction du nom et nettoyage
                name_link = cells[0].css('a')
                gpu_name = name_link.css('::text').get('').strip()

                # Extraction des autres données
                g3d_mark = cells[1].css('::text').get('').strip()
                rank = cells[2].css('::text').get('').strip()

                # Ajout des données à la liste (sans value et price)
                gpu_data.append({
                    'id': gpu_id,
                    'name': gpu_name,
                    'g3d_mark': g3d_mark,
                    'rank': rank
                })

        # Sauvegarde des données dans un fichier CSV
        csv_file = 'gpu_benchmark.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'name', 'g3d_mark', 'rank']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for data in gpu_data:
                writer.writerow(data)

        self.log(f'Extracted {len(gpu_data)} GPUs to {csv_file}')

    def parse_cpu_data(self, response):
        # Extraction des données CPU
        cpu_data = []

        # Sélection de toutes les lignes du tableau
        rows = response.css('table tr')

        # Pour chaque ligne (sauf l'en-tête)
        for row in rows[1:]:  # Skip header row
            # Extraction des cellules
            cells = row.css('td')
            if len(cells) >= 3:
                # Extraction du nom et nettoyage
                name_link = cells[0].css('a')
                cpu_name = name_link.css('::text').get('').strip()

                # Extraction des autres données
                cpu_mark = cells[1].css('::text').get('').strip()
                rank = cells[2].css('::text').get('').strip()

                # Ajout des données à la liste
                cpu_data.append({
                    'name': cpu_name,
                    'cpu_mark': cpu_mark,
                    'rank': rank
                })

        # Sauvegarde des données dans un fichier CSV
        csv_file = 'cpu_benchmark.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['name', 'cpu_mark', 'rank']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for data in cpu_data:
                writer.writerow(data)

        self.log(f'Extracted {len(cpu_data)} CPUs to {csv_file}')
