import os
import sys
import time
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "etl/extract")
TRANSFORM_DIR = os.path.join(BASE_DIR, "etl/transform")

os.makedirs("data", exist_ok=True)

scripts = [
    {"path": os.path.join(SCRIPTS_DIR, "steamDB_charts.py"), "name": "Extraction de la liste des jeux", "timeout": 180},
    {"path": os.path.join(SCRIPTS_DIR, "steamDB_games-details.py"), "name": "Extraction des détails des jeux", "timeout": None},
    {"path": os.path.join(SCRIPTS_DIR, "steamDB_config.py"), "name": "Extraction des configurations système", "timeout": None},
    {"path": os.path.join(TRANSFORM_DIR, "transform.py"), "name": "Fusion et stockage dans MongoDB", "timeout": 60},
]

def run_script(script_info):
    script_path = script_info["path"]
    script_name = script_info["name"]
    timeout = script_info["timeout"]

    start_time = time.time()
    print(f"Démarrage de {script_name} ({script_path})")

    try:
        process = subprocess.Popen([sys.executable, script_path],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)

        if timeout is None:
            # Pas de timeout, on attend la fin du processus peu importe le temps nécessaire
            stdout, stderr = process.communicate()
        else:
            # On applique le timeout spécifié
            stdout, stderr = process.communicate(timeout=timeout)
            
        exit_code = process.returncode

        for line in stdout.splitlines():
            print(f"[{os.path.basename(script_path)}] {line}")

        if stderr:
            for line in stderr.splitlines():
                print(f"[{os.path.basename(script_path)}] {line}")

        end_time = time.time()
        duration = end_time - start_time

        if exit_code == 0:
            print(f"Script {script_name} terminé avec succès en {duration:.2f} secondes.")
            return True
        else:
            print(f"Script {script_name} a échoué avec le code {exit_code}.")
            return False

    except subprocess.TimeoutExpired:
        print(f"Script {script_name} a dépassé le délai d'attente de {timeout} secondes.")
        return False
    except Exception as e:
        print(f"Erreur lors de l'exécution de {script_name}: {str(e)}")
        return False

def main():
    print("=== DÉMARRAGE DU PROCESSUS ETL STEAM ===")

    for i, script_info in enumerate(scripts, 1):
        print(f"ÉTAPE {i}/{len(scripts)}: {script_info['name']}")

        if not os.path.exists(script_info["path"]):
            print(f"Script {script_info['path']} introuvable.")
            continue

        success = run_script(script_info)

        if not success and i < len(scripts):
            answer = input(f"Le script {script_info['name']} a échoué. Voulez-vous continuer avec le script suivant? (o/n): ").lower()
            if answer != 'o':
                print("Processus ETL interrompu par l'utilisateur.")
                break

    print("=== FIN DU PROCESSUS ETL STEAM ===")

if __name__ == "__main__":
    main()