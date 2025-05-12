import json
import os
import re
import argparse
from pymongo import MongoClient

# Récupérer les variables d'environnement
MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:password@localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "steam_games")

# Connexion MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
games_collection = db['games']
cpu_collection = db['cpu']
gpu_collection = db['gpu']
os_collection = db['os']
ram_collection = db['memory']

def load_json_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        return []

def normalize_system_requirements(system_reqs):
    """Standardise les configurations système"""
    if not system_reqs:
        return {}

    normalized_reqs = {}

    for platform, requirements in system_reqs.items():
        normalized_platform = platform.lower()
        if normalized_platform not in ['win', 'mac', 'linux']:
            if normalized_platform in ['windows', 'windows 10', 'windows 11']:
                normalized_platform = 'win'
            elif normalized_platform in ['macos', 'osx']:
                normalized_platform = 'mac'

        normalized_reqs[normalized_platform] = {}

        for key, value in requirements.items():
            if not value:
                continue

            key_lower = key.lower()

            if any(os_term in key_lower for os_term in ['système', 'system', 'os']):
                normalized_os = normalize_os(value)
                normalized_reqs[normalized_platform]['Système d\'exploitation'] = normalized_os

            elif any(cpu_term in key_lower for cpu_term in ['processeur', 'processor', 'cpu']):
                normalized_cpu = normalize_cpu(value)
                normalized_reqs[normalized_platform]['Processeur'] = normalized_cpu

            elif any(gpu_term in key_lower for gpu_term in ['graphi', 'video', 'gpu', 'carte']):
                normalized_gpu = normalize_gpu(value)
                normalized_reqs[normalized_platform]['Graphiques'] = normalized_gpu

            elif any(ram_term in key_lower for ram_term in ['mémoire', 'memory', 'ram']):
                normalized_ram = normalize_ram(value)
                normalized_reqs[normalized_platform]['Mémoire vive'] = normalized_ram

            else:
                normalized_reqs[normalized_platform][key] = value

    return normalized_reqs

def normalize_system_requirements_with_refs(requirements):
    """Standardise les configurations système avec des références aux ID des composants"""
    if not requirements:
        return {}

    normalized_reqs = {}

    if isinstance(requirements, dict) and "config" in requirements:
        requirements = requirements["config"]

    for platform, platform_reqs in requirements.items():
        normalized_platform = platform.lower()
        if normalized_platform not in ['win', 'mac', 'linux']:
            if normalized_platform in ['windows', 'windows 10', 'windows 11']:
                normalized_platform = 'win'
            elif normalized_platform in ['macos', 'osx']:
                normalized_platform = 'mac'

        normalized_reqs[normalized_platform] = {}

        for key, value in platform_reqs.items():
            if not value:
                continue

            key_lower = key.lower()

            if any(os_term in key_lower for os_term in ['système', 'system', 'os']):
                os_name = normalize_os(value)
                os_refs = get_os_references(os_name)
                normalized_reqs[normalized_platform]['os'] = {
                    'name': os_name,
                    'refs': os_refs
                }

            elif any(cpu_term in key_lower for cpu_term in ['processeur', 'processor', 'cpu']):
                cpu_models = extract_cpu_models(value)
                cpu_refs = get_cpu_references(cpu_models)
                normalized_reqs[normalized_platform]['cpu'] = {
                    'name': value,
                    'models': cpu_models,
                    'refs': cpu_refs
                }

            elif any(gpu_term in key_lower for gpu_term in ['graphi', 'video', 'gpu', 'carte']):
                gpu_models = extract_gpu_models(value)
                gpu_refs = get_gpu_references(gpu_models)
                normalized_reqs[normalized_platform]['gpu'] = {
                    'name': value,
                    'models': gpu_models,
                    'refs': gpu_refs
                }

            elif any(ram_term in key_lower for ram_term in ['mémoire', 'memory', 'ram']):
                ram_value = normalize_ram(value)
                ram_refs = get_ram_references(ram_value)
                normalized_reqs[normalized_platform]['ram'] = {
                    'name': ram_value,
                    'refs': ram_refs
                }

            else:
                normalized_reqs[normalized_platform][key] = value

    return normalized_reqs

def normalize_os(os_string):
    """Normalise le système d'exploitation"""
    os_string = os_string.lower()

    if 'windows 11' in os_string or 'win 11' in os_string:
        return 'Windows 11'
    elif 'windows 10' in os_string or 'win 10' in os_string:
        return 'Windows 10'
    elif 'windows 8' in os_string or 'win 8' in os_string:
        return 'Windows 8'
    elif 'windows 7' in os_string or 'win 7' in os_string:
        return 'Windows 7'
    elif 'windows' in os_string:
        return 'Windows 10'  # Par défaut pour Windows

    elif 'macos' in os_string or 'mac os' in os_string or 'osx' in os_string:
        return 'MacOS'

    elif 'linux' in os_string or 'ubuntu' in os_string or 'debian' in os_string or 'fedora' in os_string:
        return 'Linux'

    return os_string

def normalize_cpu(cpu_string):
    """Normalise les processeurs"""
    if not cpu_string:
        return cpu_string

    cpu_models = extract_cpu_models(cpu_string)

    if cpu_models:
        return ', '.join(cpu_models)

    return cpu_string

def extract_cpu_models(cpu_string):
    """Extrait les modèles de CPU à partir d'une chaîne"""
    if not cpu_string:
        return []

    cleaned_text = cpu_string.strip()
    cleaned_text = re.sub(r'\s+(?:or better|ou mieux|ou supérieur|or higher|or equivalent|\(ou mieux\)|\(or better\))', '', cleaned_text, flags=re.IGNORECASE)
    cpu_alternatives = re.split(r'\s+(?:/|ou|or|,)\s+', cleaned_text)
    cpu_models = []

    for cpu_alt in cpu_alternatives:
        # Extraire les modèles de CPU spécifiques avec fréquence
        specific_with_freq = re.search(r'(Intel(?:®)?\s+Core(?:™)?\s+i\d+[-\s]\d+\w*).*?([\d,.]+)\s*(?:GHz|MHz)', cpu_alt, re.IGNORECASE)
        if specific_with_freq:
            cpu_model = re.sub(r'(?:®|™)', '', specific_with_freq.group(1).strip())
            if cpu_model not in cpu_models:
                cpu_models.append(cpu_model)
            continue

        # Cas spécial pour Intel Core i5-750
        i5_750_match = re.search(r'Intel(?:®)?\s+Core(?:™)?\s+i5[-\s]750', cpu_alt, re.IGNORECASE)
        if i5_750_match:
            cpu_models.append("Intel Core i5-750")
            continue

        # Vérifier si c'est un CPU générique sans modèle spécifique avec fréquence
        generic_match = re.search(r'(?:processeur|cpu)?\s*(?:intel|amd)?\s*(?:dual|quad)[-\s]?core\s+(?:à|@)?\s*([\d,.]+)\s*(?:ghz|mhz)', cpu_alt, re.IGNORECASE)

        if generic_match:
            frequency = generic_match.group(1).replace(',', '.') + " GHz"
            cpu_models.append(frequency)
            continue

        # Recherche simple de fréquence seule
        freq_match = re.search(r'(?:à|@)?\s*([\d,.]+)\s*(?:ghz|mhz)', cpu_alt, re.IGNORECASE)
        if freq_match and "core" in cpu_alt.lower():
            frequency = freq_match.group(1).replace(',', '.') + " GHz"
            if frequency not in cpu_models:
                cpu_models.append(frequency)
            continue

        # Recherche de modèles Intel i5/i7 plus génériques
        intel_generic = re.search(r'Intel(?:®)?\s+(?:Core(?:™)?)?\s*i([357])[- ]?(\d{3,4}[A-Z]*)', cpu_alt, re.IGNORECASE)
        if intel_generic:
            model = f"Intel Core i{intel_generic.group(1)}-{intel_generic.group(2)}"
            if model not in cpu_models:
                cpu_models.append(model)
            continue

        found_specific = False

        # Recherche des processeurs AMD
        amd_patterns = [
            # Ryzen series
            r'AMD\s+Ryzen\s+\d+\s+\d+\w+',  # Ex: AMD Ryzen 5 5600X
            r'AMD\s+Ryzen\s+\d+\s+PRO\s+\d+\w+',  # Ex: AMD Ryzen 5 PRO 4650G
            r'AMD\s+Ryzen\s+\d+',  # Ex: AMD Ryzen 5

            # FX series
            r'AMD\s+FX[-\s]\d+\w*',  # Ex: AMD FX-8350

            # A-Series
            r'AMD\s+A\d+[-\s]\d+\w*',  # Ex: AMD A10-7850K

            # Athlon series
            r'AMD\s+Athlon\s+\w+\s+\d+\w*',  # Ex: AMD Athlon II X4 640
            r'AMD\s+Athlon\s+\d+\w+',  # Ex: AMD Athlon 3000G
            r'AMD\s+Athlon\s+X\d+\s+\d+\w*',  # Ex: AMD Athlon X4 860K

            # Phenom series
            r'AMD\s+Phenom\s+II\s+X\d+\s+\d+\w*',  # Ex: AMD Phenom II X4 955
            r'AMD\s+Phenom\s+\w+\s+\d+\w*',  # Ex: AMD Phenom X4 9950
        ]

        for pattern in amd_patterns:
            matches = re.finditer(pattern, cpu_alt, re.IGNORECASE)
            for match in matches:
                cpu_model = match.group(0).strip()
                if cpu_model not in cpu_models:
                    cpu_models.append(cpu_model)
                    found_specific = True

        # Recherche des processeurs Intel
        intel_patterns = [
            # Core series
            r'Intel(?:®)?\s+Core(?:™)?\s+i\d+[-\s]\d+\w+',  # Ex: Intel Core i7-6700K
            r'Intel(?:®)?\s+Core(?:™)?\s+i\d+\s+\d+\w*\s+Gen',  # Ex: Intel Core i5 10th Gen
            r'Intel(?:®)?\s+Core(?:™)?\s+i\d+',  # Ex: Intel Core i5

            # Pentium
            r'Intel\s+Pentium\s+\w+[-\s]\d+\w*',  # Ex: Intel Pentium G4560

            # Celeron
            r'Intel\s+Celeron\s+\w+[-\s]\d+\w*',  # Ex: Intel Celeron G1840

            # Xeon
            r'Intel\s+Xeon\s+\w+[-\s]\d+\w*',  # Ex: Intel Xeon E5-2680
        ]

        for pattern in intel_patterns:
            matches = re.finditer(pattern, cpu_alt, re.IGNORECASE)
            for match in matches:
                cpu_model = match.group(0).strip()
                cpu_model = re.sub(r'(?:®|™)', '', cpu_model)
                if cpu_model not in cpu_models:
                    cpu_models.append(cpu_model)
                    found_specific = True

        # Si aucun modèle spécifique n'est trouvé, chercher une fréquence
        if not found_specific:
            frequency_match = re.search(r'([\d,.]+)\s*(?:ghz|mhz)', cpu_alt, re.IGNORECASE)
            if frequency_match:
                frequency = frequency_match.group(1).replace(',', '.') + " GHz"
                if frequency not in cpu_models:
                    cpu_models.append(frequency)
            elif "intel" in cpu_alt.lower() or "amd" in cpu_alt.lower():
                if "any" not in cpu_models:
                    cpu_models.append("any")

    # Détecter les doublons générique/spécifique
    for i in range(len(cpu_models) - 1, -1, -1):
        for j in range(len(cpu_models)):
            if i != j and cpu_models[i] in cpu_models[j] and cpu_models[i] != cpu_models[j]:
                cpu_models.pop(i)
                break

    if not cpu_models:
        cpu_models.append("any")

    return cpu_models

def normalize_gpu(gpu_string):
    """Normalise les cartes graphiques"""
    if not gpu_string:
        return gpu_string

    gpu_models = extract_gpu_models(gpu_string)

    if gpu_models:
        return ', '.join(gpu_models)

    return gpu_string

def extract_gpu_models(gpu_string):
    """Extrait les modèles de GPU à partir d'une chaîne"""
    if not gpu_string:
        return []

    cleaned_text = gpu_string.strip()
    cleaned_text = re.sub(r'\s+(?:or better|ou mieux|ou supérieur|or higher|or equivalent|\(ou mieux\)|\(or better\))', '', cleaned_text, flags=re.IGNORECASE)
    gpu_alternatives = re.split(r'\s+(?:/|ou|or|,)\s+', cleaned_text)
    gpu_models = []

    # Vérifier si c'est seulement une spécification de VRAM
    vram_match = re.search(r'(?:au moins)?\s*(\d+)\s*(?:GB|Go|G)(?:o)?\s*(?:de)?\s*(?:mémoire|VRAM)', cleaned_text, re.IGNORECASE)
    if vram_match and not re.search(r'(GeForce|Radeon|NVIDIA|AMD|Intel)', cleaned_text, re.IGNORECASE):
        vram = vram_match.group(1) + " Go VRAM"
        gpu_models.append(vram)
        return gpu_models

    # Vérifier s'il s'agit juste d'une compatibilité DirectX sans modèle spécifique
    directx_match = re.search(r'compatible\s+(?:avec)?\s+DirectX\s*(\d+)?', cleaned_text, re.IGNORECASE)
    if directx_match and not re.search(r'(GeForce|Radeon|NVIDIA|AMD|Intel)', cleaned_text, re.IGNORECASE):
        gpu_models.append("any")
        return gpu_models

    # Cas spécial pour les modèles Intel HD et Iris
    intel_hd_match = re.search(r'Intel\s+HD\s+\d+', cleaned_text, re.IGNORECASE)
    if intel_hd_match:
        gpu_models.append(intel_hd_match.group(0))

    intel_iris_match = re.search(r'Intel\s+Iris(?:\s+Pro)?\s+\d+', cleaned_text, re.IGNORECASE)
    if intel_iris_match:
        gpu_models.append(intel_iris_match.group(0))

    # Cas spécial pour NVIDIA GTX 1060 et similaires
    gtx_with_mem = re.search(r'(?:NVIDIA\s+)?GTX\s+(\d+)\s+(\d+)GB', cleaned_text, re.IGNORECASE)
    if gtx_with_mem:
        model = f"NVIDIA GeForce GTX {gtx_with_mem.group(1)}"
        if model not in gpu_models:
            gpu_models.append(model)
        model_simple = f"GeForce GTX {gtx_with_mem.group(1)}"
        if model_simple not in gpu_models:
            gpu_models.append(model_simple)

    # Traitement pour les cartes NVIDIA avec numéros de modèle multiples
    multi_model_match = re.search(r'NVIDIA\s+GeForce\s+(\d+)/(\d+)(?:GT)?', cleaned_text, re.IGNORECASE)
    if multi_model_match:
        model1 = f"NVIDIA GeForce {multi_model_match.group(1)}"
        model2 = f"NVIDIA GeForce {multi_model_match.group(2)}GT"
        if model1 not in gpu_models:
            gpu_models.append(model1)
        if model2 not in gpu_models:
            gpu_models.append(model2)
        return gpu_models

    for gpu_alt in gpu_alternatives:
        found_specific = False

        # Recherche des GPUs NVIDIA
        nvidia_patterns = [
            # RTX Series
            r'NVIDIA\s+GeForce\s+RTX\s+\d+\w*\s*(?:Ti|SUPER)?',  # Ex: NVIDIA GeForce RTX 3080 Ti
            r'GeForce\s+RTX\s+\d+\w*\s*(?:Ti|SUPER)?',           # Ex: GeForce RTX 3080 Ti

            # GTX Series
            r'NVIDIA\s+GeForce\s+GTX\s+\d+\w*\s*(?:Ti|SUPER)?',  # Ex: NVIDIA GeForce GTX 1660 Ti
            r'GeForce\s+GTX\s+\d+\w*\s*(?:Ti|SUPER)?',           # Ex: GeForce GTX 1660 Ti

            # Other GeForce
            r'NVIDIA\s+GeForce\s+\d+\w*',                         # Ex: NVIDIA GeForce 840M
            r'GeForce\s+\d+\w*',                                  # Ex: GeForce 840M

            # Quadro
            r'Quadro\s+RTX\s+\d+\w*',                             # Ex: Quadro RTX 4000
            r'Quadro\s+\w+\d+\w*'                                 # Ex: Quadro P2000
        ]

        for pattern in nvidia_patterns:
            matches = re.finditer(pattern, gpu_alt, re.IGNORECASE)
            for match in matches:
                gpu_model = match.group(0).strip()
                if gpu_model not in gpu_models:
                    gpu_models.append(gpu_model)
                    found_specific = True

        # Recherche des GPUs AMD
        amd_patterns = [
            # Radeon RX Series
            r'AMD\s+Radeon\s+RX\s+\d+\w*\s*(?:XT|VEGA)?',         # Ex: AMD Radeon RX 6800 XT
            r'Radeon\s+RX\s+\d+\w*\s*(?:XT|VEGA)?',               # Ex: Radeon RX 6800 XT

            # Radeon R Series
            r'AMD\s+Radeon\s+R\d+\s+\d+\w*',                      # Ex: AMD Radeon R9 290X
            r'Radeon\s+R\d+\s+\d+\w*',                            # Ex: Radeon R9 290X

            # Radeon HD Series
            r'AMD\s+Radeon\s+HD\s+\d+\w*',                        # Ex: AMD Radeon HD 7870
            r'Radeon\s+HD\s+\d+\w*',                              # Ex: Radeon HD 7870

            # FirePro
            r'FirePro\s+\w+\d+\w*',                               # Ex: FirePro W5100

            # Mobility Radeon
            r'Mobility\s+Radeon\s+HD\s+\d+\w*',                   # Ex: Mobility Radeon HD 5650
            r'Mobility\s+Radeon\s+\w+\s+\d+\w*'                   # Ex: Mobility Radeon X1800
        ]

        for pattern in amd_patterns:
            matches = re.finditer(pattern, gpu_alt, re.IGNORECASE)
            for match in matches:
                gpu_model = match.group(0).strip()
                if gpu_model not in gpu_models:
                    gpu_models.append(gpu_model)
                    found_specific = True

        # Intel integrated GPUs
        intel_patterns = [
            r'Intel\s+UHD\s+Graphics\s+\d+\w*',
            r'Intel\s+HD\s+Graphics\s+\d+\w*',
            r'Intel\s+Iris\s+\w+\s+Graphics\s+\d+\w*',
            r'Intel\s+Iris\s+\w+\s+Graphics'
        ]

        for pattern in intel_patterns:
            matches = re.finditer(pattern, gpu_alt, re.IGNORECASE)
            for match in matches:
                gpu_model = match.group(0).strip()
                if gpu_model not in gpu_models:
                    gpu_models.append(gpu_model)
                    found_specific = True

    # Si aucun modèle spécifique n'a été trouvé
    if not gpu_models:
        vram_match = re.search(r'(\d+)\s*(?:GB|Go|G)(?:o)?\s*(?:de)?\s*(?:mémoire|VRAM)', cleaned_text, re.IGNORECASE)
        if vram_match:
            vram = vram_match.group(1) + " Go VRAM"
            gpu_models.append(vram)
        else:
            gpu_models.append("any")

    return gpu_models

def normalize_ram(ram_string):
    """Normalise la mémoire RAM"""
    if not ram_string:
        return ram_string

    ram_match = re.search(r'(\d+)\s*(?:GB|Go|G)', ram_string, re.IGNORECASE)
    if ram_match:
        return f"{ram_match.group(1)}GB RAM"

    return ram_string

def normalize_price(price_string):
    """Normalise le prix en valeur numérique sans symbole de devise"""
    if not price_string:
        return 0.0

    if price_string.lower() == "free-to-play" or price_string.lower() == "free" or price_string.lower() == "gratuit":
        return 0.0

    price_match = re.search(r'(\d+[,.]\d+|\d+)', price_string)
    if price_match:
        price_value = price_match.group(1).replace(',', '.')
        return float(price_value)

    return 0.0

def get_os_references(os_name):
    """Récupère les IDs de référence pour un système d'exploitation"""
    if not os_name:
        return []

    os_doc = os_collection.find_one({"name": os_name})

    if os_doc:
        return [os_doc["_id"]]

    result = os_collection.insert_one({"name": os_name})
    return [result.inserted_id]

def get_cpu_references(cpu_models):
    """Récupère les IDs de référence pour des modèles de CPU"""
    if not cpu_models:
        return []

    cpu_refs = []
    ignored_values = ["any", "2.8 GHz", "3 GHz", "1.7 GHz", "2.4 GHz", "3.2 GHz", "4 GHz", "AMD", "Intel"]
    ignored_patterns = [r'^\d+\.?\d*\s*GHz$', r'^AMD\s+Ryzen\s+\d+$', r'^Intel\s+Core\s+i\d+$']

    for cpu_model in cpu_models:
        if cpu_model in ignored_values:
            continue

        skip = False
        for pattern in ignored_patterns:
            if re.match(pattern, cpu_model, re.IGNORECASE):
                skip = True
                break
        if skip:
            continue

        normalized_name = cpu_model.strip()
        model_parts = re.findall(r'((?:Intel|AMD)[\w\s-]+\d+(?:-\d+\w*)?|FX-\d+)', normalized_name, re.IGNORECASE)

        if not model_parts:
            continue

        search_term = model_parts[0]

        try:
            escaped_search_term = re.escape(search_term)
            cpu_doc = cpu_collection.find_one({"name": {"$regex": escaped_search_term, "$options": "i"}})

            if cpu_doc:
                cpu_refs.append(cpu_doc["_id"])
                continue

            if not cpu_doc and " " in search_term:
                specific_part = re.search(r'(i\d+-\d+\w*|FX-\d+\w*|Ryzen\s+\d+\s+\d+\w*)', search_term, re.IGNORECASE)
                if specific_part:
                    specific_term = specific_part.group(0)
                    escaped_specific_term = re.escape(specific_term)
                    cpu_doc = cpu_collection.find_one({"name": {"$regex": escaped_specific_term, "$options": "i"}})

                    if cpu_doc:
                        cpu_refs.append(cpu_doc["_id"])
                        continue

            print(f"Nouveau CPU à ajouter: {normalized_name}")
            result = cpu_collection.insert_one({"name": normalized_name})
            cpu_refs.append(result.inserted_id)

        except Exception as e:
            print(f"Erreur lors de la recherche du CPU {normalized_name}: {str(e)}")

    return cpu_refs

def get_gpu_references(gpu_models):
    """Récupère les IDs de référence pour des modèles de GPU"""
    if not gpu_models:
        return []

    gpu_refs = []
    ignored_values = ["any", "1 Go VRAM", "2 Go VRAM", "3 Go VRAM", "4 Go VRAM", "6 Go VRAM", "8 Go VRAM"]

    for gpu_model in gpu_models:
        if gpu_model in ignored_values:
            continue

        normalized_name = gpu_model.strip()
        normalized_name = re.sub(r'^NVIDIA\s+', '', normalized_name, flags=re.IGNORECASE)
        normalized_name = re.sub(r'^AMD\s+', '', normalized_name, flags=re.IGNORECASE)
        normalized_name = re.sub(r'(GeForce|Radeon)(\d+)', r'\1 \2', normalized_name)
        normalized_name = re.sub(r'(\d+)(GT|XT|Ti)', r'\1 \2', normalized_name)

        try:
            gpu_doc = gpu_collection.find_one({"name": normalized_name})

            if gpu_doc:
                gpu_refs.append(gpu_doc["_id"])
                continue

            base_pattern = re.escape(re.sub(r'\s+', ' ', normalized_name.split()[0]))
            if len(normalized_name.split()) > 1:
                model_number = re.search(r'(\d+)', normalized_name)
                if model_number:
                    base_pattern = base_pattern + r'.*' + re.escape(model_number.group(0))

            gpu_doc = gpu_collection.find_one({"name": {"$regex": base_pattern, "$options": "i"}})

            if gpu_doc:
                gpu_refs.append(gpu_doc["_id"])
                continue

            print(f"Nouveau GPU à ajouter: {normalized_name}")
            result = gpu_collection.insert_one({"name": normalized_name})
            gpu_refs.append(result.inserted_id)

        except Exception as e:
            print(f"Erreur lors de la recherche du GPU {normalized_name}: {str(e)}")

    return gpu_refs

def get_ram_references(ram_value):
    """Récupère les IDs de référence pour une quantité de RAM"""
    if not ram_value:
        return []

    ram_doc = ram_collection.find_one({"name": ram_value})

    if ram_doc:
        return [ram_doc["_id"]]

    result = ram_collection.insert_one({"name": ram_value})
    return [result.inserted_id]

def main():
    parser = argparse.ArgumentParser(description='Transformation de données système pour les jeux Steam')
    parser.add_argument('--f', action='store_true', help='Lire les données depuis le répertoire @data')
    args = parser.parse_args()

    data_dir = "@data" if args.f else "data"
    print(f"Lecture des données depuis le répertoire: {data_dir}")

    games_data = load_json_data(f"{data_dir}/games_data.json")
    system_requirements = load_json_data(f"{data_dir}/steam_sysreqs.json")

    use_refs = True

    game_count = 0
    games_with_both = 0
    games_with_details_only = 0
    games_with_configs_only = 0
    complete_games = []

    for game in games_data:
        game_name = game.get('name')
        if not game_name:
            continue

        game_count += 1

        if game_name in system_requirements:
            if "price" in system_requirements[game_name]:
                raw_price = system_requirements[game_name]["price"]
                game['price'] = normalize_price(raw_price)
                game['price_display'] = raw_price

            if use_refs:
                normalized_reqs = normalize_system_requirements_with_refs(system_requirements[game_name])
            else:
                normalized_reqs = normalize_system_requirements(system_requirements[game_name])

            game['system_requirements'] = normalized_reqs

            games_collection.update_one(
                {"name": game_name},
                {"$set": game},
                upsert=True
            )

            games_with_both += 1
            complete_games.append(game_name)
        else:
            games_with_details_only += 1

    for game_name in system_requirements:
        if not any(g.get('name') == game_name for g in games_data):
            games_with_configs_only += 1

    os.makedirs(data_dir, exist_ok=True)
    with open(f"{data_dir}/complete_games.json", "w", encoding="utf-8") as f:
        json.dump(complete_games, f, indent=4, ensure_ascii=False)

    print(f"Statistiques de traitement:")
    print(f"- Jeux traités: {game_count}")
    print(f"- Jeux avec détails et config: {games_with_both}")
    print(f"- Jeux avec détails uniquement: {games_with_details_only}")
    print(f"- Configurations sans détails: {games_with_configs_only}")
    print(f"- Méthode de normalisation: {'Références ID' if use_refs else 'Texte normalisé'}")

if __name__ == "__main__":
    main()
