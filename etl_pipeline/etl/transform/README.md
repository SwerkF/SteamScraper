# Transformation des données système pour les jeux Steam

Ce module est responsable de la transformation et de la normalisation des exigences système des jeux Steam avant leur insertion dans la base de données MongoDB.

## Fonctionnalités

- Normalisation des configurations système (OS, CPU, GPU, RAM)
- Extraction intelligente des modèles de CPU et GPU depuis les descriptions textuelles
- Support pour deux méthodes de stockage:
  - **Méthode texte**: Stocke les données sous forme de chaînes normalisées
  - **Méthode référence**: Stocke les données avec des références \_id vers des collections distinctes

## Utilisation

1. Assurez-vous que les fichiers JSON de données sont disponibles dans le dossier `@data/`:

   - `games_data.json`: données générales des jeux
   - `steam_sysreqs.json`: configurations système des jeux

2. Définissez vos variables d'environnement (ou utilisez les valeurs par défaut):

   ```
   MONGO_URI=mongodb://root:password@localhost:27017/
   DB_NAME=steam_games
   ```

3. Exécutez le script:

   ```
   python transform.py
   ```

4. Pour tester les patterns d'extraction sans exécuter la transformation complète:
   ```python
   # Décommentez dans le fichier transform.py
   if __name__ == "__main__":
       test_extraction_patterns()
       # main()
   ```

## Structure des données

### Méthode texte

```json
{
  "system_requirements": {
    "win": {
      "Système d'exploitation": "Windows 10",
      "Processeur": "Intel Core i5-6600K, AMD Ryzen 5 1600",
      "Graphiques": "NVIDIA GeForce GTX 970, AMD Radeon R9 290X",
      "Mémoire vive": "8 GB RAM"
    }
  }
}
```

### Méthode référence

```json
{
  "system_requirements": {
    "win": {
      "os": {
        "name": "Windows 10",
        "refs": ["615a8f41c382884f3e9b7c6d"]
      },
      "cpu": {
        "name": "Intel Core i5-6600K / AMD Ryzen 5 1600",
        "models": ["Intel Core i5-6600K", "AMD Ryzen 5 1600"],
        "refs": ["615a8f41c382884f3e9b7c6e", "615a8f41c382884f3e9b7c6f"]
      },
      "gpu": {
        "name": "NVIDIA GeForce GTX 970 / AMD Radeon R9 290X",
        "models": ["NVIDIA GeForce GTX 970", "AMD Radeon R9 290X"],
        "refs": ["615a8f41c382884f3e9b7c70", "615a8f41c382884f3e9b7c71"]
      },
      "ram": {
        "name": "8 GB RAM",
        "refs": ["615a8f41c382884f3e9b7c72"]
      }
    }
  }
}
```

## Collections MongoDB

Le script crée ou utilise les collections suivantes:

- **games**: Collection principale des jeux
- **cpus**: Liste de tous les modèles de CPU (utilisée avec la méthode référence)
- **gpus**: Liste de tous les modèles de GPU (utilisée avec la méthode référence)
- **os**: Liste des systèmes d'exploitation (utilisée avec la méthode référence)
- **ram**: Liste des configurations de RAM (utilisée avec la méthode référence)

## Configuration

Pour choisir la méthode de normalisation, modifiez la variable `use_refs` dans la fonction `main()`:

```python
# True: utiliser les références d'ID pour les composants (recommandé pour la recherche)
# False: utiliser uniquement des chaînes de texte normalisées
use_refs = True
```

## Exemples de requêtes MongoDB

Une fois les données transformées, vous pouvez effectuer des requêtes comme:

```javascript
// Trouver tous les jeux compatibles avec Windows 10
db.games.find({ 'system_requirements.win.os.name': 'Windows 10' });

// Trouver tous les jeux qui fonctionnent avec un CPU spécifique (méthode référence)
db.games.find({
  'system_requirements.win.cpu.refs': ObjectId('615a8f41c382884f3e9b7c6e'),
});

// Trouver tous les jeux qui nécessitent au moins 8 GB de RAM
db.games.find({ 'system_requirements.win.ram.name': '8 GB RAM' });
```
