# Guide de Dépannage / Troubleshooting Guide

## Problème : Fichiers d'export vides / Empty Export Files

### Symptômes / Symptoms
- Les fichiers CSV/JSON/MD sont créés mais ne contiennent aucune donnée
- Seulement les en-têtes CSV sont présents, sans aucune ligne de données
- JSON contient un tableau vide `[]`

### Causes Possibles / Possible Causes

#### 1. Base de données vide / Empty Database
**Symptôme** : Message "No profiles found in database"

**Solution** :
```bash
# Vérifier la base de données
python main.py stats

# Si vide, scraper des profils
python main.py scrape --school "École Polytechnique" --max-profiles 10

# OU utiliser le mode démo (pas besoin d'API key)
python demo_data.py
```

#### 2. Problème avec l'API Proxycurl / Proxycurl API Issues

**Symptôme** : Le scraping retourne 0 profils

**Vérifications** :
```bash
# Vérifier que la clé API est configurée
cat .env | grep PROXYCURL_API_KEY

# Tester l'API manuellement
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "https://nubela.co/proxycurl/api/v2/linkedin?url=https://linkedin.com/in/williamhgates"
```

**Solutions** :
- Vérifier que `PROXYCURL_API_KEY` est défini dans `.env`
- Vérifier que votre clé API est valide sur https://nubela.co/proxycurl/
- Vérifier votre quota d'API (crédits restants)
- Essayer avec un nom d'école plus connu (Harvard, MIT, Stanford)

#### 3. Filtres trop restrictifs / Overly Restrictive Filters

**Symptôme** : Le scraping trouve des profils mais l'export est vide

**Exemple** :
```bash
# Scrape uniquement job seekers
python main.py scrape --school "MIT" --job-status seeking

# Mais essaie d'exporter tous les profils
python main.py export --format csv --output results.csv
# ❌ Peut être vide si l'école filtrée n'est pas "MIT"
```

**Solution** :
```bash
# Exporter avec les mêmes filtres
python main.py list --school "MIT" --job-status seeking
python main.py export --format csv --output results.csv --school "MIT" --job-status seeking
```

### Mode Démo - Test sans API / Demo Mode - Test without API

Pour tester le système sans clé API :

```bash
# Générer 10 profils de démonstration
python demo_data.py

# Vérifier la base de données
python main.py stats

# Lister les profils
python main.py list

# Exporter
python main.py export --format csv --output test.csv
python main.py export --format json --output test.json
python main.py export --format markdown --output test.md
```

Les fichiers seront créés dans `./exports/`

### Nouvelles Améliorations / New Improvements

#### Messages d'avertissement / Warning Messages

L'exportateur affiche maintenant des messages clairs :

```
⚠️  Warning: No profiles to export. Creating empty CSV file.
```

ou

```
✅ Exported 10 profiles to ./exports/profiles.csv
```

#### Détails des erreurs / Error Details

En cas d'erreur, la stack trace complète est affichée :

```
❌ Error exporting to CSV: [Errno 13] Permission denied: '/protected/file.csv'
Traceback (most recent call last):
  ...
```

## Commandes de Diagnostic / Diagnostic Commands

### 1. Vérifier l'état de la base de données
```bash
python main.py stats
```

**Résultat attendu** :
```
📊 Statistics:
  Total Profiles: 10
  Job Seekers: 5
  Employed: 5
```

### 2. Lister tous les profils
```bash
python main.py list
```

### 3. Vérifier les fichiers exportés
```bash
# Taille des fichiers
ls -lh exports/

# Contenu CSV
head exports/demo_profiles.csv

# Nombre de lignes (devrait être > 1)
wc -l exports/demo_profiles.csv
```

### 4. Tester avec données de démo
```bash
# Nettoyer la base
rm -f data/profiles.db

# Générer données de démo
python demo_data.py

# Exporter
python main.py export --format csv --output test.csv
```

## Workflow Recommandé / Recommended Workflow

### Première utilisation avec API Proxycurl
```bash
# 1. Configurer l'API
cp .env.example .env
# Éditer .env et ajouter PROXYCURL_API_KEY

# 2. Scraper des profils
python main.py scrape --school "Harvard University" --max-profiles 20

# 3. Vérifier les résultats
python main.py stats

# 4. Exporter
python main.py export --format csv --output harvard.csv
```

### Test rapide sans API
```bash
# 1. Générer données de démo
python demo_data.py

# 2. Exporter immédiatement
# (Les fichiers sont déjà créés dans exports/)

# 3. Vérifier
cat exports/demo_profiles.csv
```

## Logs et Debugging

### Activer les logs détaillés
Les logs sont automatiquement écrits dans `./logs/scraper.log`

```bash
# Voir les logs en temps réel
tail -f logs/scraper.log

# Chercher des erreurs
grep ERROR logs/scraper.log
grep -i "no profiles" logs/scraper.log
```

### Vérifier les permissions
```bash
# Vérifier que vous pouvez écrire dans exports/
touch exports/test.txt && rm exports/test.txt

# Vérifier la base de données
sqlite3 data/profiles.db "SELECT COUNT(*) FROM profiles;"
```

## FAQ

**Q: Pourquoi mon fichier CSV ne contient que les en-têtes ?**
R: La base de données est probablement vide. Lancez `python main.py stats` pour vérifier.

**Q: Le scraping dit "Found 0 profiles". Pourquoi ?**
R: Soit le nom de l'école est incorrect, soit votre clé API a des problèmes. Essayez avec "Harvard University" ou "MIT".

**Q: Puis-je tester sans clé API ?**
R: Oui ! Utilisez `python demo_data.py` pour générer des profils de démonstration.

**Q: Combien coûte l'API Proxycurl ?**
R: Proxycurl offre 100 crédits gratuits. Consultez https://nubela.co/proxycurl/pricing

**Q: Les exports sont vides mais `list` montre des profils ?**
R: Vérifiez que vous utilisez les mêmes filtres (--school, --job-status) pour les deux commandes.

## Support

Pour plus d'aide :
1. Vérifier les logs : `cat logs/scraper.log`
2. Tester avec le mode démo : `python demo_data.py`
3. Consulter la documentation Proxycurl : https://nubela.co/proxycurl/docs
4. Ouvrir une issue sur GitHub avec les logs
