# Guide de résolution des problèmes

## Erreur de connexion PostgreSQL en développement local

### Problème
```
django.db.utils.OperationalError: connection is bad: nodename nor servname provided, or not known
```

### Cause
Le fichier `.env` est configuré pour Docker avec `POSTGRES_HOST=db`, mais en développement local (sans Docker), le service `db` n'existe pas.

### Solution

1. **Configuration automatique** : Le projet charge maintenant automatiquement `.env.local` s'il existe, sinon `.env`

2. **Fichier `.env.local`** créé pour le développement local :
   - `bd=SQLITE` : utilise SQLite au lieu de PostgreSQL
   - `POSTGRES_HOST=localhost` : si vous voulez utiliser PostgreSQL local
   - `BASE_URL="http://127.0.0.1:8001"` : adapté au port local

3. **Utilisation** :
   - **Développement local** : `python manage.py runserver localhost:8001`
   - **Docker** : `docker compose up` (utilise `.env`)

## Configuration par environnement

| Fichier | Usage | Base de données | POSTGRES_HOST | DJANGO_ENV |
|---------|-------|-----------------|---------------|------------|
| `.env` | Développement local | SQLite (bd=SQLITE) | `localhost` | `development` |
| `.env.prod` | Production Docker | PostgreSQL (bd=POSTGRES) | `db` | `production` |

## Commandes d'utilisation

### Développement local (sans Docker)
```bash
# Utilise .env par défaut (SQLite)
python manage.py runserver localhost:8001
```

### Production Docker
```bash
# Utilise .env.prod (PostgreSQL)
DJANGO_ENV=production docker compose up
```