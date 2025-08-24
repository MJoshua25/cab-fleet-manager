#!/bin/sh

set -e

 echo "Environnement: ${DJANGO_ENV:-$env}"

echo "En attente de la base de donnée"
#./wait-for db:5432

echo "Exécution des migrations"
python manage.py migrate --noinput

echo "Collecte des fichiers statiques"
python manage.py collectstatic --noinput

echo "Démarrage du serveur Gunicorn"
exec gunicorn projet.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --access-logfile '-' \
    --error-logfile '-'