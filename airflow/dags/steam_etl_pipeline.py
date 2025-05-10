from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import os

# Chemin de base vers ton ETL
ETL_DIR = "/opt/airflow/etl_pipeline"

# Fonctions qui appellent tes scripts existants
def run_scraper_games_urls():
    subprocess.run(["python", os.path.join(ETL_DIR, "extract", "scraper_games_urls.py")], check=True)

def run_scraper_games_data():
    subprocess.run(["python", os.path.join(ETL_DIR, "extract", "scraper_games_data.py")], check=True)

def run_scraper_config():
    subprocess.run(["python", os.path.join(ETL_DIR, "extract", "scraper_config_steam.py")], check=True)

def run_scrapy_hardware():
    subprocess.run(["scrapy", "crawl", "hardware"], cwd=os.path.join(ETL_DIR, "extract"), check=True)

def run_mongo_loader():
    subprocess.run(["python", os.path.join(ETL_DIR, "load", "mongo_loader.py")], check=True)

# DAG definition
with DAG(
    dag_id="steam_etl_pipeline_v1",
    start_date=datetime(2025, 5, 10),
    schedule_interval=None,  # On le lance manuellement au début
    catchup=False,
    tags=["steam", "etl"]
) as dag:

    task_urls = PythonOperator(
        task_id="extract_top_game_urls",
        python_callable=run_scraper_games_urls
    )

    task_game_data = PythonOperator(
        task_id="extract_game_details",
        python_callable=run_scraper_games_data
    )

    task_config = PythonOperator(
        task_id="extract_system_requirements",
        python_callable=run_scraper_config
    )

    task_hardware = PythonOperator(
        task_id="extract_hardware_data",
        python_callable=run_scrapy_hardware
    )

    task_load = PythonOperator(
        task_id="load_all_to_mongo",
        python_callable=run_mongo_loader
    )

    # Définir l’ordre d’exécution
    task_urls >> task_game_data >> task_config >> task_hardware >> task_load
