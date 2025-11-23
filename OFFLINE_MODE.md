# Mode Offline - Utilisation Sans API / Offline Mode - No API Required

## 🎯 Vue d'ensemble / Overview

**Bonne nouvelle !** Vous pouvez utiliser cet outil **SANS clé API Proxycurl**. L'API est maintenant **complètement optionnelle** et uniquement nécessaire si vous voulez scraper de nouveaux profils depuis LinkedIn.

**Good news!** You can use this tool **WITHOUT a Proxycurl API key**. The API is now **completely optional** and only needed if you want to scrape new profiles from LinkedIn.

---

## ✅ Ce que vous POUVEZ faire sans API / What you CAN do without API

### 1. Mode Démo / Demo Mode
Générez immédiatement 10 profils réalistes pour tester l'outil :

```bash
python demo_data.py
```

Cela crée automatiquement :
- ✅ 10 profils LinkedIn de démonstration
- ✅ Base de données SQLite remplie
- ✅ Exports CSV, JSON, Markdown
- ✅ Statistiques (50% chercheurs d'emploi, 50% employés)

### 2. Importer vos propres profils / Import Your Own Profiles

**Import depuis CSV** :
```bash
python main.py import --input my_profiles.csv
```

**Import depuis JSON** :
```bash
python main.py import --input my_profiles.json
```

Le format est automatiquement détecté depuis l'extension du fichier.

### 3. Gérer les profils / Manage Profiles

**Lister tous les profils** :
```bash
python main.py list
```

**Filtrer par école** :
```bash
python main.py list --school "Harvard"
```

**Filtrer par statut d'emploi** :
```bash
python main.py list --job-status seeking
```

### 4. Exporter les données / Export Data

**Export CSV** :
```bash
python main.py export --format csv --output results.csv
```

**Export JSON** :
```bash
python main.py export --format json --output results.json
```

**Export Markdown** :
```bash
python main.py export --format markdown --output results.md
```

### 5. Voir les statistiques / View Statistics

```bash
python main.py stats
```

Affiche :
- Nombre total de profils
- Nombre de chercheurs d'emploi
- Nombre de personnes employées
- Top écoles
- Top entreprises
- Top localisations

---

## ❌ Ce qui NÉCESSITE une clé API / What REQUIRES an API key

Seulement la commande `scrape` pour obtenir de nouveaux profils depuis LinkedIn :

```bash
# ❌ NÉCESSITE PROXYCURL_API_KEY
python main.py scrape --school "Harvard University" --max-profiles 50
```

Si vous essayez sans clé API, vous verrez :
```
Configuration errors:
  ❌ PROXYCURL_API_KEY is required for scraping
  ❌ Get your API key at: https://nubela.co/proxycurl/
  ❌ Or use demo mode: python demo_data.py

Tip: You can use the app without an API key!
Options without API key:
  • python demo_data.py  (generate demo profiles)
  • python main.py import --input data.csv
  • python main.py list
  • python main.py export --format csv --output results.csv
```

---

## 📋 Format des fichiers pour l'import / Import File Format

### Format CSV

Votre fichier CSV doit avoir ces colonnes (headers) :

```csv
profile_id,name,headline,school,degree,field_of_study,graduation_year,current_company,current_position,is_open_to_work,location,profile_url,about,connections,scraped_at
demo-001,John Doe,Software Engineer,Harvard University,BS Computer Science,Computer Science,2020,Google,Senior Engineer,False,"San Francisco, USA",https://linkedin.com/in/johndoe,Passionate developer,500,2025-11-13T10:00:00
demo-002,Jane Smith,Looking for opportunities,MIT,MS Data Science,Data Science,2021,,,True,"Boston, USA",https://linkedin.com/in/janesmith,Data scientist seeking role,350,2025-11-13T10:00:00
```

**Colonnes requises** :
- `profile_id` - Identifiant unique
- `name` - Nom complet

**Colonnes optionnelles** :
- `headline` - Titre professionnel
- `school` - École/Université
- `degree` - Diplôme
- `field_of_study` - Domaine d'études
- `graduation_year` - Année de diplôme
- `current_company` - Entreprise actuelle
- `current_position` - Poste actuel
- `is_open_to_work` - Cherche un emploi (True/False)
- `location` - Localisation
- `profile_url` - URL du profil LinkedIn
- `about` - Résumé
- `connections` - Nombre de connexions
- `scraped_at` - Date de collecte

### Format JSON

```json
[
  {
    "profile_id": "demo-001",
    "name": "John Doe",
    "headline": "Software Engineer",
    "school": "Harvard University",
    "degree": "BS Computer Science",
    "field_of_study": "Computer Science",
    "graduation_year": "2020",
    "current_company": "Google",
    "current_position": "Senior Engineer",
    "is_open_to_work": false,
    "location": "San Francisco, USA",
    "profile_url": "https://linkedin.com/in/johndoe",
    "about": "Passionate developer",
    "connections": 500,
    "scraped_at": "2025-11-13T10:00:00"
  },
  {
    "profile_id": "demo-002",
    "name": "Jane Smith",
    "headline": "Looking for opportunities",
    "school": "MIT",
    "is_open_to_work": true,
    "location": "Boston, USA"
  }
]
```

---

## 🚀 Workflows recommandés / Recommended Workflows

### Workflow 1 : Test rapide / Quick Test
```bash
# 1. Générer des données de démo
python demo_data.py

# 2. Explorer les profils
python main.py list

# 3. Exporter
python main.py export --format csv --output test.csv
```

### Workflow 2 : Import de vos données / Import Your Data
```bash
# 1. Préparer votre fichier CSV avec vos profils
# (voir format ci-dessus)

# 2. Importer dans la base de données
python main.py import --input my_profiles.csv

# 3. Vérifier l'import
python main.py stats

# 4. Filtrer et exporter
python main.py list --school "Harvard"
python main.py export --format json --output harvard.json --school "Harvard"
```

### Workflow 3 : Analyse de données / Data Analysis
```bash
# 1. Importer plusieurs fichiers
python main.py import --input batch1.csv
python main.py import --input batch2.csv
python main.py import --input batch3.json

# 2. Voir les statistiques globales
python main.py stats

# 3. Filtrer par critères
python main.py list --job-status seeking

# 4. Exporter les résultats filtrés
python main.py export --format csv --output job_seekers.csv --job-status seeking
```

---

## 💡 Cas d'usage sans API / Use Cases Without API

### 1. Gestion de base de données de contacts
- Importez vos contacts LinkedIn existants
- Organisez-les par école, entreprise, statut
- Exportez pour campagnes de recrutement

### 2. Analyse de cohortes d'alumni
- Importez des listes d'anciens élèves
- Analysez les statistiques d'emploi
- Identifiez les chercheurs d'emploi

### 3. Test et développement
- Utilisez les données de démo
- Testez les fonctionnalités d'export
- Développez des intégrations

### 4. Formation et démonstration
- Montrez l'outil à votre équipe
- Créez des présentations
- Formez les utilisateurs

---

## 🔧 Configuration

Vous n'avez **AUCUNE configuration** à faire pour utiliser le mode offline !

Le fichier `.env` n'est nécessaire que si vous voulez scraper :

```bash
# Optionnel - uniquement pour scraping
PROXYCURL_API_KEY=your_api_key_here
```

---

## ❓ FAQ

**Q : Puis-je vraiment utiliser l'outil sans API ?**
R : Oui ! Toutes les fonctions sauf `scrape` fonctionnent sans API.

**Q : Comment obtenir des profils sans scraper ?**
R : Trois options :
   1. Utilisez `python demo_data.py` pour des profils de démo
   2. Importez vos propres CSV/JSON avec `python main.py import`
   3. Collectez manuellement et créez un CSV

**Q : Les profils de démo sont-ils réalistes ?**
R : Oui ! Ils contiennent des noms, écoles, entreprises, postes, localisations réalistes.

**Q : Puis-je mélanger démo et vrais profils ?**
R : Oui ! Vous pouvez importer plusieurs sources dans la même base de données.

**Q : L'API Proxycurl est-elle gratuite ?**
R : Proxycurl offre 100 crédits gratuits, puis c'est payant. Mais vous n'en avez pas besoin pour utiliser cet outil !

**Q : Comment exporter depuis LinkedIn manuellement ?**
R : LinkedIn ne permet pas d'export direct d'autres profils. Utilisez plutôt le mode import avec vos propres données.

---

## 📊 Exemple complet / Complete Example

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Générer des données de test
python demo_data.py

# 3. Voir ce qui a été créé
ls -lh exports/
# demo_profiles.csv
# demo_profiles.json
# demo_profiles.md

# 4. Importer d'autres profils (exemple)
python main.py import --input additional_profiles.csv

# 5. Voir toutes les statistiques
python main.py stats

# 6. Lister seulement les chercheurs d'emploi
python main.py list --job-status seeking

# 7. Exporter tout en JSON
python main.py export --format json --output all_profiles.json

# 8. Exporter seulement École Polytechnique
python main.py export --format csv --output polytechnique.csv --school "Polytechnique"
```

---

## 🎯 Résumé / Summary

| Fonctionnalité / Feature | Besoin API / Need API | Commande / Command |
|--------------------------|----------------------|-------------------|
| Générer profils démo | ❌ Non | `python demo_data.py` |
| Importer CSV/JSON | ❌ Non | `python main.py import --input file.csv` |
| Lister profils | ❌ Non | `python main.py list` |
| Exporter données | ❌ Non | `python main.py export --format csv --output file.csv` |
| Voir statistiques | ❌ Non | `python main.py stats` |
| Scraper LinkedIn | ✅ Oui | `python main.py scrape --school "Harvard"` |

**Conclusion : 5 fonctions sur 6 ne nécessitent AUCUNE API !** 🎉
