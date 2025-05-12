import json
import time
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Chemins des fichiers ===
DATA_DIR = "data"
STORE_LINKS_FILE = os.path.join(DATA_DIR, "steam_store_links.json")
SYSREQS_FILE = os.path.join(DATA_DIR, "steam_sysreqs.json")
ERRORS_FILE = os.path.join(DATA_DIR, "steam_sysreqs_errors.json")

def setup_driver():
    """Configure et retourne une instance du navigateur Chrome."""
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def extract_config_from_block(block):
    """Extrait les configurations système d'un bloc HTML."""
    lis = block.find_elements(By.CSS_SELECTOR, "ul.bb_ul > li")
    config = {}
    for li in lis:
        text = li.text.strip()
        if not text or text.lower().startswith("minimale") or text.lower().startswith("recommandée"):
            continue
        match = re.match(r'^\s*([^:]+):\s*(.+)', text)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            config[key] = value
    return config

def handle_cookies(driver):
    """Gère l'acceptation des cookies si nécessaire."""
    try:
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "acceptAllButton"))
        )
        driver.execute_script("arguments[0].click();", cookie_btn)
        logger.info("Cookies acceptés.")
        time.sleep(1)
    except:
        logger.info("Pas de popup cookies détectée.")

def handle_age_check(driver):
    """Gère la vérification d'âge pour les jeux avec contenu pour adultes."""
    try:
        age_check = driver.find_elements(By.ID, "app_agegate")

        if age_check:
            logger.info("Page de vérification d'âge détectée")

            try:
                day_dropdown = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "ageDay"))
                )
                day_selector = webdriver.support.ui.Select(day_dropdown)
                day_selector.select_by_value("10")
                logger.info("Jour sélectionné: 10")

                month_dropdown = driver.find_element(By.ID, "ageMonth")
                month_selector = webdriver.support.ui.Select(month_dropdown)
                month_selector.select_by_value("January")
                logger.info("Mois sélectionné: janvier (January)")

                year_dropdown = driver.find_element(By.ID, "ageYear")
                year_selector = webdriver.support.ui.Select(year_dropdown)
                year_selector.select_by_value("1995")
                logger.info("Année sélectionnée: 1995")

                time.sleep(1)

                submit_buttons = driver.find_elements(By.CSS_SELECTOR,
                    "a.btnv6_blue_hoverfade, a.btn_medium, input[type='submit'], button#view_product_page_btn")

                if submit_buttons:
                    submit_button = submit_buttons[0]
                    driver.execute_script("arguments[0].click();", submit_button)
                    logger.info("Formulaire d'âge soumis avec succès")
                    time.sleep(2)
                    return True
                else:
                    logger.warning("Bouton de soumission non trouvé")

            except Exception as e:
                logger.error(f"Erreur lors de la sélection de l'âge: {e}")
                try:
                    driver.execute_script("""
                        document.getElementById('ageDay').value = '10';
                        document.getElementById('ageMonth').value = 'January';
                        document.getElementById('ageYear').value = '1995';

                        // Chercher le bouton de soumission par différentes méthodes
                        var buttons = document.querySelectorAll('a.btnv6_blue_hoverfade, a.btn_medium, input[type="submit"], button#view_product_page_btn');
                        if (buttons.length > 0) {
                            buttons[0].click();
                        }
                    """)
                    logger.info("Tentative de soumission via JavaScript")
                    time.sleep(2)
                    return True
                except Exception as e2:
                    logger.error(f"Échec de la tentative JavaScript: {e2}")

        return False
    except Exception as e:
        logger.warning(f"Erreur lors de la vérification d'âge: {e}")
        return False

def scrape_game(driver, game_name, url):
    logger.info(f"Scraping de {game_name} - {url}")

    driver.get(url)
    time.sleep(3)

    handle_cookies(driver)
    handle_age_check(driver)

    game_data = {}
    game_price = None

    try:
        # === Scraper le prix ===
        try:
            price_elem = driver.find_element(By.CSS_SELECTOR, "div.game_purchase_price.price")
            game_price = price_elem.text.strip()
            logger.info(f"Prix trouvé : {game_price}")
        except Exception as e:
            logger.warning(f"Prix non trouvé pour {game_name} : {e}")

        # === Scraper la config système (comme avant) ===
        sysreq_block = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.game_page_autocollapse.sys_req"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", sysreq_block)
        time.sleep(2)

        tabs = driver.find_elements(By.CSS_SELECTOR, "div.sysreq_tab[data-os]")
        os_list = [tab.get_attribute("data-os") for tab in tabs]

        if os_list:
            for os_type in os_list:
                try:
                    tab_elem = driver.find_element(By.CSS_SELECTOR, f"div.sysreq_tab[data-os='{os_type}']")
                    driver.execute_script("arguments[0].scrollIntoView(true);", tab_elem)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", tab_elem)
                    time.sleep(1)

                    block = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, f"div.game_area_sys_req.sysreq_content[data-os='{os_type}']"))
                    )
                    config = extract_config_from_block(block)
                    if config:
                        game_data[os_type] = config
                        logger.info(f"Config minimale extraite pour {os_type}")
                except Exception as e:
                    logger.error(f"Erreur avec {os_type} pour {game_name} : {e}")
        else:
            try:
                block = driver.find_element(By.CSS_SELECTOR, "div.game_area_sys_req_leftCol")
                config = extract_config_from_block(block)
                if config:
                    game_data["win"] = config
                    logger.info(f"Config minimale extraite (bloc unique)")
            except Exception as e:
                logger.error(f"Aucun bloc détecté : {e}")

        if not game_data:
            raise Exception("Aucune configuration système trouvée")

        return {"config": game_data, "price": game_price}, None

    except Exception as e:
        error_msg = f"Section config non trouvée pour {game_name} : {e}"
        logger.error(error_msg)
        return None, {"game": game_name, "url": url, "reason": str(e)}

def load_json_file(file_path, default=None):
    """Charge un fichier JSON ou retourne une valeur par défaut si le fichier n'existe pas."""
    if default is None:
        default = {}

    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return default
    except json.JSONDecodeError:
        logger.error(f"Erreur lors du décodage JSON de {file_path}. Utilisation de la valeur par défaut.")
        return default

def save_json_file(file_path, data):
    """Enregistre des données dans un fichier JSON."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def process_games(games_to_scrape, max_games=100):
    """Traite la liste des jeux à scraper et renvoie les résultats et erreurs."""
    driver = setup_driver()
    results = {}
    errors = []

    try:
        # Limiter le nombre de jeux si spécifié
        if max_games is not None:
            games_to_scrape = dict(list(games_to_scrape.items())[:max_games])

        for i, (game_name, url) in enumerate(games_to_scrape.items()):
            logger.info(f"{i+1}/{len(games_to_scrape)} - Traitement de {game_name}")

            game_data, error = scrape_game(driver, game_name, url)

            if game_data:
                results[game_name] = game_data

            if error:
                errors.append(error)

            # Pause entre chaque requête pour éviter d'être bloqué
            time.sleep(10)

    finally:
        driver.quit()

    return results, errors

def reprocess_errors():
    """Retraite les jeux ayant échoué lors du premier passage."""
    # Charger les données existantes
    existing_results = load_json_file(SYSREQS_FILE)
    previous_errors = load_json_file(ERRORS_FILE, [])

    if not previous_errors:
        logger.info("Aucune erreur à retraiter.")
        return

    logger.info(f"Retraitement de {len(previous_errors)} jeux ayant échoué.")

    # Créer un dictionnaire des jeux à rescanner à partir des erreurs
    games_to_rescan = {error["game"]: error["url"] for error in previous_errors}

    # Rescanner ces jeux
    new_results, new_errors = process_games(games_to_rescan)

    # Mettre à jour les résultats existants avec les nouvelles données
    existing_results.update(new_results)
    save_json_file(SYSREQS_FILE, existing_results)

    # Mettre à jour le fichier d'erreurs en supprimant les jeux résolus
    resolved_games = set(new_results.keys())
    updated_errors = [error for error in previous_errors if error["game"] not in resolved_games]

    # Ajouter les nouvelles erreurs qui pourraient être différentes
    error_games = set(error["game"] for error in updated_errors)
    for error in new_errors:
        if error["game"] not in error_games:
            updated_errors.append(error)

    save_json_file(ERRORS_FILE, updated_errors)

    logger.info(f"Retraitement terminé: {len(new_results)} jeux résolus, {len(updated_errors)} erreurs restantes.")

def main():
    """Fonction principale du script."""
    # Vérifier si le dossier de données existe
    os.makedirs(DATA_DIR, exist_ok=True)

    # Charger les URLs des jeux
    if not os.path.exists(STORE_LINKS_FILE):
        logger.error(f"Le fichier {STORE_LINKS_FILE} n'existe pas. Impossible de continuer.")
        return

    games = load_json_file(STORE_LINKS_FILE)

    # Vérifier si le fichier d'erreurs existe pour un retraitement éventuel
    if os.path.exists(ERRORS_FILE):
        logger.info("Fichier d'erreurs détecté, vérification pour retraitement...")
        reprocess_errors()

    # Déterminer les jeux à scraper (ceux qui ne sont pas déjà dans les résultats)
    existing_results = load_json_file(SYSREQS_FILE)
    games_to_scrape = {name: url for name, url in games.items() if name not in existing_results}

    if not games_to_scrape:
        logger.info("Tous les jeux ont déjà été scrapés. Rien à faire.")
        return

    logger.info(f"Scraping de {len(games_to_scrape)} nouveaux jeux...")

    # Scraper les jeux (limité à 100 pour cet exemple)
    results, errors = process_games(games_to_scrape, max_games=100)

    # Mettre à jour les résultats existants
    existing_results.update(results)
    save_json_file(SYSREQS_FILE, existing_results)

    # Mettre à jour ou créer le fichier d'erreurs
    existing_errors = load_json_file(ERRORS_FILE, [])

    # Ajouter uniquement les nouvelles erreurs
    error_games = set(error["game"] for error in existing_errors)
    for error in errors:
        if error["game"] not in error_games:
            existing_errors.append(error)

    save_json_file(ERRORS_FILE, existing_errors)

    logger.info(f"Scraping terminé: {len(results)} jeux scrapés, {len(errors)} erreurs.")

if __name__ == "__main__":
    main()
